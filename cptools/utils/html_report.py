"""HTML报告生成模块"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict


def generate_html_report(
    results: List[Dict],
    output_path: str,
    title: str = "截屏报告"
):
    """生成HTML报告
    
    Args:
        results: 截图结果列表，每项包含url, name, screenshot_path, status, error等字段
        output_path: 输出HTML文件路径
        title: 报告标题
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 统计信息
    total = len(results)
    success = sum(1 for r in results if r.get('status') == 'success')
    failed = total - success
    
    # 生成HTML
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
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
        
        .header h1 {{
            font-size: 36px;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            font-size: 16px;
            opacity: 0.9;
        }}
        
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
            transition: transform 0.3s ease;
        }}
        
        .summary-card:hover {{
            transform: translateY(-5px);
        }}
        
        .summary-card .number {{
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .summary-card .label {{
            color: #6c757d;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .summary-card.total .number {{ color: #667eea; }}
        .summary-card.success .number {{ color: #28a745; }}
        .summary-card.failed .number {{ color: #dc3545; }}
        
        .results {{
            padding: 40px;
        }}
        
        .results h2 {{
            font-size: 28px;
            margin-bottom: 30px;
            color: #333;
        }}
        
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
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }}
        
        .result-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        }}
        
        .result-card.success {{
            border-color: #28a745;
        }}
        
        .result-card.failed {{
            border-color: #dc3545;
        }}
        
        .result-card .image-container {{
            width: 100%;
            height: 250px;
            background: #f8f9fa;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
        }}
        
        .result-card img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }}
        
        .result-card:hover img {{
            transform: scale(1.05);
        }}
        
        .result-card .error-placeholder {{
            color: #dc3545;
            font-size: 48px;
        }}
        
        .result-card .info {{
            padding: 20px;
        }}
        
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
            text-transform: uppercase;
        }}
        
        .result-card .status.success {{
            background: #d4edda;
            color: #155724;
        }}
        
        .result-card .status.failed {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .result-card .error {{
            margin-top: 12px;
            padding: 12px;
            background: #f8d7da;
            border-left: 4px solid #dc3545;
            border-radius: 4px;
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
        
        @media (max-width: 768px) {{
            .result-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📸 {title}</h1>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
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
"""
    
    # 添加每个结果
    for idx, result in enumerate(results, 1):
        status = result.get('status', 'failed')
        url = result.get('url', '')
        name = result.get('name', f'截图-{idx}')
        screenshot_path = result.get('screenshot_path', '')
        error = result.get('error', '')
        
        # 转换为相对路径（如果截图和HTML在同一父目录下）
        if screenshot_path and Path(screenshot_path).exists():
            try:
                rel_path = Path(screenshot_path).relative_to(Path(output_path).parent)
                img_src = str(rel_path).replace('\\', '/')
            except ValueError:
                img_src = screenshot_path
        else:
            img_src = ''
        
        html_content += f"""
                <div class="result-card {status}">
                    <div class="image-container">
"""
        
        if status == 'success' and img_src:
            html_content += f"""
                        <img src="{img_src}" alt="{name}">
"""
        else:
            html_content += """
                        <div class="error-placeholder">❌</div>
"""
        
        html_content += f"""
                    </div>
                    <div class="info">
                        <div class="name" title="{name}">{name}</div>
                        <div class="url" title="{url}">{url}</div>
                        <span class="status {status}">{status}</span>
"""
        
        if error:
            html_content += f"""
                        <div class="error">{error}</div>
"""
        
        html_content += """
                    </div>
                </div>
"""
    
    html_content += """
            </div>
        </div>
        
        <div class="footer">
            <p>Powered by CPTools | 基于 Playwright 的网页截屏工具</p>
        </div>
    </div>
</body>
</html>
"""
    
    # 写入文件
    output_file.write_text(html_content, encoding='utf-8')
    print(f"HTML报告已生成: {output_path}")

