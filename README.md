# CPTools - 命令行工具集

基于Python的命令行工具集，提供网页截屏等实用功能。

## 功能特性

- 🖼️ **网页截屏**: 基于Playwright的高质量网页截图
- 🚀 **并发执行**: 支持多任务并发，提高执行效率
- 📊 **HTML报告**: 自动生成可视化的执行结果报告
- 📢 **钉钉通知**: 支持任务完成后发送钉钉通知
- 📝 **日志记录**: 完整的日志记录，便于追踪和调试

## 安装

### 方式1: 自动安装（推荐）

使用提供的安装脚本自动创建虚拟环境并安装所有依赖：

**Linux/Mac:**
```bash
git clone https://github.com/yourusername/cptool_cli.git
cd cptool_cli
./setup_venv.sh
```

**Windows:**
```bash
git clone https://github.com/yourusername/cptool_cli.git
cd cptool_cli
setup_venv.bat
```

### 方式2: 手动安装

**1. 克隆仓库**
```bash
git clone https://github.com/yourusername/cptool_cli.git
cd cptool_cli
```

**2. 创建虚拟环境**
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. 安装依赖**
```bash
pip install --upgrade pip
pip install -e .
```

**4. 安装Playwright浏览器驱动**
```bash
playwright install chromium
```

## 使用方法

### 激活虚拟环境

**每次使用前必须先激活虚拟环境：**

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

激活后，命令行提示符前会显示 `(venv)`

退出虚拟环境：
```bash
deactivate
```

### 截屏工具

#### 基本用法

```bash
cptools screenshot --host http://www.cafepress.com --csv data.csv --log log.log --html result.html
```

#### 参数说明

- `--host`: 默认的主机地址（当CSV中的URL没有域名时使用）
- `--csv`: CSV文件路径，包含要截图的URL列表
- `--output`: 截图保存目录（默认：./screenshots）
- `--log`: 日志文件路径（默认：./screenshot.log）
- `--html`: HTML报告输出路径（默认：./result.html）
- `--concurrency`: 并发数量（默认：5）
- `--dingding-webhook`: 钉钉机器人Webhook URL（可选）

#### CSV文件格式

CSV文件应包含以下列：

**格式1（推荐）：**
```csv
url,name
/products/123,产品页面1
https://example.com/about,关于页面
/categories,分类页面
```

**格式2（也支持）：**
```csv
PTN_NO,PRODUCT_ID,URL
17108,1 Liter Stainless Steel Water Bottles,+1-liter-stainless-steel-water-bottles
18200,100th birthday,+100th-birthday
```

列说明：
- **URL列**（必需）：支持 `url`、`URL` 等列名（不区分大小写）
  - 完整URL：如 `https://example.com/about`
  - 相对路径：如 `/products` 或 `+products`（会与 `--host` 组合）
- **名称列**（可选）：支持 `name`、`PRODUCT_ID`、`title` 等列名
  - 用于生成截图文件名
  - 如果不提供，将自动生成为 `screenshot-1`, `screenshot-2` 等

#### 完整示例

```bash
cptools screenshot \
  --host http://www.cafepress.com \
  --csv data.csv \
  --output ./screenshots \
  --log ./logs/app.log \
  --html ./reports/result.html \
  --concurrency 10 \
  --dingding-webhook https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN
```

### 查看帮助

```bash
cptools --help
cptools screenshot --help
```

## 开发

### 项目结构

```
cptool_cli/
├── cptools/
│   ├── __init__.py
│   ├── cli.py              # 主命令行入口
│   ├── commands/
│   │   ├── __init__.py
│   │   └── screenshot.py   # 截屏命令实现
│   └── utils/
│       ├── __init__.py
│       ├── logger.py       # 日志工具
│       ├── html_report.py  # HTML报告生成
│       └── dingding.py     # 钉钉通知
├── setup.py
├── requirements.txt
└── README.md
```

### 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License

