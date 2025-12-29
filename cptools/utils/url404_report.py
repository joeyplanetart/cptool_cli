"""URL 404检测HTML报告生成模块 - 列表样式"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict


def generate_url404_html_report(
    results: List[Dict],
    output_path: str,
    title: str = "URL 404检测报告"
):
    """生成URL 404检测HTML报告
    
    Args:
        results: 检测结果列表
        output_path: 输出HTML文件路径
        title: 报告标题
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 统计信息
    total = len(results)
    success = sum(1 for r in results if r.get('status_code') and 200 <= r.get('status_code') < 400)
    error_404 = sum(1 for r in results if r.get('status_code') == 404)
    error_500 = sum(1 for r in results if r.get('status_code') and r.get('status_code') >= 500)
    other_errors = total - success - error_404 - error_500
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 生成HTML内容
    html_content = _generate_list_html(
        results, title, total, success, error_404, error_500, other_errors, timestamp
    )
    
    # 写入文件
    output_file.write_text(html_content, encoding='utf-8')
    print(f"HTML报告已生成: {output_path}")


def _get_status_category(status_code):
    """获取状态码分类"""
    if status_code is None:
        return 'error'
    elif 200 <= status_code < 400:
        return 'success'
    elif status_code == 404:
        return 'warning'
    elif status_code >= 500:
        return 'error'
    else:
        return 'warning'


def _get_status_icon(status_code):
    """获取状态图标"""
    category = _get_status_category(status_code)
    if category == 'success':
        return '✓'
    elif category == 'warning':
        return '⚠'
    else:
        return '✗'


def _generate_list_html(
    results: List[Dict],
    title: str,
    total: int,
    success: int,
    error_404: int,
    error_500: int,
    other_errors: int,
    timestamp: str
) -> str:
    """生成列表样式的HTML"""
    
    # 生成表格行
    table_rows = ""
    for idx, result in enumerate(results, 1):
        status_code = result.get('status_code')
        url = result.get('url', '')
        name = result.get('name', f'URL-{idx}')
        status_text = result.get('status_text', '')
        error = result.get('error', '')
        
        category = _get_status_category(status_code)
        icon = _get_status_icon(status_code)
        
        # 状态码显示
        if status_code is None:
            status_display = f'<span class="status-badge status-error">ERROR</span>'
        else:
            status_display = f'<span class="status-badge status-{category}">{status_code}</span>'
        
        # 错误信息
        error_display = ''
        if error:
            error_display = f'''
                <div class="error-message">
                    <svg class="error-icon" viewBox="0 0 20 20" width="16" height="16">
                        <path fill="currentColor" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"/>
                    </svg>
                    {error}
                </div>'''
        
        table_rows += f'''
            <tr class="table-row status-{category}">
                <td class="col-index">{idx}</td>
                <td class="col-name">
                    <div class="name-wrapper">
                        <span class="status-icon">{icon}</span>
                        <span class="name-text" title="{name}">{name}</span>
                    </div>
                </td>
                <td class="col-url">
                    <a href="{url}" target="_blank" class="url-link" title="{url}">{url}</a>
                </td>
                <td class="col-status">{status_display}</td>
                <td class="col-message">
                    <span class="status-text">{status_text}</span>
                    {error_display}
                </td>
            </tr>'''
    
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
            --warning: #f59e0b;
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
            min-height: 100vh;
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
            gap: 2rem;
        }}
        
        .title-section {{
            flex: 1;
            min-width: 300px;
        }}
        
        .title {{
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        
        .timestamp {{
            font-size: 0.95rem;
            opacity: 0.9;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 1.5rem;
            min-width: 600px;
        }}
        
        .stat {{
            text-align: center;
            padding: 0.75rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 0.5rem;
            backdrop-filter: blur(10px);
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            display: block;
            margin-bottom: 0.25rem;
        }}
        
        .stat-label {{
            font-size: 0.75rem;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .content {{
            padding: 2rem 1.5rem;
            max-width: 1600px;
            margin: 0 auto;
        }}
        
        .table-container {{
            background: var(--card-bg);
            border-radius: 0.75rem;
            box-shadow: var(--shadow);
            overflow: hidden;
        }}
        
        .table-wrapper {{
            overflow-x: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        thead {{
            background: #f1f5f9;
            border-bottom: 2px solid var(--border);
        }}
        
        th {{
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text);
        }}
        
        .table-row {{
            border-bottom: 1px solid var(--border);
            transition: background-color 0.2s;
        }}
        
        .table-row:hover {{
            background: #f8fafc;
        }}
        
        .table-row.status-success {{
            background: rgba(16, 185, 129, 0.03);
        }}
        
        .table-row.status-warning {{
            background: rgba(245, 158, 11, 0.05);
        }}
        
        .table-row.status-error {{
            background: rgba(239, 68, 68, 0.05);
        }}
        
        td {{
            padding: 1rem;
            font-size: 0.875rem;
        }}
        
        .col-index {{
            width: 60px;
            text-align: center;
            font-weight: 600;
            color: var(--text-light);
        }}
        
        .col-name {{
            width: 20%;
            min-width: 150px;
        }}
        
        .name-wrapper {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .status-icon {{
            font-size: 1.25rem;
            font-weight: bold;
            flex-shrink: 0;
        }}
        
        .status-success .status-icon {{
            color: var(--success);
        }}
        
        .status-warning .status-icon {{
            color: var(--warning);
        }}
        
        .status-error .status-icon {{
            color: var(--error);
        }}
        
        .name-text {{
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            font-weight: 500;
        }}
        
        .col-url {{
            width: 35%;
            min-width: 250px;
        }}
        
        .url-link {{
            color: var(--primary);
            text-decoration: none;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            display: block;
        }}
        
        .url-link:hover {{
            text-decoration: underline;
        }}
        
        .col-status {{
            width: 100px;
            text-align: center;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 0.375rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .status-badge.status-success {{
            background: #d1fae5;
            color: #065f46;
        }}
        
        .status-badge.status-warning {{
            background: #fef3c7;
            color: #92400e;
        }}
        
        .status-badge.status-error {{
            background: #fee2e2;
            color: #991b1b;
        }}
        
        .col-message {{
            width: 25%;
            min-width: 200px;
        }}
        
        .status-text {{
            color: var(--text-light);
            font-size: 0.875rem;
        }}
        
        .error-message {{
            margin-top: 0.5rem;
            padding: 0.5rem;
            background: #fef2f2;
            border-left: 3px solid var(--error);
            border-radius: 0.25rem;
            font-size: 0.75rem;
            color: #7f1d1d;
            display: flex;
            align-items: flex-start;
            gap: 0.5rem;
        }}
        
        .error-icon {{
            flex-shrink: 0;
            margin-top: 0.125rem;
        }}
        
        .filter-bar {{
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
            align-items: center;
        }}
        
        .filter-btn {{
            padding: 0.5rem 1rem;
            border: 2px solid var(--border);
            background: var(--card-bg);
            border-radius: 0.5rem;
            cursor: pointer;
            font-size: 0.875rem;
            font-weight: 500;
            transition: all 0.2s;
        }}
        
        .filter-btn:hover {{
            border-color: var(--primary);
            color: var(--primary);
        }}
        
        .filter-btn.active {{
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }}
        
        .filter-btn.success.active {{
            background: var(--success);
            border-color: var(--success);
        }}
        
        .filter-btn.warning.active {{
            background: var(--warning);
            border-color: var(--warning);
        }}
        
        .filter-btn.error.active {{
            background: var(--error);
            border-color: var(--error);
        }}
        
        .search-box {{
            flex: 1;
            min-width: 250px;
            position: relative;
        }}
        
        .search-input {{
            width: 100%;
            padding: 0.5rem 1rem 0.5rem 2.5rem;
            border: 2px solid var(--border);
            border-radius: 0.5rem;
            font-size: 0.875rem;
            transition: border-color 0.2s;
        }}
        
        .search-input:focus {{
            outline: none;
            border-color: var(--primary);
        }}
        
        .search-icon {{
            position: absolute;
            left: 0.75rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-light);
        }}
        
        @media (max-width: 1024px) {{
            .stats {{
                grid-template-columns: repeat(3, 1fr);
                min-width: auto;
            }}
            
            .header-content {{
                flex-direction: column;
                align-items: stretch;
            }}
        }}
        
        @media (max-width: 768px) {{
            .stats {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .title {{
                font-size: 1.5rem;
            }}
            
            .filter-bar {{
                flex-direction: column;
            }}
            
            .filter-btn {{
                width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="header-content">
                <div class="title-section">
                    <h1 class="title">
                        🔍 {title}
                    </h1>
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
                        <span class="stat-value">{error_404}</span>
                        <span class="stat-label">404</span>
                    </div>
                    <div class="stat">
                        <span class="stat-value">{error_500}</span>
                        <span class="stat-label">500+</span>
                    </div>
                    <div class="stat">
                        <span class="stat-value">{other_errors}</span>
                        <span class="stat-label">其他错误</span>
                    </div>
                </div>
            </div>
        </div>
    </header>
    
    <main class="content">
        <div class="filter-bar">
            <button class="filter-btn active" onclick="filterStatus('all')">全部 ({total})</button>
            <button class="filter-btn success" onclick="filterStatus('success')">成功 ({success})</button>
            <button class="filter-btn warning" onclick="filterStatus('warning')">404 ({error_404})</button>
            <button class="filter-btn error" onclick="filterStatus('error')">错误 ({error_500 + other_errors})</button>
            <div class="search-box">
                <svg class="search-icon" width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
                </svg>
                <input type="text" class="search-input" placeholder="搜索 URL 或名称..." oninput="searchTable(this.value)">
            </div>
        </div>
        
        <div class="table-container">
            <div class="table-wrapper">
                <table id="resultsTable">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>名称</th>
                            <th>URL</th>
                            <th>状态码</th>
                            <th>状态信息</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </div>
        </div>
    </main>
    
    <script>
        let currentFilter = 'all';
        
        function filterStatus(status) {{
            currentFilter = status;
            
            // 更新按钮状态
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // 过滤表格行
            const rows = document.querySelectorAll('.table-row');
            rows.forEach(row => {{
                if (status === 'all') {{
                    row.style.display = '';
                }} else {{
                    if (row.classList.contains('status-' + status)) {{
                        row.style.display = '';
                    }} else {{
                        row.style.display = 'none';
                    }}
                }}
            }});
            
            // 重新应用搜索过滤
            const searchValue = document.querySelector('.search-input').value;
            if (searchValue) {{
                searchTable(searchValue);
            }}
        }}
        
        function searchTable(value) {{
            const searchTerm = value.toLowerCase();
            const rows = document.querySelectorAll('.table-row');
            
            rows.forEach(row => {{
                // 如果当前有过滤器激活，先检查是否符合过滤条件
                if (currentFilter !== 'all' && !row.classList.contains('status-' + currentFilter)) {{
                    return;
                }}
                
                const name = row.querySelector('.name-text').textContent.toLowerCase();
                const url = row.querySelector('.url-link').textContent.toLowerCase();
                
                if (name.includes(searchTerm) || url.includes(searchTerm)) {{
                    row.style.display = '';
                }} else {{
                    row.style.display = 'none';
                }}
            }});
        }}
        
        // 平滑滚动到顶部按钮
        window.addEventListener('scroll', () => {{
            if (window.scrollY > 300) {{
                if (!document.querySelector('.scroll-top')) {{
                    const btn = document.createElement('button');
                    btn.className = 'scroll-top';
                    btn.innerHTML = '↑';
                    btn.style.cssText = 'position: fixed; bottom: 2rem; right: 2rem; width: 3rem; height: 3rem; border-radius: 50%; background: var(--primary); color: white; border: none; cursor: pointer; box-shadow: var(--shadow-lg); font-size: 1.5rem; z-index: 1000;';
                    btn.onclick = () => window.scrollTo({{ top: 0, behavior: 'smooth' }});
                    document.body.appendChild(btn);
                }}
            }} else {{
                const btn = document.querySelector('.scroll-top');
                if (btn) btn.remove();
            }}
        }});
    </script>
</body>
</html>'''

