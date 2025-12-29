# URL404 检测 - 快速开始

## 5分钟快速上手

本指南将帮助你在 5 分钟内开始使用 CPTools 的 URL404 检测功能。

## 前提条件

确保已安装 CPTools:

```bash
# 检查安装
cptools --version

# 应该显示: cptools, version 1.1.0 或更高
```

如果未安装,请参考 [安装指南](../INSTALL.md)。

## 第一步: 准备 CSV 文件

创建一个包含要检测的 URL 列表的 CSV 文件:

```csv
PTN_NO,PRODUCT_ID,URL
1,首页,/
2,关于我们,/about
3,产品页,/products/123
4,联系我们,/contact
```

**注意**: 
- CSV 必须包含 `URL` 列
- 可以包含 `PRODUCT_ID`、`name` 等列作为名称
- URL 可以是相对路径或完整 URL

## 第二步: 运行检测

```bash
cptools url404 --host http://www.example.com --csv your_urls.csv
```

**示例**:

```bash
cptools url404 --host http://www.cafepress.com --csv test_10.csv
```

## 第三步: 查看结果

### 1. 控制台输出

```
================================================================================
URL 404检测任务完成
总数: 10
成功(2xx-3xx): 8
404错误: 1
500错误: 0
其他错误: 1
耗时: 12.89秒
================================================================================
```

### 2. HTML 报告

命令执行完成后会自动打开浏览器显示报告。报告包含:

- 📊 **统计面板**: 总数、成功、404、500等
- 🔍 **过滤按钮**: 点击查看特定状态的 URL
- 🔎 **搜索框**: 搜索 URL 或名称
- 📋 **结果表格**: 详细的检测结果列表

### 3. 日志文件

日志文件保存在 `logs/url404_YYYYMMDD_HHMMSS.log`

## 常用选项

### 提高并发数(加快检测)

```bash
cptools url404 -h http://example.com --csv urls.csv -c 10
```

### 自定义报告路径

```bash
cptools url404 -h http://example.com --csv urls.csv --html ./reports/check.html
```

### 增加超时时间

```bash
cptools url404 -h http://example.com --csv urls.csv --timeout 60000
```

### 自定义日志路径

```bash
cptools url404 -h http://example.com --csv urls.csv -l ./logs/my_check.log
```

## 完整示例

```bash
cptools url404 \
  --host http://www.cafepress.com \
  --csv test_10.csv \
  --html ./reports/url_check.html \
  --log ./logs/check.log \
  -c 8 \
  --timeout 45000
```

## 理解结果

### 状态码含义

| 状态码 | 含义 | 颜色 |
|--------|------|------|
| 200-299 | 成功 | 🟢 绿色 |
| 300-399 | 重定向(正常) | 🟢 绿色 |
| 404 | 页面不存在 | 🟡 黄色 |
| 500-599 | 服务器错误 | 🔴 红色 |
| 其他 4xx | 客户端错误 | 🟡 黄色 |

### HTML 报告操作

1. **查看所有结果**: 点击"全部"按钮
2. **只看成功**: 点击"成功"按钮
3. **查看404**: 点击"404"按钮
4. **查看错误**: 点击"错误"按钮
5. **搜索特定URL**: 在搜索框输入关键词

## 下一步

### 了解更多

- [URL404 完整文档](../guides/URL404.md)
- [命令速查表](../reference/CHEATSHEET.md)
- [常见问题](../guides/URL404.md#常见问题)

### 高级用法

- 调整并发数优化性能
- 配置钉钉通知
- 批量处理大量 URL
- 导出检测结果

## 常见问题

### Q: 为什么有些 URL 显示错误?

A: 可能原因:
- URL 不存在(404)
- 服务器错误(500)
- 网络超时
- 权限问题

### Q: 如何加快检测速度?

A: 增加并发数:

```bash
cptools url404 -h http://example.com --csv urls.csv -c 10
```

**注意**: 并发数过高可能导致服务器拒绝请求。

### Q: CSV 文件格式错误怎么办?

A: 确保:
- 文件包含表头
- 有 `URL` 列
- 使用 UTF-8 编码
- 逗号分隔

### Q: 如何只检测失败的 URL?

A: 先运行完整检测,然后在 HTML 报告中:
1. 点击"404"或"错误"按钮
2. 复制失败的 URL
3. 创建新的 CSV 文件重新检测

## 获取帮助

```bash
# 查看帮助
cptools url404 --help

# 查看示例
cptools url404 --help | grep "示例" -A 10
```

## 对比 screenshot 命令

| 特性 | url404 | screenshot |
|------|--------|-----------|
| 主要用途 | 检测状态码 | 网页截图 |
| 速度 | 快 | 慢 |
| 输出 | HTML报告 | 图片 + HTML |
| 适用场景 | URL验证 | 视觉检查 |

**组合使用**: 先用 `url404` 找出有问题的 URL,再用 `screenshot` 查看页面效果!

---

**需要更多帮助?** 查看 [完整文档](../guides/URL404.md) 或运行 `cptools url404 --help`

