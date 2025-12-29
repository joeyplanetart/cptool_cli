"""产品主图下载报告生成模块"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict


def generate_downloadmips_html_report(
    results: List[Dict],
    output_path: str,
    title: str = "产品主图下载报告"
):
    """生成产品主图下载HTML报告
    
    Args:
        results: 下载结果列表
        output_path: 输出HTML文件路径
        title: 报告标题
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 统计信息
    total = len(results)
    success = sum(1 for r in results if r.get('status') == 'success')
    failed = total - success
    total_images = sum(r.get('image_count', 0) for r in results)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 生成HTML内容
    html_content = _generate_html(
        results, output_path, title, total, success, failed, total_images, timestamp
    )
    
    # 写入文件
    output_file.write_text(html_content, encoding='utf-8')
    print(f"HTML报告已生成: {output_path}")


def _generate_html(
    results: List[Dict],
    output_path: str,
    title: str,
    total: int,
    success: int,
    failed: int,
    total_images: int,
    timestamp: str
) -> str:
    """生成HTML内容"""
    
    # 生成产品行
    rows_html = ""
    error_nav_html = ""
    error_count = 0
    
    for idx, result in enumerate(results, 1):
        status = result.get('status', 'failed')
        product_no = result.get('product_no', '')
        url = result.get('url', '')
        error = result.get('error', '')
        image_count = result.get('image_count', 0)
        images = result.get('images', [])
        
        # 生成缩略图HTML
        thumbnails_html = ""
        if status == 'success' and images:
            for img in images:
                img_path = img.get('path', '')
                img_filename = img.get('filename', '')
                
                # 转换为相对路径
                if img_path and Path(img_path).exists():
                    try:
                        output_dir = Path(output_path).parent
                        rel_path = Path(img_path).relative_to(output_dir)
                        img_src = str(rel_path).replace('\\', '/')
                    except ValueError:
                        img_src = img_path
                else:
                    img_src = ''
                
                if img_src:
                    thumbnails_html += f'''
                        <div class="thumbnail" onclick="openModal('{img_src}', '{img_filename}')">
                            <img src="{img_src}" alt="{img_filename}">
                        </div>'''
        
        # 生成表格行
        status_class = 'success' if status == 'success' else 'error'
        status_text = '✓ 成功' if status == 'success' else '✗ 失败'
        
        rows_html += f'''
            <tr class="product-row {status_class}" id="product-{idx}">
                <td class="product-no">{product_no}</td>
                <td class="url-cell">
                    <a href="{url}" target="_blank" title="{url}">{url}</a>
                </td>
                <td class="status-cell">
                    <span class="status-badge {status_class}">{status_text}</span>
                </td>
                <td class="count-cell">{image_count}</td>
                <td class="images-cell">'''
        
        if status == 'success' and thumbnails_html:
            rows_html += f'''
                    <div class="thumbnails-container">
                        {thumbnails_html}
                    </div>'''
        elif error:
            rows_html += f'''
                    <div class="error-message">
                        <span class="error-icon">⚠️</span>
                        <span>{error}</span>
                    </div>'''
        
        rows_html += '''
                </td>
            </tr>'''
        
        # 错误导航
        if status == 'failed':
            error_count += 1
            error_nav_html += f'''
                <a href="#product-{idx}" class="error-link">
                    <span class="error-num">{error_count}</span>
                    <span class="error-name">{product_no}</span>
                </a>'''
    
    # 生成完整HTML
    return f'''<!DOCTYPE html>
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
        
        :root {{
            --primary: #2563eb;
            --success: #10b981;
            --error: #ef4444;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text: #1e293b;
            --text-light: #64748b;
            --border: #e2e8f0;
            --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            box-shadow: var(--shadow-lg);
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }}
        
        .header-content {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1.5rem;
        }}
        
        .title {{
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        .timestamp {{
            font-size: 0.95rem;
            opacity: 0.9;
        }}
        
        .stats {{
            display: flex;
            gap: 2rem;
        }}
        
        .stat {{
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 2.5rem;
            font-weight: 700;
            display: block;
        }}
        
        .stat-label {{
            font-size: 0.875rem;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .error-nav {{
            background: var(--card-bg);
            margin: 1.5rem auto;
            padding: 1.5rem;
            border-radius: 0.75rem;
            box-shadow: var(--shadow);
            max-width: 1600px;
            margin-left: auto;
            margin-right: auto;
        }}
        
        .error-nav-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--error);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .error-links {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 0.75rem;
        }}
        
        .error-link {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 1rem;
            background: #fef2f2;
            border: 1px solid #fecaca;
            border-radius: 0.5rem;
            text-decoration: none;
            color: var(--text);
            transition: all 0.2s;
        }}
        
        .error-link:hover {{
            background: #fee2e2;
            transform: translateX(4px);
        }}
        
        .error-num {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 2rem;
            height: 2rem;
            background: var(--error);
            color: white;
            border-radius: 50%;
            font-weight: 600;
            font-size: 0.875rem;
            flex-shrink: 0;
        }}
        
        .error-name {{
            flex: 1;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        
        .content {{
            padding: 2rem 1.5rem;
            max-width: 1600px;
            margin: 0 auto;
        }}
        
        .table-container {{
            background: var(--card-bg);
            border-radius: 0.75rem;
            overflow: hidden;
            box-shadow: var(--shadow);
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        thead {{
            background: #f1f5f9;
        }}
        
        thead th {{
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-light);
            border-bottom: 2px solid var(--border);
        }}
        
        tbody tr {{
            border-bottom: 1px solid var(--border);
            transition: background 0.2s;
        }}
        
        tbody tr:hover {{
            background: #f8fafc;
        }}
        
        tbody tr.error {{
            background: #fef2f2;
        }}
        
        tbody tr.error:hover {{
            background: #fee2e2;
        }}
        
        td {{
            padding: 1rem;
            vertical-align: top;
        }}
        
        .product-no {{
            font-weight: 600;
            color: var(--primary);
            font-size: 1rem;
            white-space: nowrap;
        }}
        
        .url-cell a {{
            color: var(--text-light);
            text-decoration: none;
            font-size: 0.875rem;
            display: block;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            max-width: 300px;
        }}
        
        .url-cell a:hover {{
            color: var(--primary);
            text-decoration: underline;
        }}
        
        .status-cell {{
            text-align: center;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 0.375rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .status-badge.success {{
            background: #d1fae5;
            color: #065f46;
        }}
        
        .status-badge.error {{
            background: #fee2e2;
            color: #991b1b;
        }}
        
        .count-cell {{
            text-align: center;
            font-weight: 600;
            font-size: 1.125rem;
            color: var(--primary);
        }}
        
        .images-cell {{
            min-width: 300px;
        }}
        
        .thumbnails-container {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}
        
        .thumbnail {{
            width: 80px;
            height: 80px;
            border-radius: 0.5rem;
            overflow: hidden;
            border: 2px solid var(--border);
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .thumbnail:hover {{
            transform: scale(1.1);
            border-color: var(--primary);
            box-shadow: var(--shadow);
            z-index: 10;
        }}
        
        .thumbnail img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        .error-message {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--error);
            font-size: 0.875rem;
        }}
        
        .error-icon {{
            font-size: 1.25rem;
        }}
        
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            overflow: auto;
            animation: fadeIn 0.2s;
            padding: 40px 20px;
            box-sizing: border-box;
        }}
        
        .modal-content {{
            display: block;
            margin: 0 auto;
            max-width: 90%;
            max-height: 90%;
            animation: zoomIn 0.3s;
        }}
        
        .modal-close {{
            position: absolute;
            top: 1.5rem;
            right: 2rem;
            color: white;
            font-size: 3rem;
            font-weight: 300;
            cursor: pointer;
            z-index: 1001;
            transition: opacity 0.2s;
        }}
        
        .modal-close:hover {{
            opacity: 0.7;
        }}
        
        .modal-filename {{
            position: absolute;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            color: white;
            font-size: 1.125rem;
            background: rgba(0, 0, 0, 0.7);
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            z-index: 1001;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        @keyframes zoomIn {{
            from {{ transform: scale(0.8); }}
            to {{ transform: scale(1); }}
        }}
        
        @media (max-width: 768px) {{
            .header-content {{
                flex-direction: column;
                align-items: flex-start;
            }}
            
            .stats {{
                width: 100%;
                justify-content: space-around;
            }}
            
            .table-container {{
                overflow-x: auto;
            }}
            
            table {{
                min-width: 800px;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="header-content">
                <div>
                    <h1 class="title">🖼️ {title}</h1>
                    <p class="timestamp">生成时间: {timestamp}</p>
                </div>
                <div class="stats">
                    <div class="stat">
                        <span class="stat-value">{total}</span>
                        <span class="stat-label">总产品数</span>
                    </div>
                    <div class="stat">
                        <span class="stat-value">{success}</span>
                        <span class="stat-label">成功</span>
                    </div>
                    <div class="stat">
                        <span class="stat-value">{failed}</span>
                        <span class="stat-label">失败</span>
                    </div>
                    <div class="stat">
                        <span class="stat-value">{total_images}</span>
                        <span class="stat-label">下载图片数</span>
                    </div>
                </div>
            </div>
        </div>
    </header>
    
    {_generate_error_nav(error_nav_html, failed)}
    
    <main class="content">
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>产品编号</th>
                        <th>URL</th>
                        <th>状态</th>
                        <th>图片数</th>
                        <th>预览图</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
    </main>
    
    <div id="imageModal" class="modal">
        <span class="modal-close" onclick="closeModal()">&times;</span>
        <img class="modal-content" id="modalImage">
        <div class="modal-filename" id="modalFilename"></div>
    </div>
    
    <script>
        function openModal(src, filename) {{
            const modal = document.getElementById('imageModal');
            const modalImg = document.getElementById('modalImage');
            const modalFilename = document.getElementById('modalFilename');
            modal.style.display = 'block';
            modalImg.src = src;
            modalFilename.textContent = filename;
            event.stopPropagation();
        }}
        
        function closeModal() {{
            document.getElementById('imageModal').style.display = 'none';
        }}
        
        // 点击模态框背景关闭
        document.getElementById('imageModal').addEventListener('click', (e) => {{
            if (e.target.id === 'imageModal') {{
                closeModal();
            }}
        }});
        
        // ESC键关闭
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') {{
                closeModal();
            }}
        }});
        
        // 平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'center'
                    }});
                    target.style.animation = 'highlight 1s';
                    setTimeout(() => target.style.animation = '', 1000);
                }}
            }});
        }});
        
        const style = document.createElement('style');
        style.textContent = '@keyframes highlight {{ 0%, 100% {{ transform: scale(1); }} 50% {{ transform: scale(1.02); box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.3); }} }}';
        document.head.appendChild(style);
    </script>
</body>
</html>'''


def _generate_error_nav(error_nav_html: str, failed: int) -> str:
    """生成错误导航区域"""
    if not error_nav_html or failed == 0:
        return ''
    
    return f'''
    <nav class="error-nav container">
        <h2 class="error-nav-title">
            <svg viewBox="0 0 24 24" width="24" height="24">
                <path fill="currentColor" d="M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16" />
            </svg>
            失败记录 ({failed} 个) - 点击快速定位
        </h2>
        <div class="error-links">
            {error_nav_html}
        </div>
    </nav>'''

