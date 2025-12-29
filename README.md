# CPTools - 命令行工具集

基于Python的命令行工具集，提供网页截屏、URL检测等实用功能。

## 功能特性

- 🖼️ **网页截屏**: 基于Playwright的高质量网页截图
- 🔍 **URL检测**: 批量检测URL状态码，识别404/500错误
- 📦 **产品主图下载**: 批量下载CafePress产品主图
- 🚀 **并发执行**: 支持多任务并发，提高执行效率
- 📊 **HTML报告**: 自动生成可视化的执行结果报告
- 📢 **钉钉通知**: 支持任务完成后发送钉钉通知
- 📝 **日志记录**: 完整的日志记录，便于追踪和调试

## 快速开始

### 方式1: 从 GitHub 安装（推荐）

```bash
pip install git+https://github.com/joeyplanetart/cptool_cli.git
playwright install chromium
cptools --version
```

### 方式2: 一键安装脚本

**Linux/Mac:**
```bash
./install_from_github.sh
```

**Windows:**
```bash
install_from_github.bat
```

### 方式3: 本地安装

如果已克隆仓库：

**Linux/Mac:**
```bash
git clone https://github.com/joeyplanetart/cptool_cli.git
cd cptool_cli
./setup_venv.sh
```

**Windows:**
```bash
git clone https://github.com/joeyplanetart/cptool_cli.git
cd cptool_cli
setup_venv.bat
```

## 📚 完整文档

详细文档请查看 [docs](docs/) 目录：

- **[快速开始指南](docs/getting-started/QUICKSTART.md)** - 5分钟快速上手
- **[产品主图下载快速入门](docs/getting-started/DOWNLOADMIPS_QUICKSTART.md)** - downloadmips 工具快速上手
- **[使用示例](docs/getting-started/EXAMPLES.md)** - 丰富的实战示例
- **[命令速查表](docs/reference/CHEATSHEET.md)** - 快速命令参考
- **[开发指南](docs/development/DEVELOPMENT.md)** - 贡献代码指南

**完整文档索引**: [docs/README.md](docs/README.md)

## 主要命令

### 截屏工具

```bash
cptools screenshot [选项]
```

**常用选项：**

| 选项 | 说明 |
|------|------|
| `--host`, `-h` | 默认主机地址（必需）|
| `--csv` | CSV文件路径（必需）|
| `--output`, `-o` | 截图保存目录 |
| `--log`, `-l` | 日志文件路径 |
| `--html` | HTML报告路径 |
| `-c` | 并发数量 |

**示例：**

```bash
# 基本使用
cptools screenshot --host http://example.com --csv urls.csv

# 高并发
cptools screenshot --host http://example.com --csv urls.csv -c 10

# 完整配置
cptools screenshot \
  --host http://example.com \
  --csv urls.csv \
  --output ./screenshots \
  --log ./logs/app.log \
  --html ./reports/result.html \
  -c 10 \
  --dingding-webhook https://oapi.dingtalk.com/robot/send?access_token=TOKEN
```

### URL 404检测工具

```bash
cptools url404 [选项]
```

**常用选项：**

| 选项 | 说明 |
|------|------|
| `--host`, `-h` | 默认主机地址（必需）|
| `--csv` | CSV文件路径（必需）|
| `--log`, `-l` | 日志文件路径 |
| `--html` | HTML报告路径 |
| `-c` | 并发数量 |

**示例：**

```bash
# 基本使用
cptools url404 --host http://www.cafepress.com --csv test_10.csv

# 自定义报告路径
cptools url404 --host http://example.com --csv urls.csv --html ./reports/url404_result.html

# 高并发检测
cptools url404 \
  --host http://example.com \
  --csv urls.csv \
  -c 10 \
  --log ./logs/url404.log
```

### 产品主图下载工具

```bash
cptools downloadmips [选项]
```

**常用选项：**

| 选项 | 说明 |
|------|------|
| `--host`, `-h` | 主机地址（必需，如: https://www.cafepress.com）|
| `--csv` | CSV文件路径（必需，包含product_no列）|
| `--output`, `-o` | 图片保存目录 |
| `--log`, `-l` | 日志文件路径 |
| `--html` | HTML报告路径 |
| `-c` | 并发数量（默认3，建议不要太大） |

**示例：**

```bash
# 基本使用 - US站点
cptools downloadmips --host https://www.cafepress.com --csv products.csv

# AU站点
cptools downloadmips -h https://www.cafepress.com.au --csv products.csv

# 完整配置
cptools downloadmips \
  -h https://www.cafepress.com \
  --csv products.csv \
  --output ./product_images \
  -c 3 \
  --log ./logs/download.log \
  --html ./report.html
```

**支持的地区：**

| 地区 | URL |
|------|-----|
| US | https://www.cafepress.com |
| AU | https://www.cafepress.com.au |
| UK | https://www.cafepress.co.uk |
| CA | https://www.cafepress.ca |

**CSV 格式：**

```csv
product_no
629442244
629442245
629442246
```

**产品URL格式**: `{host}/+,{product_no}`

**输出结构**:

```
mips/
├── 629442244/
│   ├── 629442244_01.jpg
│   ├── 629442244_02.jpg
│   └── ...
├── 629442245/
│   └── ...
└── 629442246/
    └── ...
```

## CSV 文件格式

```csv
url,name
/products/123,产品页面1
https://example.com/about,关于页面
/categories,分类页面
```

- **url**: 页面URL（可以是完整URL或相对路径）
- **name**: 截图名称（可选）

## 项目结构

```
cptool_cli/
├── cptools/              # 主包
│   ├── cli.py           # 命令行入口
│   ├── commands/        # 命令模块
│   └── utils/           # 工具模块
├── docs/                # 📚 文档目录
│   ├── getting-started/ # 快速入门
│   ├── guides/          # 详细指南
│   ├── reference/       # 参考文档
│   └── development/     # 开发文档
├── setup.py             # 安装配置
├── requirements.txt     # 依赖列表
└── README.md           # 本文件
```

## 脚本工具

| 脚本 | 说明 |
|------|------|
| `./setup_venv.sh` | 自动安装脚本（Linux/Mac）|
| `setup_venv.bat` | 自动安装脚本（Windows）|
| `./test.sh` | 环境测试脚本 |
| `./info.sh` | 显示项目信息 |

## 获取帮助

```bash
# 查看版本
cptools --version

# 查看帮助
cptools --help
cptools screenshot --help
cptools url404 --help
cptools downloadmips --help

# 运行测试
./test.sh
./test_downloadmips.sh

# 查看项目信息
./info.sh
```

## 开发

参见 [开发指南](docs/development/DEVELOPMENT.md)

## 许可证

MIT License

---

**需要帮助？** 查看 [完整文档](docs/README.md) 或运行 `./info.sh`

