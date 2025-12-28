"""HTML报告生成模块"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict


def generate_html_report(
    results: List[Dict],
    output_path: str,
    title: str = "截屏报告",
    template: str = "default"
):
    """生成HTML报告
    
    Args:
        results: 截图结果列表，每项包含url, name, screenshot_path, status, error等字段
        output_path: 输出HTML文件路径
        title: 报告标题
        template: 模板名称 (default, terminal, minimal)
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 统计信息
    total = len(results)
    success = sum(1 for r in results if r.get('status') == 'success')
    failed = total - success
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 生成结果HTML
    results_html = _generate_results_html(results, output_path, template)
    
    # 读取模板
    template_path = Path(__file__).parent.parent / 'templates' / f'{template}.html'
    
    if not template_path.exists():
        print(f"警告: 模板 '{template}' 不存在，使用默认模板")
        template_path = Path(__file__).parent.parent / 'templates' / 'default.html'
    
    # 如果模板仍不存在，使用内置模板
    if not template_path.exists():
        html_content = _generate_fallback_html(results, output_path, title, total, success, failed, timestamp)
    else:
        # 读取模板并替换变量
        template_content = template_path.read_text(encoding='utf-8')
        html_content = template_content.replace('{{ title }}', title)
        html_content = html_content.replace('{{ timestamp }}', timestamp)
        html_content = html_content.replace('{{ total }}', str(total))
        html_content = html_content.replace('{{ success }}', str(success))
        html_content = html_content.replace('{{ failed }}', str(failed))
        html_content = html_content.replace('{{ results_html }}', results_html)
    
    # 写入文件
    output_file.write_text(html_content, encoding='utf-8')
    print(f"HTML报告已生成: {output_path}")


def _generate_results_html(results: List[Dict], output_path: str, template: str) -> str:
    """生成结果HTML片段"""
    results_html = ""
    
    for idx, result in enumerate(results, 1):
        status = result.get('status', 'failed')
        url = result.get('url', '')
        name = result.get('name', f'截图-{idx}')
        screenshot_path = result.get('screenshot_path', '')
        error = result.get('error', '')
        
        # 转换为相对路径
        if screenshot_path and Path(screenshot_path).exists():
            try:
                rel_path = Path(screenshot_path).relative_to(Path(output_path).parent)
                img_src = str(rel_path).replace('\\', '/')
            except ValueError:
                img_src = screenshot_path
        else:
            img_src = ''
        
        # 根据模板生成不同的HTML结构
        if template == 'terminal':
            results_html += _generate_terminal_result(status, name, url, img_src, error)
        elif template == 'minimal':
            results_html += _generate_minimal_result(status, name, url, img_src, error)
        else:  # default
            results_html += _generate_default_result(status, name, url, img_src, error)
    
    return results_html


def _generate_default_result(status: str, name: str, url: str, img_src: str, error: str) -> str:
    """生成默认模板的结果项"""
    html = f"""
                <div class="result-card {status}">
                    <div class="image-container">
"""
    
    if status == 'success' and img_src:
        html += f"""
                        <img src="{img_src}" alt="{name}">
"""
    else:
        html += """
                        <div class="error-placeholder">❌</div>
"""
    
    html += f"""
                    </div>
                    <div class="info">
                        <div class="name" title="{name}">{name}</div>
                        <div class="url" title="{url}">{url}</div>
                        <span class="status {status}">{status}</span>
"""
    
    if error:
        html += f"""
                        <div class="error">{error}</div>
"""
    
    html += """
                    </div>
                </div>
"""
    return html


def _generate_terminal_result(status: str, name: str, url: str, img_src: str, error: str) -> str:
    """生成终端模板的结果项"""
    html = f"""
                <div class="result-item {status}">
                    <div class="thumbnail">
"""
    
    if status == 'success' and img_src:
        html += f"""
                        <img src="{img_src}" alt="{name}">
"""
    else:
        html += """
                        <div class="error-icon">✗</div>
"""
    
    html += f"""
                    </div>
                    <div class="info">
                        <div class="name">{name}</div>
                        <div class="url">{url}</div>
"""
    
    if error:
        html += f"""
                        <div class="error">> ERROR: {error}</div>
"""
    
    html += f"""
                    </div>
                    <div class="status {status}">{status}</div>
                </div>
"""
    return html


def _generate_minimal_result(status: str, name: str, url: str, img_src: str, error: str) -> str:
    """生成简约模板的结果项"""
    return _generate_default_result(status, name, url, img_src, error)


def _generate_fallback_html(results: List[Dict], output_path: str, title: str, 
                            total: int, success: int, failed: int, timestamp: str) -> str:
    """生成后备HTML（当模板文件不存在时）"""
    results_html = _generate_results_html(results, output_path, 'default')
    
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 36px; margin-bottom: 10px; font-weight: 700; }}
        .header p {{ font-size: 16px; opacity: 0.9; }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}
        .summary-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .summary-card .number {{ font-size: 48px; font-weight: bold; margin-bottom: 10px; }}
        .summary-card .label {{ color: #6c757d; font-size: 14px; }}
        .summary-card.total .number {{ color: #667eea; }}
        .summary-card.success .number {{ color: #28a745; }}
        .summary-card.failed .number {{ color: #dc3545; }}
        .results {{ padding: 40px; }}
        .results h2 {{ font-size: 28px; margin-bottom: 30px; color: #333; }}
        .result-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
        }}
        .result-card {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border: 2px solid transparent;
        }}
        .result-card.success {{ border-color: #28a745; }}
        .result-card.failed {{ border-color: #dc3545; }}
        .result-card .image-container {{
            width: 100%;
            height: 250px;
            background: #f8f9fa;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}
        .result-card img {{ width: 100%; height: 100%; object-fit: cover; }}
        .result-card .error-placeholder {{ color: #dc3545; font-size: 48px; }}
        .result-card .info {{ padding: 20px; }}
        .result-card .name {{
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .result-card .url {{
            font-size: 14px;
            color: #6c757d;
            margin-bottom: 12px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .result-card .status {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }}
        .result-card .status.success {{ background: #d4edda; color: #155724; }}
        .result-card .status.failed {{ background: #f8d7da; color: #721c24; }}
        .result-card .error {{
            margin-top: 12px;
            padding: 12px;
            background: #f8d7da;
            border-left: 4px solid #dc3545;
            font-size: 13px;
            color: #721c24;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #6c757d;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📸 {title}</h1>
            <p>生成时间: {timestamp}</p>
        </div>
        <div class="summary">
            <div class="summary-card total">
                <div class="number">{total}</div>
                <div class="label">总数</div>
            </div>
            <div class="summary-card success">
                <div class="number">{success}</div>
                <div class="label">成功</div>
            </div>
            <div class="summary-card failed">
                <div class="number">{failed}</div>
                <div class="label">失败</div>
            </div>
        </div>
        <div class="results">
            <h2>详细结果</h2>
            <div class="result-grid">
                {results_html}
            </div>
        </div>
        <div class="footer">
            <p>Powered by CPTools</p>
        </div>
    </div>
</body>
</html>
"""
