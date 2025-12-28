"""HTML报告生成模块 - 简约大气版"""
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
        results: 截图结果列表
        output_path: 输出HTML文件路径
        title: 报告标题
        template: 模板名称（已废弃，保留参数兼容性）
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 统计信息
    total = len(results)
    success = sum(1 for r in results if r.get('status') == 'success')
    failed = total - success
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 生成HTML内容
    html_content = _generate_modern_html(
        results, output_path, title, total, success, failed, timestamp
    )
    
    # 写入文件
    output_file.write_text(html_content, encoding='utf-8')
    print(f"HTML报告已生成: {output_path}")


def _generate_modern_html(
    results: List[Dict],
    output_path: str,
    title: str,
    total: int,
    success: int,
    failed: int,
    timestamp: str
) -> str:
    """生成现代简约风格的HTML"""
    
    # 生成结果卡片
    cards_html = ""
    error_nav_html = ""
    error_count = 0
    
    for idx, result in enumerate(results, 1):
        status = result.get('status', 'failed')
        url = result.get('url', '')
        name = result.get('name', f'截图-{idx}')
        screenshot_path = result.get('screenshot_path', '')
        error = result.get('error', '')
        
        # 转换为相对路径
        if screenshot_path and Path(screenshot_path).exists():
            try:
                output_dir = Path(output_path).parent
                rel_path = Path(screenshot_path).relative_to(output_dir)
                img_src = str(rel_path).replace('\\', '/')
            except ValueError:
                img_src = screenshot_path
        else:
            img_src = ''
        
        # 生成卡片
        cards_html += f'''
            <div class="screenshot-card {'error' if status == 'failed' else ''}" id="item-{idx}">
                <div class="card-image">'''
        
        if status == 'success' and img_src:
            cards_html += f'''
                    <img src="{img_src}" alt="{name}" onclick="openModal({idx - 1})" data-index="{idx - 1}">'''
        else:
            error_count += 1
            cards_html += f'''
                    <div class="error-icon">
                        <svg viewBox="0 0 24 24" width="64" height="64">
                            <path fill="currentColor" d="M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16" />
                        </svg>
                        <p>截图失败</p>
                    </div>'''
        
        cards_html += f'''
                </div>
                <div class="card-info">
                    <h3 class="card-title" title="{name}">{name}</h3>
                    <a href="{url}" class="card-url" target="_blank" title="{url}">{url}</a>
                    <div class="card-status {'success' if status == 'success' else 'error'}">
                        {'✓ 成功' if status == 'success' else '✗ 失败'}
                    </div>'''
        
        if error:
            cards_html += f'''
                    <details class="error-details">
                        <summary>错误详情</summary>
                        <pre>{error}</pre>
                    </details>'''
        
        cards_html += '''
                </div>
            </div>'''
        
        # 错误导航
        if status == 'failed':
            error_nav_html += f'''
                <a href="#item-{idx}" class="error-link">
                    <span class="error-num">{error_count}</span>
                    <span class="error-name">{name}</span>
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
            max-width: 1400px;
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
            max-width: 1400px;
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
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1.5rem;
        }}
        
        .screenshot-card {{
            background: var(--card-bg);
            border-radius: 0.75rem;
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: all 0.3s;
            border: 2px solid transparent;
        }}
        
        .screenshot-card:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
        }}
        
        .screenshot-card.error {{
            border-color: var(--error);
        }}
        
        .card-image {{
            position: relative;
            width: 100%;
            padding-bottom: 75%;
            background: #f1f5f9;
            overflow: hidden;
        }}
        
        .card-image img {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            cursor: pointer;
            transition: transform 0.3s, opacity 0.3s;
        }}
        
        .card-image:hover img {{
            transform: scale(1.05);
            opacity: 0.85;
        }}
        
        .error-icon {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: var(--error);
        }}
        
        .error-icon p {{
            margin-top: 0.5rem;
            font-size: 0.875rem;
        }}
        
        .card-info {{
            padding: 1.25rem;
        }}
        
        .card-title {{
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        
        .card-url {{
            display: block;
            font-size: 0.875rem;
            color: var(--text-light);
            text-decoration: none;
            margin-bottom: 0.75rem;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        
        .card-url:hover {{
            color: var(--primary);
            text-decoration: underline;
        }}
        
        .card-status {{
            display: inline-block;
            padding: 0.375rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .card-status.success {{
            background: #d1fae5;
            color: #065f46;
        }}
        
        .card-status.error {{
            background: #fee2e2;
            color: #991b1b;
        }}
        
        .error-details {{
            margin-top: 0.75rem;
            border-top: 1px solid var(--border);
            padding-top: 0.75rem;
        }}
        
        .error-details summary {{
            cursor: pointer;
            font-size: 0.875rem;
            color: var(--error);
            font-weight: 500;
            user-select: none;
        }}
        
        .error-details pre {{
            margin-top: 0.5rem;
            padding: 0.75rem;
            background: #fef2f2;
            border-radius: 0.375rem;
            font-size: 0.75rem;
            color: #7f1d1d;
            overflow-x: auto;
            line-height: 1.5;
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
            padding: 20px;
            box-sizing: border-box;
        }}
        
        .modal-content {{
            display: block;
            margin: 0 auto;
            max-width: 95%;
            max-height: 90vh;
            width: auto;
            height: auto;
            animation: zoomIn 0.3s;
            cursor: default;
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
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        @keyframes zoomIn {{
            from {{ transform: translate(-50%, -50%) scale(0.8); }}
            to {{ transform: translate(-50%, -50%) scale(1); }}
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
            
            .grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="header-content">
                <div>
                    <h1 class="title">📸 {title}</h1>
                    <p class="timestamp">生成时间: {timestamp}</p>
                </div>
                <div class="stats">
                    <div class="stat">
                        <span class="stat-value">{total}</span>
                        <span class="stat-label">总数</span>
                    </div>
                    <div class="stat">
                        <span class="stat-value">{success}</span>
                        <span class="stat-label">成功</span>
                    </div>
                    <div class="stat">
                        <span class="stat-value">{failed}</span>
                        <span class="stat-label">失败</span>
                    </div>
                </div>
            </div>
        </div>
    </header>
    
    {_generate_error_nav(error_nav_html, failed)}
    
    <main class="content">
        <div class="grid">
            {cards_html}
        </div>
    </main>
    
    <div id="imageModal" class="modal">
        <span class="modal-close" onclick="closeModal()">&times;</span>
        <img class="modal-content" id="modalImage" onclick="event.stopPropagation()">
    </div>
    
    <script>
        let allImages = [];
        let currentImageIndex = 0;
        
        // 初始化图片列表
        document.addEventListener('DOMContentLoaded', () => {{
            allImages = Array.from(document.querySelectorAll('.card-image img[data-index]'))
                .map(img => ({{
                    src: img.src,
                    alt: img.alt,
                    index: parseInt(img.getAttribute('data-index'))
                }}));
        }});
        
        function openModal(index) {{
            const modal = document.getElementById('imageModal');
            const modalImg = document.getElementById('modalImage');
            currentImageIndex = index;
            modal.style.display = 'block';
            modalImg.src = allImages[currentImageIndex].src;
            modalImg.alt = allImages[currentImageIndex].alt;
            event.stopPropagation();
        }}
        
        function closeModal() {{
            document.getElementById('imageModal').style.display = 'none';
        }}
        
        function showPrevImage() {{
            if (allImages.length === 0) return;
            currentImageIndex = (currentImageIndex - 1 + allImages.length) % allImages.length;
            const modalImg = document.getElementById('modalImage');
            modalImg.src = allImages[currentImageIndex].src;
            modalImg.alt = allImages[currentImageIndex].alt;
        }}
        
        function showNextImage() {{
            if (allImages.length === 0) return;
            currentImageIndex = (currentImageIndex + 1) % allImages.length;
            const modalImg = document.getElementById('modalImage');
            modalImg.src = allImages[currentImageIndex].src;
            modalImg.alt = allImages[currentImageIndex].alt;
        }}
        
        document.addEventListener('keydown', (e) => {{
            const modal = document.getElementById('imageModal');
            if (modal.style.display === 'block') {{
                if (e.key === 'Escape') {{
                    closeModal();
                }} else if (e.key === 'ArrowLeft') {{
                    showPrevImage();
                }} else if (e.key === 'ArrowRight') {{
                    showNextImage();
                }}
            }}
        }});
        
        // 点击模态框背景关闭
        document.getElementById('imageModal').addEventListener('click', (e) => {{
            if (e.target.id === 'imageModal') {{
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
