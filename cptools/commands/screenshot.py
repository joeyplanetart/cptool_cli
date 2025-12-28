"""截屏命令实现"""
import click
import asyncio
import csv
from pathlib import Path
from urllib.parse import urlparse, urljoin
from datetime import datetime
from typing import List, Dict, Optional
import sys

from playwright.async_api import async_playwright, Browser, Page
from cptools.utils.logger import setup_logger
from cptools.utils.html_report import generate_html_report
from cptools.utils.dingding import send_dingding_notification


@click.command()
@click.option('--host', '-h', required=True, help='默认主机地址（当CSV中的URL没有域名时使用）')
@click.option('--csv', 'csv_file', required=True, type=click.Path(exists=True), help='CSV文件路径，包含要截图的URL列表')
@click.option('--output', '-o', default='./screenshots', help='截图保存目录（默认：./screenshots）')
@click.option('--log', '-l', default='./screenshot.log', help='日志文件路径（默认：./screenshot.log）')
@click.option('--html', default='./result.html', help='HTML报告输出路径（默认：./result.html）')
@click.option('--concurrency', '-c', default=5, type=int, help='并发数量（默认：5）')
@click.option('--dingding-webhook', default='', help='钉钉机器人Webhook URL（可选）')
@click.option('--timeout', default=30000, type=int, help='页面加载超时时间（毫秒，默认：30000）')
@click.option('--width', default=1920, type=int, help='浏览器窗口宽度（默认：1920）')
@click.option('--height', default=1080, type=int, help='浏览器窗口高度（默认：1080）')
@click.option('--template', default='default', type=click.Choice(['default', 'terminal', 'minimal']), help='HTML报告模板（默认：default）')
def screenshot(host, csv_file, output, log, html, concurrency, dingding_webhook, timeout, width, height, template):
    """网页截屏工具
    
    从CSV文件读取URL列表并进行截图。CSV文件应包含以下列：
    
    \b
    - url: 页面URL（可以是完整URL或相对路径）
    - name: 截图名称（可选，用于标识）
    
    示例：
    
    \b
    cptools screenshot -h http://www.cafepress.com --csv data.csv -l log.log --html result.html
    
    \b
    cptools screenshot --host http://example.com --csv urls.csv --output ./imgs -c 10
    """
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
        from playwright.async_api import async_playwright
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
    
    # 创建输出目录
    output_dir = Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
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
        generate_html_report(results, html, title="截屏报告", template=template)
        logger.info(f"HTML报告已生成: {html} (模板: {template})")
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
            fieldnames_lower = {name.lower(): name for name in reader.fieldnames}
            
            # 查找URL列
            url_column = None
            for possible_name in ['url', 'URL']:
                if possible_name.lower() in fieldnames_lower:
                    url_column = fieldnames_lower[possible_name.lower()]
                    break
            
            if not url_column:
                logger.error(f"CSV文件必须包含'url'或'URL'列，当前列: {', '.join(reader.fieldnames)}")
                return []
            
            # 查找名称列（优先级：name > PRODUCT_ID）
            name_column = None
            for possible_name in ['name', 'PRODUCT_ID', 'product_id', 'title', 'TITLE']:
                if possible_name.lower() in fieldnames_lower:
                    name_column = fieldnames_lower[possible_name.lower()]
                    break
            
            logger.info(f"使用列: URL='{url_column}', NAME='{name_column or '(自动生成)'}'")
            
            for idx, row in enumerate(reader, 1):
                url = row.get(url_column, '').strip()
                if not url:
                    logger.warning(f"第{idx}行: URL为空，跳过")
                    continue
                
                # 获取名称
                if name_column:
                    name = row.get(name_column, '').strip() or f'screenshot-{idx}'
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
        # 启动浏览器
        try:
            browser = await p.chromium.launch(headless=True)
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
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name or f'screenshot-{index}'
        filename = f"{safe_name}_{timestamp}.png"
        screenshot_path = output_dir / filename
        
        page = None
        try:
            # 创建新页面
            context = await browser.new_context(
                viewport={'width': width, 'height': height},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = await context.new_page()
            
            # 导航到页面
            await page.goto(full_url, timeout=timeout, wait_until='networkidle')
            
            # 等待一小段时间确保页面完全渲染
            await asyncio.sleep(1)
            
            # 截图
            await page.screenshot(path=str(screenshot_path), full_page=True)
            
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
            
            if page:
                try:
                    await page.context.close()
                except:
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

