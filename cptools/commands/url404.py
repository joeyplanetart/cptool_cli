"""URL 404检测命令实现"""
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
from cptools.utils.url404_report import generate_url404_html_report
from cptools.utils.dingding import send_dingding_notification


@click.command()
@click.option(
    '--host', '-h', required=True,
    help='默认主机地址（当CSV中的URL没有域名时使用）')
@click.option(
    '--csv', 'csv_file', required=True, type=click.Path(exists=True),
    help='CSV文件路径，包含要检测的URL列表')
@click.option(
    '--log', '-l', default='',
    help='日志文件路径（默认：./logs/url404_YYYYMMDD_HHMMSS.log）')
@click.option(
    '--html', default='./url404_result.html',
    help='HTML报告输出路径（默认：./url404_result.html）')
@click.option(
    '--concurrency', '-c', default=5, type=int,
    help='并发数量（默认：5）')
@click.option(
    '--dingding-webhook',
    default='https://oapi.dingtalk.com/robot/send?access_token='
            'ce631c399761d21df6460018238a6fd22c237e3feb7021c580f34967c9a6e951',
    help='钉钉机器人Webhook URL（默认已配置）')
@click.option(
    '--dingding-secret',
    default='SECdc9d0205aebf46618039a4bf770cb69ed87173bc7270cead292136c1'
            '4287708f',
    help='钉钉机器人签名密钥（默认已配置）')
@click.option(
    '--no-dingding', is_flag=True, default=False,
    help='禁用钉钉通知（调试时使用）')
@click.option(
    '--timeout', default=30000, type=int,
    help='页面加载超时时间（毫秒，默认：30000）')
def url404(host, csv_file, log, html, concurrency,
           dingding_webhook, dingding_secret, no_dingding, timeout):
    """URL 404/500错误检测工具

    从CSV文件读取URL列表并检测状态码。CSV文件应包含以下列：

    \b
    - url: 页面URL（可以是完整URL或相对路径）
    - name: URL名称（可选，用于标识）

    示例：

    \b
    cptools url404 -h http://www.cafepress.com \\
        --csv test_10.csv -l log.log --html url404_result.html

    \b
    cptools url404 --host http://example.com \\
        --csv urls.csv -c 10
    """
    # 如果没有指定日志文件，自动生成基于时间戳的文件名
    if not log:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log = f'./logs/url404_{timestamp}.log'
        # 确保 logs 目录存在
        Path('./logs').mkdir(parents=True, exist_ok=True)

    # 设置日志
    logger = setup_logger(log)

    logger.info("=" * 80)
    logger.info("开始执行URL 404检测任务")
    logger.info(f"主机地址: {host}")
    logger.info(f"CSV文件: {csv_file}")
    logger.info(f"并发数: {concurrency}")
    logger.info(f"超时时间: {timeout}ms")
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

    # 删除旧的HTML报告
    html_path = Path(html)
    if html_path.exists():
        logger.info(f"删除旧的HTML报告: {html_path}")
        html_path.unlink()

    # 执行检测任务
    start_time = datetime.now()
    results = asyncio.run(
        run_url404_tasks(
            urls=urls,
            host=host,
            concurrency=concurrency,
            timeout=timeout,
            logger=logger
        )
    )
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # 统计结果
    total = len(results)
    success = sum(1 for r in results if r.get('status_code') and 200 <= r.get('status_code') < 400)
    error_404 = sum(1 for r in results if r.get('status_code') == 404)
    error_500 = sum(1 for r in results if r.get('status_code') and r.get('status_code') >= 500)
    other_errors = total - success - error_404 - error_500

    logger.info("=" * 80)
    logger.info("URL 404检测任务完成")
    logger.info(f"总数: {total}")
    logger.info(f"成功(2xx-3xx): {success}")
    logger.info(f"404错误: {error_404}")
    logger.info(f"500错误: {error_500}")
    logger.info(f"其他错误: {other_errors}")
    logger.info(f"耗时: {duration:.2f}秒")
    logger.info("=" * 80)

    # 生成HTML报告
    try:
        generate_url404_html_report(results, html, title="URL 404检测报告")
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
    if dingding_webhook and not no_dingding:
        try:
            notification_content = f"""### 🔍 URL 404 Check Completed

**Time**: {start_time.strftime('%Y-%m-%d %H:%M:%S')}

**Results**: Total {total} | OK {success}✅ | 404 {error_404}⚠️ | 500+ {error_500}❌

**Duration**: {duration:.2f}s

**Host**: `{host}`

**File**: `{csv_file}`
"""
            asyncio.run(
                send_dingding_notification(
                    dingding_webhook,
                    "URL 404 Check Completed",
                    notification_content,
                    secret=dingding_secret
                )
            )
            logger.info("钉钉通知发送成功")
        except Exception as e:
            logger.error(f"发送钉钉通知失败: {str(e)}")
    elif no_dingding:
        logger.info("已禁用钉钉通知（--no-dingding）")

    # 如果有失败的任务，以非零状态码退出
    if error_404 + error_500 + other_errors > 0:
        sys.exit(1)


def read_csv_urls(csv_file: str, logger) -> List[Dict]:
    """读取CSV文件中的URL列表

    支持的列名（不区分大小写）：
    - url/URL: URL地址（必需）
    - name/PRODUCT_ID: URL名称（可选）
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
                            f'url-{idx}')
                else:
                    name = f'url-{idx}'

                urls.append({
                    'url': url,
                    'name': name,
                    'index': idx
                })

    except Exception as e:
        logger.error(f"读取CSV文件失败: {str(e)}")
        return []

    return urls


async def run_url404_tasks(
    urls: List[Dict],
    host: str,
    concurrency: int,
    timeout: int,
    logger
) -> List[Dict]:
    """运行URL检测任务"""
    results = []

    async with async_playwright() as p:
        # 启动浏览器
        try:
            launch_args = [
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-setuid-sandbox',
                '--disable-gpu',
                '--disable-software-rasterizer',
                '--disable-extensions',
                '--disable-background-networking',
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
            logger.info("浏览器启动成功")
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
                task = check_single_url(
                    browser=browser,
                    url_info=url_info,
                    host=host,
                    timeout=timeout,
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
                        'status_code': None,
                        'status_text': 'Exception',
                        'error': str(result)
                    })
                else:
                    processed_results.append(result)

            results = processed_results

        finally:
            await browser.close()
            logger.info("浏览器已关闭")

    return results


async def check_single_url(
    browser: Browser,
    url_info: Dict,
    host: str,
    timeout: int,
    semaphore: asyncio.Semaphore,
    logger
) -> Dict:
    """检测单个URL的状态码"""
    url = url_info['url']
    name = url_info['name']
    index = url_info['index']

    async with semaphore:
        # 构建完整URL
        full_url = build_full_url(url, host)

        logger.info(f"[{index}] 开始检测: {full_url}")

        page = None
        context = None
        try:
            # 随机延迟（模拟人类行为）
            delay = random.uniform(1.0, 2.5)
            logger.debug(f"[{index}] 随机延迟 {delay:.2f} 秒")
            await asyncio.sleep(delay)

            # 创建上下文
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent=(
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/120.0.0.0 Safari/537.36'
                ),
                locale='en-US',
                ignore_https_errors=True,
            )

            page = await context.new_page()

            # 设置超时
            page.set_default_navigation_timeout(timeout)
            page.set_default_timeout(timeout)

            # 访问页面并获取响应
            resp = await page.goto(full_url, wait_until='domcontentloaded')

            # 获取状态码
            status_code = resp.status if resp else None
            status_text = resp.status_text if resp else 'No Response'

            # 判断状态
            if status_code is None:
                error_msg = "无法获取响应"
                logger.warning(f"[{index}] {error_msg}: {full_url}")
            elif status_code == 404:
                error_msg = "页面不存在(404)"
                logger.warning(f"[{index}] {error_msg}: {full_url}")
            elif status_code >= 500:
                error_msg = f"服务器错误({status_code})"
                logger.error(f"[{index}] {error_msg}: {full_url}")
            elif status_code >= 400:
                error_msg = f"客户端错误({status_code})"
                logger.warning(f"[{index}] {error_msg}: {full_url}")
            else:
                error_msg = ""
                logger.info(f"[{index}] 检测成功 [{status_code}]: {full_url}")

            await context.close()

            return {
                'url': full_url,
                'name': name,
                'status_code': status_code,
                'status_text': status_text,
                'error': error_msg
            }

        except Exception as e:
            error_msg = str(e)
            logger.error(f"[{index}] 检测失败: {full_url} - {error_msg}")

            if context:
                try:
                    await context.close()
                except Exception:
                    pass

            return {
                'url': full_url,
                'name': name,
                'status_code': None,
                'status_text': 'Error',
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

