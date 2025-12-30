"""下载产品主图命令实现"""
import click
import asyncio
import csv
import random
import shutil
import webbrowser
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import sys

from playwright.async_api import async_playwright, Browser
from cptools.utils.logger import setup_logger
from cptools.utils.downloadmips_report import (
    generate_downloadmips_html_report
)
from cptools.utils.dingding import send_dingding_notification


@click.command()
@click.option(
    '--host', '-h', required=True,
    help='主机地址（如: https://www.cafepress.com）')
@click.option(
    '--csv', 'csv_file', required=True, type=click.Path(exists=True),
    help='CSV文件路径，包含产品编号列表（product_no列）')
@click.option(
    '--output', '-o', default='./mips',
    help='图片保存目录（默认：./mips）')
@click.option(
    '--log', '-l', default='',
    help='日志文件路径（默认：./logs/downloadmips_YYYYMMDD_HHMMSS.log）')
@click.option(
    '--html', default='./downloadmips_result.html',
    help='HTML报告输出路径（默认：./downloadmips_result.html）')
@click.option(
    '--concurrency', '-c', default=3, type=int,
    help='并发数量（默认：3，建议不要太大以避免被封）')
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
def downloadmips(host, csv_file, output, log, html, concurrency,
                 dingding_webhook, dingding_secret, no_dingding, timeout):
    """产品主图下载工具

    从CSV文件读取产品编号列表并下载主图。CSV文件应包含以下列：

    \b
    - product_no: 产品编号（必需）

    产品URL格式: {host}/+,{product_no}

    支持的地区：

    \b
    - US: https://www.cafepress.com
    - AU: https://www.cafepress.com.au
    - UK: https://www.cafepress.co.uk
    - CA: https://www.cafepress.ca

    示例：

    \b
    cptools downloadmips --host https://www.cafepress.com \\
        --csv products.csv

    \b
    cptools downloadmips -h https://www.cafepress.com.au \\
        --csv products.csv -c 5
    """
    # 如果没有指定日志文件，自动生成基于时间戳的文件名
    if not log:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log = f'./logs/downloadmips_{timestamp}.log'
        # 确保 logs 目录存在
        Path('./logs').mkdir(parents=True, exist_ok=True)

    # 设置日志
    logger = setup_logger(log)

    logger.info("=" * 80)
    logger.info("开始执行产品主图下载任务")
    logger.info(f"主机地址: {host}")
    logger.info(f"CSV文件: {csv_file}")
    logger.info(f"输出目录: {output}")
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
    products = read_csv_products(csv_file, logger)
    if not products:
        logger.error("CSV文件中没有找到有效的Product No")
        sys.exit(1)

    logger.info(f"从CSV文件中读取到 {len(products)} 个Product No")

    # 清理旧文件
    output_dir = Path(output)
    html_path = Path(html)

    # 删除旧的图片目录
    if output_dir.exists():
        logger.info(f"删除旧的Product No目录: {output_dir}")
        shutil.rmtree(output_dir)

    # 删除旧的HTML报告
    if html_path.exists():
        logger.info(f"删除旧的HTML报告: {html_path}")
        html_path.unlink()

    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"创建新的Product No目录: {output_dir}")

    # 执行下载任务
    start_time = datetime.now()
    results = asyncio.run(
        run_download_tasks(
            products=products,
            host=host,
            output_dir=output_dir,
            concurrency=concurrency,
            timeout=timeout,
            logger=logger
        )
    )
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # 统计结果
    total = len(results)
    success = sum(1 for r in results if r.get('status') == 'success')
    failed = total - success
    total_images = sum(r.get('image_count', 0) for r in results)

    logger.info("=" * 80)
    logger.info("Product MIPs Download Task Completed")
    logger.info("=" * 80)
    logger.info(f"Total Product Count: {total}")
    logger.info(f"Success: {success}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Downloaded Image Count: {total_images}")
    logger.info(f"Duration: {duration:.2f} seconds")
    logger.info("=" * 80)

    # 生成HTML报告
    try:
        generate_downloadmips_html_report(
            results, html, title="Product MIPs Download Report")
        logger.info(f"HTML Report Generated: {html}")

        # 自动在浏览器中打开报告
        try:
            html_abs_path = Path(html).absolute()
            webbrowser.open(f'file://{html_abs_path}')
            logger.info("Report Opened in Browser")
        except Exception as e:
            logger.warning(f"Failed to open browser: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to generate HTML report: {str(e)}")

    # 发送钉钉通知
    if dingding_webhook and not no_dingding:
        try:
            notification_content = f"""### 🖼️ Product MIPs Download Completed

**Time**: {start_time.strftime('%Y-%m-%d %H:%M:%S')}

**Results**: Total {total} | Success {success}✅ | Failed {failed}❌

**Images**: {total_images} downloaded in {duration:.2f}s

**File**: `{csv_file}`
"""
            asyncio.run(
                send_dingding_notification(
                    dingding_webhook,
                    "Product MIPs Download Task Completed",
                    notification_content,
                    secret=dingding_secret
                )
            )
            logger.info("Dingding Notification Sent Successfully")
        except Exception as e:
            logger.error(f"Failed to send Dingding notification: {str(e)}")
    elif no_dingding:
        logger.info("Dingding notification disabled (--no-dingding)")

    # 如果有失败的任务，以非零状态码退出
    if failed > 0:
        sys.exit(1)


def read_csv_products(csv_file: str, logger) -> List[Dict]:
    """Read the list of Product No from the CSV file

    支持的列名（不区分大小写）：
    - product_no/PRODUCT_NO: Product No (Required)
    """
    products = []

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            if not reader.fieldnames:
                logger.error("CSV file is empty or format error")
                return []

            # 创建列名映射（不区分大小写）
            fieldnames_lower = {
                name.lower(): name for name in reader.fieldnames
            }

            # 查找产品编号列
            product_no_column = None
            for possible_name in ['product_no', 'PRODUCT_NO', 'productno',
                                  'product_id', 'PRODUCT_ID']:
                if possible_name.lower() in fieldnames_lower:
                    product_no_column = (
                        fieldnames_lower[possible_name.lower()]
                    )
                    break

            if not product_no_column:
                logger.error(
                    f"CSV file must contain 'product_no' or "
                    f"'PRODUCT_NO' column, "
                    f"Current columns: {', '.join(reader.fieldnames)}"
                )
                return []

            logger.info(f"Using column: PRODUCT_NO='{product_no_column}'")

            for idx, row in enumerate(reader, 1):
                product_no = row.get(product_no_column, '').strip()
                if not product_no:
                    logger.warning(f"Row {idx}: Product No is empty, skipping")
                    continue

                products.append({
                    'product_no': product_no,
                    'index': idx
                })

    except Exception as e:
        logger.error(f"读取CSV文件失败: {str(e)}")
        return []

    return products


async def run_download_tasks(
    products: List[Dict],
    host: str,
    output_dir: Path,
    concurrency: int,
    timeout: int,
    logger
) -> List[Dict]:
    """运行下载任务"""
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
            logger.error(
                "请确保已安装Playwright浏览器: playwright install chromium"
            )
            return []

        try:
            # 创建信号量控制并发
            semaphore = asyncio.Semaphore(concurrency)

            # 创建所有任务
            tasks = []
            for product in products:
                task = download_single_product(
                    browser=browser,
                    product=product,
                    host=host,
                    output_dir=output_dir,
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
                    product_no = products[i]['product_no']
                    processed_results.append({
                        'product_no': product_no,
                        'url': (
                            f"{host}/+,{product_no}"
                        ),
                        'status': 'failed',
                        'error': str(result),
                        'image_count': 0,
                        'images': []
                    })
                else:
                    processed_results.append(result)

            results = processed_results

        finally:
            await browser.close()
            logger.info("浏览器已关闭")

    return results


async def download_single_product(
    browser: Browser,
    product: Dict,
    host: str,
    output_dir: Path,
    timeout: int,
    semaphore: asyncio.Semaphore,
    logger
) -> Dict:
    """下载单个产品的主图"""
    product_no = product['product_no']
    index = product['index']
    url = f"{host}/+,{product_no}"

    async with semaphore:
        logger.info(f"[{index}] 开始处理产品: {product_no}")

        # 创建产品文件夹
        product_dir = output_dir / product_no
        product_dir.mkdir(parents=True, exist_ok=True)

        page = None
        context = None
        try:
            # 随机延迟（模拟人类行为）
            delay = random.uniform(2.0, 4.0)
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

            # 访问页面
            logger.info(f"[{index}] 访问页面: {url}")
            resp = await page.goto(url, wait_until='domcontentloaded')

            # 检查HTTP状态码
            if resp is None or resp.status >= 400:
                error_msg = (
                    f"HTTP {resp.status if resp else 'No Response'}"
                )
                logger.error(f"[{index}] 访问失败: {url} - {error_msg}")
                await context.close()
                return {
                    'product_no': product_no,
                    'url': url,
                    'status': 'failed',
                    'error': error_msg,
                    'image_count': 0,
                    'images': []
                }

            # 等待页面加载
            try:
                await page.wait_for_load_state('networkidle', timeout=5000)
            except Exception:
                logger.debug(f"[{index}] 网络空闲等待超时，继续处理")
                pass

            # 查找所有 class="stackable-image-container" 的 div 下的图片
            logger.info(f"[{index}] 查找产品主图...")
            images = await page.query_selector_all(
                '.stackable-image-container img'
            )

            if not images:
                error_msg = (
                    "未找到产品主图 (class='stackable-image-container')"
                )
                logger.warning(f"[{index}] {error_msg}")
                await context.close()
                return {
                    'product_no': product_no,
                    'url': url,
                    'status': 'failed',
                    'error': error_msg,
                    'image_count': 0,
                    'images': []
                }

            logger.info(f"[{index}] 找到 {len(images)} 张图片")

            # 下载图片
            downloaded_images = []
            for img_idx, img in enumerate(images, 1):
                try:
                    # 获取图片URL
                    img_url = await img.get_attribute('src')
                    if not img_url:
                        logger.warning(
                            f"[{index}] 图片 {img_idx} 没有src属性，跳过"
                        )
                        continue

                    # 如果是相对路径，转为绝对路径
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    elif img_url.startswith('/'):
                        # 使用 host 构建完整 URL
                        img_url = host.rstrip('/') + img_url

                    # 获取文件扩展名
                    ext = '.jpg'
                    if '.png' in img_url.lower():
                        ext = '.png'
                    elif '.gif' in img_url.lower():
                        ext = '.gif'
                    elif '.webp' in img_url.lower():
                        ext = '.webp'

                    # 生成文件名
                    img_filename = f"{product_no}_{img_idx:02d}{ext}"
                    img_path = product_dir / img_filename

                    # 下载图片
                    logger.debug(
                        f"[{index}] 下载图片 {img_idx}: {img_url}"
                    )

                    # 使用 CDP 下载图片（更可靠）
                    img_data = await page.evaluate(f'''
                        async () => {{
                            const response = await fetch("{img_url}");
                            const blob = await response.blob();
                            const reader = new FileReader();
                            return new Promise((resolve) => {{
                                reader.onloadend = () => {{
                                    resolve(reader.result);
                                }};
                                reader.readAsDataURL(blob);
                            }});
                        }}
                    ''')

                    # 解析 base64 数据
                    if img_data and img_data.startswith('data:'):
                        import base64
                        base64_data = img_data.split(',')[1]
                        img_bytes = base64.b64decode(base64_data)

                        # 保存图片
                        with open(img_path, 'wb') as f:
                            f.write(img_bytes)

                        logger.info(
                            f"[{index}] 图片 {img_idx} "
                            f"下载成功: {img_filename}"
                        )
                        downloaded_images.append({
                            'filename': img_filename,
                            'path': str(img_path),
                            'url': img_url
                        })
                    else:
                        logger.warning(
                            f"[{index}] 图片 {img_idx} "
                            f"下载失败: 无效的数据"
                        )

                except Exception as e:
                    logger.error(
                        f"[{index}] 图片 {img_idx} 下载失败: {str(e)}"
                    )
                    continue

            await context.close()

            if downloaded_images:
                logger.info(
                    f"[{index}] 产品 {product_no} 处理完成，"
                    f"下载了 {len(downloaded_images)} 张图片"
                )
                return {
                    'product_no': product_no,
                    'url': url,
                    'status': 'success',
                    'error': '',
                    'image_count': len(downloaded_images),
                    'images': downloaded_images
                }
            else:
                error_msg = "所有图片下载失败"
                logger.warning(f"[{index}] {error_msg}")
                return {
                    'product_no': product_no,
                    'url': url,
                    'status': 'failed',
                    'error': error_msg,
                    'image_count': 0,
                    'images': []
                }

        except Exception as e:
            error_msg = str(e)
            logger.error(
                f"[{index}] 处理失败: {product_no} - {error_msg}"
            )

            if context:
                try:
                    await context.close()
                except Exception:
                    pass

            return {
                'product_no': product_no,
                'url': url,
                'status': 'failed',
                'error': error_msg,
                'image_count': 0,
                'images': []
            }
