"""截屏命令实现"""
import click
import asyncio
import csv
import random
import shutil
import webbrowser
from pathlib import Path
from urllib.parse import urlparse, urljoin
from datetime import datetime
from typing import List, Dict
import sys

from playwright.async_api import async_playwright, Browser
from cptools.utils.logger import setup_logger
from cptools.utils.html_report import generate_html_report
from cptools.utils.dingding import send_dingding_notification


@click.command()
@click.option(
    '--host', '-h', required=True,
    help='默认主机地址（当CSV中的URL没有域名时使用）')
@click.option(
    '--csv', 'csv_file', required=True, type=click.Path(exists=True),
    help='CSV文件路径，包含要截图的URL列表')
@click.option(
    '--output', '-o', default='./screenshots',
    help='截图保存目录（默认：./screenshots）')
@click.option(
    '--log', '-l', default='',
    help='日志文件路径（默认：./logs/YYYYMMDD_HHMMSS.log）')
@click.option(
    '--html', default='./result.html',
    help='HTML报告输出路径（默认：./result.html）')
@click.option(
    '--concurrency', '-c', default=5, type=int,
    help='并发数量（默认：5）')
@click.option(
    '--dingding-webhook',
    default='https://oapi.dingtalk.com/robot/send?access_token='
            'cc51fb8d186b18fd2ee82e24b0d5a810b11ba817de855b98fb3058f4c4e60767',
    help='钉钉机器人Webhook URL（默认已配置）')
@click.option(
    '--timeout', default=30000, type=int,
    help='页面加载超时时间（毫秒，默认：30000）')
@click.option(
    '--width', default=2560, type=int,
    help='浏览器窗口宽度（默认：2560，2K分辨率）')
@click.option(
    '--height', default=1440, type=int,
    help='浏览器窗口高度（默认：1440，2K分辨率）')
@click.option(
    '--template', default='default',
    type=click.Choice(['default', 'terminal', 'minimal']),
    help='HTML报告模板（默认：default）')
def screenshot(host, csv_file, output, log, html, concurrency,
               dingding_webhook, timeout, width, height, template):
    """网页截屏工具

    从CSV文件读取URL列表并进行截图。CSV文件应包含以下列：

    \b
    - url: 页面URL（可以是完整URL或相对路径）
    - name: 截图名称（可选，用于标识）

    示例：

    \b
    cptools screenshot -h http://www.cafepress.com \\
        --csv data.csv -l log.log --html result.html

    \b
    cptools screenshot --host http://example.com \\
        --csv urls.csv --output ./imgs -c 10
    """
    # 如果没有指定日志文件，自动生成基于时间戳的文件名
    if not log:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log = f'./logs/{timestamp}.log'
        # 确保 logs 目录存在
        Path('./logs').mkdir(parents=True, exist_ok=True)

    # 设置日志
    logger = setup_logger(log)

    logger.info("=" * 80)
    logger.info("开始执行截屏任务")
    logger.info(f"主机地址: {host}")
    logger.info(f"CSV文件: {csv_file}")
    logger.info(f"输出目录: {output}")
    logger.info(f"并发数: {concurrency}")
    logger.info(f"超时时间: {timeout}ms")
    logger.info(f"窗口大小: {width}x{height}")
    logger.info(f"报告模板: {template}")
    logger.info("=" * 80)

    # 检查Playwright是否已安装
    try:
        from playwright.async_api import async_playwright  # noqa: F401
    except ImportError:
        logger.error("Playwright未安装，请运行: pip install playwright")
        logger.error("然后运行: playwright install chromium")
        sys.exit(1)

    # 读取CSV文件
    urls = read_csv_urls(csv_file, logger)
    if not urls:
        logger.error("CSV文件中没有找到有效的URL")
        sys.exit(1)

    logger.info(f"从CSV文件中读取到 {len(urls)} 个URL")

    # 清理旧文件
    output_dir = Path(output)
    html_path = Path(html)

    # 删除旧的截图目录
    if output_dir.exists():
        logger.info(f"删除旧的截图目录: {output_dir}")
        shutil.rmtree(output_dir)

    # 删除旧的HTML报告
    if html_path.exists():
        logger.info(f"删除旧的HTML报告: {html_path}")
        html_path.unlink()

    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"创建新的截图目录: {output_dir}")

    # 执行截图任务
    start_time = datetime.now()
    results = asyncio.run(
        run_screenshot_tasks(
            urls=urls,
            host=host,
            output_dir=output_dir,
            concurrency=concurrency,
            timeout=timeout,
            width=width,
            height=height,
            logger=logger
        )
    )
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # 统计结果
    total = len(results)
    success = sum(1 for r in results if r.get('status') == 'success')
    failed = total - success

    logger.info("=" * 80)
    logger.info("截屏任务完成")
    logger.info(f"总数: {total}")
    logger.info(f"成功: {success}")
    logger.info(f"失败: {failed}")
    logger.info(f"耗时: {duration:.2f}秒")
    logger.info("=" * 80)

    # 生成HTML报告
    try:
        generate_html_report(results, html, title="截屏报告",
                             template=template)
        logger.info(f"HTML报告已生成: {html}")
        
        # 自动在浏览器中打开报告
        try:
            html_abs_path = Path(html).absolute()
            webbrowser.open(f'file://{html_abs_path}')
            logger.info("已在浏览器中打开报告")
        except Exception as e:
            logger.warning(f"自动打开浏览器失败: {str(e)}")
    except Exception as e:
        logger.error(f"生成HTML报告失败: {str(e)}")

    # 发送钉钉通知
    if dingding_webhook:
        try:
            notification_content = f"""### 📸 截屏任务完成

**执行时间**: {start_time.strftime('%Y-%m-%d %H:%M:%S')}

**执行结果**:
- 总数: {total}
- 成功: {success} ✅
- 失败: {failed} ❌
- 耗时: {duration:.2f}秒

**主机地址**: {host}

**CSV文件**: {csv_file}
"""
            asyncio.run(
                send_dingding_notification(
                    dingding_webhook,
                    "截屏任务完成",
                    notification_content
                )
            )
        except Exception as e:
            logger.error(f"发送钉钉通知失败: {str(e)}")

    # 如果有失败的任务，以非零状态码退出
    if failed > 0:
        sys.exit(1)


def read_csv_urls(csv_file: str, logger) -> List[Dict]:
    """读取CSV文件中的URL列表

    支持的列名（不区分大小写）：
    - url/URL: URL地址（必需）
    - name/PRODUCT_ID: 截图名称（可选）
    """
    urls = []

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            if not reader.fieldnames:
                logger.error("CSV文件为空或格式错误")
                return []

            # 创建列名映射（不区分大小写）
            fieldnames_lower = {
                name.lower(): name for name in reader.fieldnames
            }

            # 查找URL列
            url_column = None
            for possible_name in ['url', 'URL']:
                if possible_name.lower() in fieldnames_lower:
                    url_column = fieldnames_lower[possible_name.lower()]
                    break

            if not url_column:
                logger.error(
                    f"CSV文件必须包含'url'或'URL'列，"
                    f"当前列: {', '.join(reader.fieldnames)}"
                )
                return []

            # 查找名称列（优先级：name > PRODUCT_ID）
            name_column = None
            for possible_name in ['name', 'PRODUCT_ID', 'product_id',
                                  'title', 'TITLE']:
                if possible_name.lower() in fieldnames_lower:
                    name_column = fieldnames_lower[possible_name.lower()]
                    break

            logger.info(
                f"使用列: URL='{url_column}', "
                f"NAME='{name_column or '(自动生成)'}'")

            for idx, row in enumerate(reader, 1):
                url = row.get(url_column, '').strip()
                if not url:
                    logger.warning(f"第{idx}行: URL为空，跳过")
                    continue

                # 获取名称
                if name_column:
                    name = (row.get(name_column, '').strip() or
                            f'screenshot-{idx}')
                else:
                    name = f'screenshot-{idx}'

                urls.append({
                    'url': url,
                    'name': name,
                    'index': idx
                })

    except Exception as e:
        logger.error(f"读取CSV文件失败: {str(e)}")
        return []

    return urls


async def run_screenshot_tasks(
    urls: List[Dict],
    host: str,
    output_dir: Path,
    concurrency: int,
    timeout: int,
    width: int,
    height: int,
    logger
) -> List[Dict]:
    """运行截图任务"""
    results = []

    async with async_playwright() as p:
        # 启动浏览器 - 添加反爬虫和性能优化参数
        try:
            # 轻量级浏览器启动参数
            # （针对低配置服务器优化 + 反爬虫）
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
            logger.info("浏览器启动成功（已启用反爬虫优化）")
        except Exception as e:
            logger.error(f"启动浏览器失败: {str(e)}")
            logger.error("请确保已安装Playwright浏览器: playwright install chromium")
            return []

        try:
            # 创建信号量控制并发
            semaphore = asyncio.Semaphore(concurrency)

            # 创建所有任务
            tasks = []
            for url_info in urls:
                task = screenshot_single_page(
                    browser=browser,
                    url_info=url_info,
                    host=host,
                    output_dir=output_dir,
                    timeout=timeout,
                    width=width,
                    height=height,
                    semaphore=semaphore,
                    logger=logger
                )
                tasks.append(task)

            # 并发执行所有任务
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # 处理异常结果
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    processed_results.append({
                        'url': urls[i]['url'],
                        'name': urls[i]['name'],
                        'status': 'failed',
                        'error': str(result)
                    })
                else:
                    processed_results.append(result)

            results = processed_results

        finally:
            await browser.close()
            logger.info("浏览器已关闭")

    return results


async def screenshot_single_page(
    browser: Browser,
    url_info: Dict,
    host: str,
    output_dir: Path,
    timeout: int,
    width: int,
    height: int,
    semaphore: asyncio.Semaphore,
    logger
) -> Dict:
    """截取单个页面"""
    url = url_info['url']
    name = url_info['name']
    index = url_info['index']

    async with semaphore:
        # 构建完整URL
        full_url = build_full_url(url, host)

        logger.info(f"[{index}] 开始截图: {full_url}")

        # 生成安全的文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = "".join(
            c for c in name if c.isalnum() or c in (' ', '-', '_')
        ).strip()
        safe_name = safe_name or f'screenshot-{index}'
        filename = f"{safe_name}_{timestamp}.png"
        screenshot_path = output_dir / filename

        page = None
        context = None
        try:
            # 🔥 反爬虫机制1: 随机延迟（模拟人类行为）
            delay = random.uniform(1.5, 3.5)
            logger.debug(f"[{index}] 随机延迟 {delay:.2f} 秒")
            await asyncio.sleep(delay)

            # 🔥 反爬虫机制2: 轻量级上下文配置 + 真实浏览器特征
            # 高清晰度设置：启用设备像素比 (device_scale_factor)
            context = await browser.new_context(
                viewport={'width': width, 'height': height},
                device_scale_factor=2,  # 2x DPI，提高截图清晰度
                user_agent=(
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/120.0.0.0 Safari/537.36'
                ),
                locale='en-US',
                ignore_https_errors=True,  # 忽略 HTTPS 错误
            )

            page = await context.new_page()

            # 设置超时
            page.set_default_navigation_timeout(timeout)
            page.set_default_timeout(timeout)

            # 🔥 反爬虫机制3: 使用 domcontentloaded 而不是完全加载
            # （更快，更像真实浏览）
            resp = await page.goto(full_url,
                                   wait_until='domcontentloaded')

            # 🔥 反爬虫机制4: 尝试等待网络空闲，但不强制
            # （避免超时）
            try:
                await page.wait_for_load_state('networkidle',
                                               timeout=3000)
            except Exception:
                # 超时不影响截图，继续执行
                logger.debug(f"[{index}] 网络空闲等待超时，继续截图")
                pass

            # 检查 HTTP 状态码
            if resp is not None and resp.status >= 400:
                error_msg = f"HTTP {resp.status}"
                logger.warning(
                    f"[{index}] HTTP 错误: {full_url} - {error_msg}")
                await context.close()
                return {
                    'url': full_url,
                    'name': name,
                    'screenshot_path': '',
                    'status': 'failed',
                    'error': error_msg
                }

            # 🔥 反爬虫机制5: 使用 JPEG 格式 + 降低质量（更快）
            # 但保持 PNG 格式以确保质量（根据需求调整）
            await page.screenshot(path=str(screenshot_path),
                                  full_page=True)

            logger.info(f"[{index}] 截图成功: {full_url}")

            await context.close()

            return {
                'url': full_url,
                'name': name,
                'screenshot_path': str(screenshot_path),
                'status': 'success',
                'error': ''
            }

        except Exception as e:
            error_msg = str(e)
            logger.error(f"[{index}] 截图失败: {full_url} - {error_msg}")

            if context:
                try:
                    await context.close()
                except Exception:
                    pass

            return {
                'url': full_url,
                'name': name,
                'screenshot_path': '',
                'status': 'failed',
                'error': error_msg
            }


def build_full_url(url: str, host: str) -> str:
    """构建完整URL

    如果URL已经包含域名，直接使用；否则使用提供的host
    """
    url = url.strip()

    # 检查是否已经是完整URL
    parsed = urlparse(url)
    if parsed.scheme and parsed.netloc:
        return url

    # 如果是相对路径，与host组合
    if not url.startswith('/'):
        url = '/' + url

    return urljoin(host, url)
