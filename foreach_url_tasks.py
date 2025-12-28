"""
ForeachURL Celery tasks

任务名：
 - tasks.foreach_url_process_job
"""

from __future__ import annotations

import asyncio
import mimetypes
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlparse

from loguru import logger
from playwright.async_api import async_playwright

from app.celery_app import celery_app
from app.config import settings
from app.core.database import supabase


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_part(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return "NA"
    s = s.replace(" ", "_")
    s = re.sub(r"[^a-zA-Z0-9._-]", "_", s)
    s = re.sub(r"_+", "_", s)
    return s[:120] or "NA"


def _make_filename(ptn_no: str, product_id: str) -> str:
    return f"PTN_{_safe_part(ptn_no)}_{_safe_part(product_id)}.jpg"


def _pick_unique_name(base_name: str, used: set[str]) -> str:
    if base_name not in used:
        used.add(base_name)
        return base_name
    stem = base_name[:-4] if base_name.lower().endswith((".png", ".jpg", ".jpeg")) else base_name
    i = 2
    while True:
        candidate = f"{stem}_{i}.jpg"
        if candidate not in used:
            used.add(candidate)
            return candidate
        i += 1


def _classify_error(exc: Exception) -> Tuple[str, str]:
    msg = str(exc)
    low = msg.lower()
    if "timeout" in low:
        return "timeout", msg
    if "net::" in low or "dns" in low or "name not resolved" in low:
        return "network", msg
    return "navigation_error", msg


async def _upload_to_bucket(bucket: str, storage_path: str, local_path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(str(local_path))
    if not mime_type:
        mime_type = "image/png"
    with open(local_path, "rb") as f:
        content = f.read()

    # 上传（覆盖策略：若已存在会报错；我们用唯一文件名避免冲突）
    supabase.storage.from_(bucket).upload(
        path=storage_path,
        file=content,
        file_options={"content-type": mime_type},
    )

    return supabase.storage.from_(bucket).get_public_url(storage_path)


@celery_app.task(name="tasks.foreach_url_process_job")
def foreach_url_process_job(job_id: str):
    """
    顺序处理一个 job：遍历所有 results，访问 URL -> 记录状态码/错误 -> 成功则截图并上传
    """
    logger.info(f"🔁 ForeachURL job start: {job_id}")

    try:
        supabase.table("foreach_url_jobs").update(
            {"status": "running", "started_at": _now_iso()}
        ).eq("id", job_id).execute()

        # 拉取全部 results（只取必要字段）
        # 注意：Supabase 单次返回限制不明确，这里分页拉取
        all_results: list[dict[str, Any]] = []
        page_size = 1000
        offset = 0
        while True:
            resp = (
                supabase.table("foreach_url_results")
                .select("id,ptn_no,product_id,url,screenshot_url,http_status,error_type,error_message")
                .eq("job_id", job_id)
                .order("created_at", desc=False)
                .range(offset, offset + page_size - 1)
                .execute()
            )
            chunk = resp.data or []
            all_results.extend(chunk)
            if len(chunk) < page_size:
                break
            offset += page_size

        total = len(all_results)
        processed = 0
        success = 0
        failed = 0

        used_names: set[str] = set()
        screenshots_dir = Path("screenshots") / "foreach-url" / job_id
        screenshots_dir.mkdir(parents=True, exist_ok=True)

        bucket = getattr(settings, "FOREACH_URL_SCREENSHOT_BUCKET", "foreach-url-screenshots")

        async def run():
            nonlocal processed, success, failed

            async with async_playwright() as p:
                # 轻量级浏览器启动参数（针对低配置服务器优化）
                launch_args = [
                    '--no-sandbox',
                    '--disable-dev-shm-usage',  # 重要：低内存环境
                    '--disable-setuid-sandbox',
                    '--disable-gpu',  # 重要：节省资源
                    '--disable-software-rasterizer',
                    '--disable-extensions',
                    '--disable-background-networking',  # 减少后台网络请求
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-breakpad',
                    '--disable-client-side-phishing-detection',
                    '--disable-component-update',
                    '--disable-default-apps',
                    '--disable-domain-reliability',
                    '--disable-features=AudioServiceOutOfProcess',
                    '--disable-hang-monitor',
                    '--disable-ipc-flooding-protection',
                    '--disable-notifications',
                    '--disable-offer-store-unmasked-wallet-cards',
                    '--disable-popup-blocking',
                    '--disable-print-preview',
                    '--disable-prompt-on-repost',
                    '--disable-renderer-backgrounding',
                    '--disable-sync',
                    '--disable-translate',
                    '--metrics-recording-only',
                    '--no-first-run',
                    '--mute-audio',
                    '--safebrowsing-disable-auto-update',
                    '--enable-automation',
                    '--password-store=basic',
                    '--use-mock-keychain',
                ]
                
                browser = await p.chromium.launch(
                    headless=True,
                    args=launch_args,
                    chromium_sandbox=False,
                )
                
                # 轻量级上下文配置（降低分辨率，减少内存占用）
                context = await browser.new_context(
                    viewport={"width": 1280, "height": 720},  # 降低分辨率
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    locale="en-US",
                    ignore_https_errors=True,
                )
                
                page = await context.new_page()
                # 设置合理的超时时间
                page.set_default_navigation_timeout(getattr(settings, "PLAYWRIGHT_TIMEOUT", 30000))
                page.set_default_timeout(getattr(settings, "PLAYWRIGHT_TIMEOUT", 30000))

                try:
                    for r in all_results:
                        result_id = r["id"]
                        url = r.get("url") or ""
                        ptn_no = r.get("ptn_no") or ""
                        product_id = r.get("product_id") or ""

                        # 🔴 检查任务是否已被取消
                        job_status_check = supabase.table("foreach_url_jobs").select("status").eq("id", job_id).single().execute()
                        if job_status_check.data and job_status_check.data.get("status") == "cancelled":
                            logger.info(f"⚠️ ForeachURL job cancelled by user: {job_id}")
                            return {"job_id": job_id, "message": "任务已被用户取消", "cancelled": True}

                        # 如果已经处理过（已有截图或已有错误/状态码），跳过
                        if r.get("screenshot_url") or r.get("http_status") or r.get("error_type") or r.get("error_message"):
                            processed += 1
                            if r.get("screenshot_url"):
                                success += 1
                            else:
                                failed += 1
                            continue

                        http_status: Optional[int] = None
                        error_type: Optional[str] = None
                        error_message: Optional[str] = None
                        screenshot_url: Optional[str] = None
                        screenshot_path: Optional[str] = None

                        try:
                            # 基本 URL 校验
                            parsed = urlparse(url)
                            if parsed.scheme not in ("http", "https"):
                                raise ValueError(f"Invalid URL scheme: {url}")

                            # 适度延迟（降低服务器压力）
                            import random
                            await asyncio.sleep(random.uniform(2.0, 4.0))
                            
                            # 直接访问页面，不额外设置headers（避免崩溃）
                            resp = await page.goto(url, wait_until="domcontentloaded")
                            
                            # 简短等待让页面稳定
                            try:
                                await page.wait_for_load_state("networkidle", timeout=3000)
                            except Exception:
                                pass  # 超时不影响截图
                            
                            if resp is not None:
                                http_status = resp.status
                            else:
                                http_status = None

                            if http_status is not None and http_status >= 400:
                                error_type = "http_error"
                                error_message = f"HTTP {http_status}"
                            else:
                                base_name = _make_filename(ptn_no, product_id)
                                filename = _pick_unique_name(base_name, used_names)
                                local_path = screenshots_dir / filename

                                # 视口截图（降低质量以节省资源）
                                await page.screenshot(
                                    path=str(local_path), 
                                    full_page=False,
                                    type='jpeg',  # 使用JPEG格式，文件更小
                                    quality=80    # 降低质量以节省内存
                                )

                                storage_path = f"foreach-url/{job_id}/{filename}"
                                screenshot_path = storage_path
                                screenshot_url = await _upload_to_bucket(bucket, storage_path, local_path)

                        except Exception as exc:
                            et, em = _classify_error(exc)
                            error_type = et
                            error_message = em

                        # 写回 result
                        supabase.table("foreach_url_results").update(
                            {
                                "http_status": http_status,
                                "error_type": error_type,
                                "error_message": error_message,
                                "screenshot_url": screenshot_url,
                                "screenshot_path": screenshot_path,
                            }
                        ).eq("id", result_id).execute()

                        processed += 1
                        if screenshot_url:
                            success += 1
                        else:
                            failed += 1

                        # 更新 job 进度（单任务串行执行，不存在并发写冲突）
                        supabase.table("foreach_url_jobs").update(
                            {
                                "total": total,
                                "processed": processed,
                                "success": success,
                                "failed": failed,
                                "status": "running",
                            }
                        ).eq("id", job_id).execute()

                finally:
                    try:
                        await page.close()
                        await context.close()
                        await browser.close()
                    except Exception:
                        pass

        asyncio.run(run())

        supabase.table("foreach_url_jobs").update(
            {
                "total": total,
                "processed": processed,
                "success": success,
                "failed": failed,
                "status": "success",
                "finished_at": _now_iso(),
            }
        ).eq("id", job_id).execute()

        logger.info(f"✅ ForeachURL job done: {job_id}, total={total}, success={success}, failed={failed}")

        return {"job_id": job_id, "total": total, "success": success, "failed": failed}

    except Exception as e:
        logger.error(f"❌ ForeachURL job failed: {job_id}: {e}")
        try:
            supabase.table("foreach_url_jobs").update(
                {"status": "failed", "finished_at": _now_iso()}
            ).eq("id", job_id).execute()
        except Exception:
            pass
        raise


