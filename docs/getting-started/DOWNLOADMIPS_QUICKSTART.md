# 产品主图下载快速入门

## 5 分钟快速上手

### 1. 准备 CSV 文件

创建一个包含产品编号的 CSV 文件：

```bash
cat > products.csv << EOF
product_no
629442244
629442245
629442246
EOF
```

### 2. 运行下载命令

```bash
cptools downloadmips --host https://www.cafepress.com --csv products.csv --no-dingding
```

**其他地区站点：**

```bash
# AU 站点
cptools downloadmips -h https://www.cafepress.com.au --csv products.csv

# UK 站点
cptools downloadmips -h https://www.cafepress.co.uk --csv products.csv

# CA 站点
cptools downloadmips -h https://www.cafepress.ca --csv products.csv
```

### 3. 查看结果

- **下载的图片**：`./mips/{product_no}/`
- **HTML 报告**：`./downloadmips_result.html`
- **日志文件**：`./logs/downloadmips_*.log`

## 示例输出

```
2025-12-29 16:20:21 - 开始执行产品主图下载任务
2025-12-29 16:20:21 - 从CSV文件中读取到 1 个产品编号
2025-12-29 16:20:34 - [1] 找到 4 张图片
2025-12-29 16:20:34 - [1] 图片 1 下载成功: 629442244_01.jpg
2025-12-29 16:20:35 - [1] 图片 2 下载成功: 629442244_02.jpg
2025-12-29 16:20:35 - [1] 图片 3 下载成功: 629442244_03.jpg
2025-12-29 16:20:35 - [1] 图片 4 下载成功: 629442244_04.jpg
2025-12-29 16:20:35 - 产品主图下载任务完成
2025-12-29 16:20:35 - 总产品数: 1
2025-12-29 16:20:35 - 成功: 1
2025-12-29 16:20:35 - 下载图片总数: 4
```

## 常用选项

```bash
# 调整并发数（默认 3）
cptools downloadmips -h https://www.cafepress.com --csv products.csv -c 5

# 指定输出目录
cptools downloadmips -h https://www.cafepress.com --csv products.csv --output ./images

# 指定 HTML 报告位置
cptools downloadmips -h https://www.cafepress.com --csv products.csv --html ./report.html
```

## 下一步

查看完整文档：[DOWNLOADMIPS.md](./DOWNLOADMIPS.md)

