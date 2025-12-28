# 使用示例

## 示例1：基本使用

截取指定网站的多个页面：

```bash
cptools screenshot \
  --host http://www.cafepress.com \
  --csv example_data.csv \
  --output ./screenshots \
  --log ./logs/screenshot.log \
  --html ./reports/result.html
```

## 示例2：高并发截图

使用更高的并发数来加速大量页面的截图：

```bash
cptools screenshot \
  --host http://www.example.com \
  --csv urls.csv \
  -c 20 \
  --output ./batch_screenshots
```

## 示例3：带钉钉通知

截图完成后自动发送钉钉通知：

```bash
cptools screenshot \
  --host http://www.example.com \
  --csv urls.csv \
  --dingding-webhook "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
```

## 示例4：自定义窗口大小

截取移动端视图（常见手机屏幕尺寸）：

```bash
cptools screenshot \
  --host http://www.example.com \
  --csv mobile_pages.csv \
  --width 375 \
  --height 667
```

平板视图：

```bash
cptools screenshot \
  --host http://www.example.com \
  --csv tablet_pages.csv \
  --width 768 \
  --height 1024
```

## 示例5：混合URL（相对路径和绝对路径）

CSV文件内容（`mixed_urls.csv`）：

```csv
url,name
/products,产品列表
/about,关于我们
https://www.google.com,Google首页
https://www.github.com,GitHub首页
/contact,联系方式
```

执行命令：

```bash
cptools screenshot \
  --host http://www.mysite.com \
  --csv mixed_urls.csv
```

结果：
- `/products` → `http://www.mysite.com/products`
- `/about` → `http://www.mysite.com/about`
- `https://www.google.com` → `https://www.google.com` (使用完整URL)
- `https://www.github.com` → `https://www.github.com` (使用完整URL)
- `/contact` → `http://www.mysite.com/contact`

## 示例6：完整配置

```bash
cptools screenshot \
  --host http://www.example.com \
  --csv production_urls.csv \
  --output ./production_screenshots \
  --log ./logs/production_$(date +%Y%m%d).log \
  --html ./reports/production_$(date +%Y%m%d).html \
  -c 15 \
  --timeout 60000 \
  --width 1920 \
  --height 1080 \
  --dingding-webhook "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
```

## 批量截图脚本示例

创建一个Shell脚本 `batch_screenshot.sh`：

```bash
#!/bin/bash

# 设置变量
HOST="http://www.example.com"
DATE=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="./screenshots_${DATE}"
LOG_FILE="./logs/batch_${DATE}.log"
HTML_FILE="./reports/batch_${DATE}.html"

# 执行截图
cptools screenshot \
  --host "${HOST}" \
  --csv data.csv \
  --output "${OUTPUT_DIR}" \
  --log "${LOG_FILE}" \
  --html "${HTML_FILE}" \
  -c 10

# 检查结果
if [ $? -eq 0 ]; then
    echo "截图任务成功完成！"
    echo "截图保存在: ${OUTPUT_DIR}"
    echo "报告保存在: ${HTML_FILE}"
else
    echo "截图任务失败，请查看日志: ${LOG_FILE}"
    exit 1
fi
```

使用方法：

```bash
chmod +x batch_screenshot.sh
./batch_screenshot.sh
```

## Python脚本调用示例

创建 `run_screenshot.py`：

```python
import subprocess
import sys
from datetime import datetime

def run_screenshot(host, csv_file, **kwargs):
    """执行截图任务"""
    cmd = [
        'cptools', 'screenshot',
        '--host', host,
        '--csv', csv_file
    ]
    
    # 添加可选参数
    if kwargs.get('output'):
        cmd.extend(['--output', kwargs['output']])
    if kwargs.get('log'):
        cmd.extend(['--log', kwargs['log']])
    if kwargs.get('html'):
        cmd.extend(['--html', kwargs['html']])
    if kwargs.get('concurrency'):
        cmd.extend(['-c', str(kwargs['concurrency'])])
    if kwargs.get('dingding_webhook'):
        cmd.extend(['--dingding-webhook', kwargs['dingding_webhook']])
    
    # 执行命令
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"错误: {e.stderr}", file=sys.stderr)
        return False

if __name__ == '__main__':
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    success = run_screenshot(
        host='http://www.example.com',
        csv_file='data.csv',
        output=f'./screenshots_{timestamp}',
        log=f'./logs/app_{timestamp}.log',
        html=f'./reports/result_{timestamp}.html',
        concurrency=10
    )
    
    sys.exit(0 if success else 1)
```

## 定时任务示例

使用crontab定时执行截图（Linux/Mac）：

```bash
# 编辑crontab
crontab -e

# 每天凌晨2点执行截图任务
0 2 * * * cd /path/to/cptool_cli && /path/to/venv/bin/cptools screenshot --host http://www.example.com --csv daily.csv --output ./daily_screenshots/$(date +\%Y\%m\%d) >> ./logs/cron.log 2>&1
```

Windows任务计划程序：

```batch
REM 创建批处理文件 screenshot_task.bat
@echo off
cd C:\path\to\cptool_cli
call venv\Scripts\activate
cptools screenshot --host http://www.example.com --csv daily.csv --output .\daily_screenshots\%date:~0,4%%date:~5,2%%date:~8,2%
```

然后在任务计划程序中添加该批处理文件的定时任务。

