# 测试说明

## 已准备好测试！

你的CSV文件已经添加到项目中：`csv_data/categories_172 1-100.csv`

## 🚀 快速测试

### 方式1: 使用测试脚本（推荐）

```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 运行测试脚本
./run_test.sh http://www.cafepress.com "csv_data/categories_172 1-100.csv" 5

# 参数说明:
#   参数1: 主机地址（默认: http://www.cafepress.com）
#   参数2: CSV文件路径（默认: csv_data/categories_172 1-100.csv）
#   参数3: 并发数（默认: 5）
```

测试脚本会自动：
- ✓ 检查虚拟环境
- ✓ 显示CSV文件预览
- ✓ 统计URL数量
- ✓ 询问确认
- ✓ 创建带时间戳的输出目录
- ✓ 执行截图任务
- ✓ 显示执行结果统计
- ✓ 提供打开HTML报告选项

### 方式2: 直接使用命令

```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 直接运行
cptools screenshot \
  --host http://www.cafepress.com \
  --csv "csv_data/categories_172 1-100.csv" \
  --output ./screenshots \
  --log ./test.log \
  --html ./result.html \
  --concurrency 10
```

## 📋 CSV格式说明

你的CSV文件使用以下格式：
```csv
PTN_NO,PRODUCT_ID,URL
17108,1 Liter Stainless Steel Water Bottles,+1-liter-stainless-steel-water-bottles
18200,100th birthday,+100th-birthday
```

程序已经支持这种格式：
- **PTN_NO**: 产品编号（会被忽略）
- **PRODUCT_ID**: 作为截图名称使用 ✓
- **URL**: URL路径（会与host组合）✓

## 🔄 URL处理方式

你的CSV中的URL以 `+` 开头，例如：
- `+1-liter-stainless-steel-water-bottles`

程序会自动处理：
1. 移除开头的 `+`
2. 与 `--host` 参数组合
3. 最终URL: `http://www.cafepress.com/1-liter-stainless-steel-water-bottles`

## ⚙️ 建议的测试配置

### 小批量测试（前10条）

```bash
# 创建测试用的小文件
head -n 11 "csv_data/categories_172 1-100.csv" > test_10.csv

# 运行测试
./run_test.sh http://www.cafepress.com test_10.csv 3
```

### 完整测试（全部100条）

```bash
# 使用较高并发
./run_test.sh http://www.cafepress.com "csv_data/categories_172 1-100.csv" 10
```

### 保守测试（慢速但稳定）

```bash
# 低并发，适合网络不稳定时
./run_test.sh http://www.cafepress.com "csv_data/categories_172 1-100.csv" 2
```

## 📊 预期结果

运行后会生成：

```
test_screenshots_20241228_180000/   # 截图目录（100张图片）
├── 1 Liter Stainless Steel Water Bottles_20241228_180001.png
├── 100th birthday_20241228_180002.png
├── 10th birthday_20241228_180003.png
└── ...

test_logs/
└── test_20241228_180000.log        # 详细日志

test_reports/
└── report_20241228_180000.html     # HTML报告（用浏览器打开）
```

## 🐛 故障排除

### 如果截图失败

1. **检查URL是否正确**
   ```bash
   # 手动测试一个URL
   curl -I "http://www.cafepress.com/1-liter-stainless-steel-water-bottles"
   ```

2. **降低并发数**
   ```bash
   ./run_test.sh http://www.cafepress.com "csv_data/categories_172 1-100.csv" 2
   ```

3. **增加超时时间**
   ```bash
   cptools screenshot ... --timeout 60000
   ```

4. **查看详细日志**
   ```bash
   less test_logs/test_*.log
   ```

### 如果某些页面失败

这是正常的！可能原因：
- 页面不存在（404）
- 页面加载超时
- 临时网络问题

查看HTML报告了解哪些成功、哪些失败。

## 💡 优化建议

### 根据网络速度调整并发

```bash
# 快速网络
./run_test.sh http://www.cafepress.com "csv_data/categories_172 1-100.csv" 15

# 普通网络
./run_test.sh http://www.cafepress.com "csv_data/categories_172 1-100.csv" 5

# 慢速网络
./run_test.sh http://www.cafepress.com "csv_data/categories_172 1-100.csv" 2
```

### 分批处理大量URL

```bash
# 分成多个文件
split -l 20 "csv_data/categories_172 1-100.csv" batch_

# 分别处理
for file in batch_*; do
    ./run_test.sh http://www.cafepress.com "$file" 5
    sleep 10  # 休息10秒
done
```

## 📞 需要帮助？

运行环境检查：
```bash
./test.sh
```

查看项目信息：
```bash
./info.sh
```

查看快速参考：
```bash
cat CHEATSHEET.md
```

---

**准备好了！现在可以运行测试了** 🎉

```bash
source venv/bin/activate
./run_test.sh
```

