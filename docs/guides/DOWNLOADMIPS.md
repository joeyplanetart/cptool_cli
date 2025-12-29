# 产品主图下载工具 (downloadmips)

## 概述

`downloadmips` 是一个从 CafePress 网站批量下载产品主图的命令行工具。它可以自动访问产品页面，提取 `stackable-image-container` 类下的所有图片，并保存到以产品编号命名的文件夹中。

## 功能特点

- ✅ 批量下载产品主图
- ✅ 自动创建产品文件夹（以 product_no 命名）
- ✅ 图片按序号命名（product_no_01, product_no_02...）
- ✅ 生成美观的 HTML 报告（表格形式，一个产品一行）
- ✅ 支持并发下载（可自定义并发数）
- ✅ 反爬虫机制（随机延迟、模拟真实浏览器）
- ✅ 钉钉通知（以产品维度统计）
- ✅ 详细的日志记录

## 产品 URL 格式

```
{host}/+,{product_no}
```

**支持的地区：**

| 地区 | Host URL | 示例 |
|------|----------|------|
| US | `https://www.cafepress.com` | `https://www.cafepress.com/+,629442244` |
| AU | `https://www.cafepress.com.au` | `https://www.cafepress.com.au/+,629442244` |
| UK | `https://www.cafepress.co.uk` | `https://www.cafepress.co.uk/+,629442244` |
| CA | `https://www.cafepress.ca` | `https://www.cafepress.ca/+,629442244` |

也支持测试环境或其他自定义 host 地址。

## CSV 文件格式

CSV 文件必须包含 `product_no` 列（不区分大小写）：

```csv
product_no
629442244
629442245
629442246
```

支持的列名：
- `product_no` / `PRODUCT_NO`
- `productno`
- `product_id` / `PRODUCT_ID`

## 基本用法

### 1. 最简单的用法

```bash
cptools downloadmips --host https://www.cafepress.com --csv products.csv
```

这将：
- 使用指定的 host 地址
- 从 `products.csv` 读取产品编号
- 下载图片到 `./mips/{product_no}/` 目录
- 生成 HTML 报告到 `./downloadmips_result.html`
- 自动生成日志文件到 `./logs/downloadmips_YYYYMMDD_HHMMSS.log`

### 2. 不同地区站点

```bash
# US 站点
cptools downloadmips --host https://www.cafepress.com --csv products.csv

# AU 站点
cptools downloadmips -h https://www.cafepress.com.au --csv products.csv

# UK 站点
cptools downloadmips -h https://www.cafepress.co.uk --csv products.csv

# CA 站点
cptools downloadmips -h https://www.cafepress.ca --csv products.csv
```

### 3. 自定义输出目录

```bash
cptools downloadmips -h https://www.cafepress.com --csv products.csv --output ./images
```

### 4. 调整并发数

```bash
# 默认并发数为 3，建议不要设置太大以避免被封
cptools downloadmips -h https://www.cafepress.com --csv products.csv -c 5
```

### 5. 禁用钉钉通知（调试时）

```bash
cptools downloadmips -h https://www.cafepress.com --csv products.csv --no-dingding
```

### 6. 完整示例

```bash
cptools downloadmips \
    --host https://www.cafepress.com \
    --csv products.csv \
    --output ./product_images \
    -c 3 \
    --log ./logs/download.log \
    --html ./report.html \
    --no-dingding
```

## 命令参数

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--host` | `-h` | **必需** | 主机地址（如: https://www.cafepress.com） |
| `--csv` | - | **必需** | CSV文件路径 |
| `--output` | `-o` | `./mips` | 图片保存目录 |
| `--log` | `-l` | 自动生成 | 日志文件路径 |
| `--html` | - | `./downloadmips_result.html` | HTML报告路径 |
| `--concurrency` | `-c` | `3` | 并发数量 |
| `--timeout` | - | `30000` | 页面加载超时（毫秒） |
| `--dingding-webhook` | - | 已配置 | 钉钉机器人 Webhook |
| `--dingding-secret` | - | 已配置 | 钉钉机器人签名密钥 |
| `--no-dingding` | - | `False` | 禁用钉钉通知 |

## 输出结构

### 文件夹结构

```
mips/
├── 629442244/
│   ├── 629442244_01.jpg
│   ├── 629442244_02.jpg
│   ├── 629442244_03.jpg
│   └── 629442244_04.jpg
├── 629442245/
│   ├── 629442245_01.jpg
│   ├── 629442245_02.jpg
│   └── 629442245_03.jpg
└── 629442246/
    ├── 629442246_01.jpg
    └── 629442246_02.jpg
```

### HTML 报告

报告采用表格形式展示，每个产品占一行：

- **产品编号**：产品的唯一标识
- **URL**：产品页面链接
- **状态**：成功 ✓ / 失败 ✗
- **图片数**：下载的图片数量
- **预览图**：缩略图预览（点击放大）

### 钉钉通知

通知内容包括：
- 总产品数
- 成功数量
- 失败数量
- 下载图片总数
- 执行耗时
- CSV文件路径

## 与 screenshot 的区别

| 特性 | screenshot | downloadmips |
|------|-----------|--------------|
| **URL 格式** | CSV 中提供完整 URL 或相对路径 | 固定格式：`/+,{product_no}` |
| **主要功能** | 网页截图 | 下载图片 |
| **输出** | PNG 截图文件 | JPG/PNG/GIF 等原图 |
| **文件组织** | 单层目录 | 产品文件夹结构 |
| **HTML 报告** | 网格卡片布局 | 表格布局 |
| **通知维度** | URL 维度 | 产品维度 |

## 常见问题

### 1. 为什么有些产品下载失败？

可能的原因：
- 产品不存在（404 错误）
- 页面没有 `stackable-image-container` 类的图片
- 网络超时
- 被反爬虫机制阻止

解决方法：
- 检查产品编号是否正确
- 降低并发数（`-c 1` 或 `-c 2`）
- 增加超时时间（`--timeout 60000`）

### 2. 如何避免被封？

建议：
- 使用较低的并发数（默认 3 已经比较保守）
- 不要一次性下载太多产品
- 工具已内置随机延迟和真实浏览器特征

### 3. 图片格式是什么？

工具会根据原图 URL 自动判断格式：
- `.jpg` / `.jpeg`
- `.png`
- `.gif`
- `.webp`

### 4. 可以断点续传吗？

暂不支持。每次运行会清空输出目录重新下载。

### 5. 日志文件在哪里？

默认在 `./logs/downloadmips_YYYYMMDD_HHMMSS.log`

## 性能参考

- 单个产品（4张图片）：约 10-15 秒
- 10 个产品（并发3）：约 50-80 秒
- 100 个产品（并发3）：约 8-12 分钟

*注：实际时间取决于网络速度和页面复杂度*

## 测试

运行测试脚本：

```bash
./test_downloadmips.sh
```

或手动测试：

```bash
# 创建测试 CSV
echo "product_no" > test.csv
echo "629442244" >> test.csv

# 运行测试
cptools downloadmips --csv test.csv --no-dingding
```

## 更新日志

### v1.1.0 (2025-12-29)

- 🎉 新增 `downloadmips` 命令
- ✨ 支持批量下载产品主图
- 📊 新的表格式 HTML 报告
- 📁 自动创建产品文件夹结构
- 🔔 产品维度的钉钉通知

## 许可证

与 CPTools 项目相同，详见 [LICENSE](../LICENSE)。

