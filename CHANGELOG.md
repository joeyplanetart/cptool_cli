# CPTools 更新日志

## 版本 1.1.0 - 2024-12-29

### 📦 新增产品主图下载工具

我们为 CPTools 添加了全新的产品主图下载功能！现在你可以批量下载 CafePress 产品的主图。

#### ✨ 新增功能

1. **downloadmips 命令**
   - 批量下载产品主图
   - 自动创建产品文件夹（以 product_no 命名）
   - 图片按序号命名（product_no_01, product_no_02...）
   - 支持并发下载
   - 内置反爬虫机制

2. **表格式 HTML 报告**
   - 清晰的表格展示
   - 每个产品一行
   - 缩略图预览
   - 点击放大查看
   - 响应式设计

3. **产品维度统计**
   - 总产品数
   - 成功数量
   - 失败数量
   - 下载图片总数

4. **钉钉通知**
   - 任务完成自动通知
   - 包含详细统计信息

#### 🚀 使用方法

```bash
# 基本使用
cptools downloadmips --csv products.csv

# 指定输出目录
cptools downloadmips --csv products.csv --output ./images

# 完整配置
cptools downloadmips \
  --csv products.csv \
  --output ./product_images \
  -c 3 \
  --log ./logs/download.log \
  --html ./report.html
```

#### 📂 新增文件

```
cptools/
├── commands/
│   └── downloadmips.py        # 新增 - 产品主图下载命令
└── utils/
    └── downloadmips_report.py # 新增 - 产品下载报告生成器

docs/
├── guides/
│   └── DOWNLOADMIPS.md        # 新增 - downloadmips 使用指南
└── getting-started/
    └── DOWNLOADMIPS_QUICKSTART.md  # 新增 - 快速入门

test_downloadmips.sh           # 新增 - 测试脚本
test_downloadmips.csv          # 新增 - 测试数据
```

#### 🔧 命令参数

```bash
cptools downloadmips [选项]

必需参数:
  --csv PATH                   CSV文件路径（包含 product_no 列）

可选参数:
  --output, -o TEXT            图片保存目录（默认: ./mips）
  --log, -l TEXT               日志文件路径
  --html TEXT                  HTML报告路径（默认: ./downloadmips_result.html）
  -c, --concurrency INTEGER    并发数量（默认: 3）
  --timeout INTEGER            超时时间（默认: 30000ms）
  --dingding-webhook TEXT      钉钉Webhook
  --dingding-secret TEXT       钉钉签名密钥
  --no-dingding               禁用钉钉通知
```

#### 📊 输出结构

```
mips/
├── 629442244/
│   ├── 629442244_01.jpg
│   ├── 629442244_02.jpg
│   ├── 629442244_03.jpg
│   └── 629442244_04.jpg
├── 629442245/
│   ├── 629442245_01.jpg
│   └── ...
└── 629442246/
    └── ...
```

#### 📖 文档

详细使用指南请查看：
- [产品主图下载使用指南](docs/guides/DOWNLOADMIPS.md)
- [快速入门](docs/getting-started/DOWNLOADMIPS_QUICKSTART.md)
- [README.md](README.md)

#### 🔄 版本更新

- 更新 CLI 主命令描述
- 更新 README 功能列表
- 新增测试脚本

### 🔍 新增 URL 404检测工具

我们为 CPTools 添加了全新的 URL 状态码检测功能！现在你可以批量检测 URL 是否存在 404、500 等错误。

#### ✨ 新增功能

1. **url404 命令**
   - 批量检测 URL 状态码
   - 自动识别 404 和 500 错误
   - 支持并发检测
   - 无需截图,检测速度更快

2. **列表式 HTML 报告**
   - 清晰的表格展示
   - 状态码彩色标识
   - 过滤功能(全部/成功/404/错误)
   - 搜索功能(按 URL 或名称)
   - 响应式设计

3. **状态统计**
   - 成功数(2xx-3xx)
   - 404 错误数
   - 500+ 错误数
   - 其他错误数

4. **钉钉通知**
   - 任务完成自动通知
   - 包含详细统计信息

#### 🚀 使用方法

```bash
# 基本使用
cptools url404 --host http://www.cafepress.com --csv test_10.csv

# 自定义输出
cptools url404 -h http://example.com --csv urls.csv --html ./url404_result.html

# 高并发检测
cptools url404 -h http://example.com --csv urls.csv -c 10
```

#### 📂 新增文件

```
cptools/
├── commands/
│   └── url404.py              # 新增 - URL404检测命令
└── utils/
    └── url404_report.py       # 新增 - URL404报告生成器

docs/
└── guides/
    └── URL404.md              # 新增 - URL404使用指南

test_url404.sh                 # 新增 - URL404测试脚本
```

#### 🔧 命令参数

```bash
cptools url404 [选项]

必需参数:
  --host, -h TEXT              默认主机地址
  --csv PATH                   CSV文件路径

可选参数:
  --log, -l TEXT               日志文件路径
  --html TEXT                  HTML报告路径(默认: ./url404_result.html)
  -c, --concurrency INTEGER    并发数量(默认: 5)
  --timeout INTEGER            超时时间(默认: 30000ms)
  --dingding-webhook TEXT      钉钉Webhook
  --dingding-secret TEXT       钉钉签名密钥
```

#### 📊 HTML 报告特性

- **可视化统计**: 顶部显示总数、成功、404、500等统计
- **状态过滤**: 快速过滤不同状态的 URL
- **实时搜索**: 按 URL 或名称搜索
- **状态标识**: 
  - ✓ 绿色 = 成功(2xx-3xx)
  - ⚠ 黄色 = 404
  - ✗ 红色 = 500+/错误

#### 📖 文档

详细使用指南请查看：
- [URL404 使用指南](docs/guides/URL404.md)
- [README.md](README.md)

#### 🔄 版本更新

- 版本号: 1.0.0 → 1.1.0
- 更新 CLI 主命令描述
- 更新 README 功能列表

### 🎨 HTML 报告模板系统 (v1.0.1)

我们为 CPTools 添加了功能强大的 HTML 报告模板系统！现在你可以根据不同场景选择不同风格的报告模板。

#### ✨ 新增功能

1. **三种精美模板**
   - **Default** - 现代渐变风格，紫色主题，适合正式场合
   - **Terminal** - 黑客终端风格，绿色矩阵主题，适合技术团队
   - **Minimal** - 极简主义风格，白色主题，专注内容

2. **图片预览功能**
   - 点击任意截图可全屏预览
   - 支持 ESC 键快速关闭
   - 所有模板均支持

3. **响应式设计**
   - 自适应不同屏幕尺寸
   - 移动设备友好
   - 支持触摸操作

#### 🚀 使用方法

```bash
# 使用默认模板
cptools screenshot --host http://example.com --csv data.csv

# 使用终端模板
cptools screenshot --host http://example.com --csv data.csv --template terminal

# 使用简约模板  
cptools screenshot --host http://example.com --csv data.csv --template minimal
```

#### 📂 新增文件

```
cptools/
├── templates/              # 新增 - 模板目录
│   ├── default.html       # 默认模板
│   ├── terminal.html      # 终端模板
│   └── minimal.html       # 简约模板
└── utils/
    └── html_report.py     # 更新 - 支持模板系统

docs/
└── reference/
    └── TEMPLATES.md       # 新增 - 模板使用文档
```

#### 🔧 更新的命令参数

```bash
cptools screenshot [选项]

新增参数:
  --template [default|terminal|minimal]  HTML报告模板（默认：default）
```

#### 📖 文档

详细的模板使用指南请查看：
- [模板文档](docs/reference/TEMPLATES.md)
- [命令速查表](docs/reference/CHEATSHEET.md)

---

## 版本 1.0.1 - 2024-12-28

### 📚 文档重组

将所有 Markdown 文档移动到 `docs/` 目录并进行分类：

```
docs/
├── README.md              # 文档中心索引
├── getting-started/       # 快速入门
├── guides/               # 详细指南
├── reference/            # 参考文档
└── development/          # 开发文档
```

### ⚡ 参数优化

- 将 `--concurrency` 的短选项从 `-n` 改为 `-c`
- 移除 `--csv` 的短选项以避免冲突
- 统一命令行参数风格

---

## 版本 1.0.0 - 2024-12-27

### 🎉 首次发布

基于 Playwright 的网页截屏工具，支持：
- 异步并发截图
- HTML 可视化报告
- 钉钉通知集成
- 完整的日志记录
- 虚拟环境管理

---

**查看完整文档**: [docs/README.md](docs/README.md)

