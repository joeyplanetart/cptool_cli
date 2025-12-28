# 快速开始指南

## 安装步骤

### 方式1: 一键安装（推荐）

**Linux/Mac:**
```bash
git clone <your-repository-url>
cd cptool_cli
./setup_venv.sh
```

脚本会自动完成：
- ✓ 检查Python环境
- ✓ 创建虚拟环境
- ✓ 升级pip
- ✓ 安装项目依赖
- ✓ 安装Playwright浏览器
- ✓ 验证安装

**Windows:**
```bash
git clone <your-repository-url>
cd cptool_cli
setup_venv.bat
```

### 方式2: 手动安装

**1. 克隆或下载项目**
```bash
git clone <your-repository-url>
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

**3. 升级pip并安装项目**
```bash
pip install --upgrade pip
pip install -e .
```

**4. 安装Playwright浏览器驱动**
```bash
playwright install chromium
```

## 基本使用

### 重要：激活虚拟环境

**每次使用前必须先激活虚拟环境！**

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

激活后，命令行提示符前会显示 `(venv)`

### 1. 准备CSV文件

创建一个CSV文件（例如 `data.csv`），包含要截图的URL：

**格式1（简单）：**
```csv
url,name
/products/123,产品页面1
/categories,分类页面
https://www.example.com/about,关于页面
/contact,联系我们
```

**格式2（带编号）：**
```csv
PTN_NO,PRODUCT_ID,URL
17108,水瓶产品,+1-liter-stainless-steel-water-bottles
18200,生日主题,+100th-birthday
```

**重要说明：**
- URL列必需（支持 `url`、`URL` 等，不区分大小写）
- 名称列可选（支持 `name`、`PRODUCT_ID`、`title` 等）
- URL可以是完整地址或相对路径
- 以 `+` 或 `/` 开头的URL会与 `--host` 参数组合

### 2. 执行截图

```bash
cptools screenshot \
  --host http://www.cafepress.com \
  --csv data.csv \
  --log log.log \
  --html result.html
```

### 3. 查看结果

- 截图文件：默认保存在 `./screenshots/` 目录
- 日志文件：`log.log`
- HTML报告：`result.html`（用浏览器打开查看）

## 高级用法

### 自定义输出目录

```bash
cptools screenshot \
  --host http://example.com \
  --csv data.csv \
  --output ./my_screenshots
```

### 调整并发数

```bash
cptools screenshot \
  --host http://example.com \
  --csv data.csv \
  -c 10
```

### 启用钉钉通知

```bash
cptools screenshot \
  --host http://example.com \
  --csv data.csv \
  --dingding-webhook https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN
```

### 自定义浏览器窗口大小

```bash
cptools screenshot \
  --host http://example.com \
  --csv data.csv \
  --width 1366 \
  --height 768
```

## 查看帮助

```bash
# 查看所有命令
cptools --help

# 查看screenshot命令帮助
cptools screenshot --help
```

## 上传到GitHub

### 1. 在GitHub上创建新仓库

访问 https://github.com/new 创建一个新仓库

### 2. 关联远程仓库

```bash
git remote add origin https://github.com/yourusername/cptool_cli.git
```

### 3. 推送到GitHub

```bash
git branch -M main
git push -u origin main
```

## 常见问题

### Q: 提示 "playwright未安装" 怎么办？

A: 运行以下命令：
```bash
pip install playwright
playwright install chromium
```

### Q: 截图失败怎么办？

A: 检查：
1. 目标网站是否可访问
2. 网络连接是否正常
3. 查看日志文件了解详细错误信息

### Q: 如何加快截图速度？

A: 可以增加并发数：
```bash
cptools screenshot -c 20 ...
```

### Q: CSV文件格式有什么要求？

A: 
- 必须包含 `url` 列
- `name` 列可选，用于给截图命名
- 使用UTF-8编码保存

## 示例文件

项目中包含 `example_data.csv` 作为参考示例。

