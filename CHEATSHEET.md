# CPTools 快速参考

## 🚀 快速开始

```bash
# 1. 一键安装
./setup_venv.sh              # Linux/Mac
setup_venv.bat               # Windows

# 2. 激活环境（每次使用前）
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows

# 3. 运行截图
cptools screenshot -h http://example.com -c data.csv -l log.log --html result.html
```

## 📋 常用命令

### 环境管理
```bash
# 激活虚拟环境
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows

# 退出虚拟环境
deactivate

# 检查环境
echo $VIRTUAL_ENV            # 显示虚拟环境路径
which python                 # 显示Python路径
pip list                     # 显示已安装包
```

### 截图命令
```bash
# 基本用法
cptools screenshot --host <主机> --csv <文件> [选项]

# 查看帮助
cptools --help
cptools screenshot --help

# 完整示例
cptools screenshot \
  --host http://www.example.com \
  --csv urls.csv \
  --output ./screenshots \
  --log ./log.log \
  --html ./result.html \
  --concurrency 10 \
  --timeout 30000 \
  --width 1920 \
  --height 1080 \
  --dingding-webhook "https://oapi.dingtalk.com/robot/send?access_token=TOKEN"
```

## ⚙️ 命令参数

| 参数 | 短选项 | 必需 | 默认值 | 说明 |
|------|--------|------|--------|------|
| `--host` | `-h` | ✓ | - | 默认主机地址 |
| `--csv` | `-c` | ✓ | - | CSV文件路径 |
| `--output` | `-o` | ✗ | ./screenshots | 截图保存目录 |
| `--log` | `-l` | ✗ | ./screenshot.log | 日志文件路径 |
| `--html` | | ✗ | ./result.html | HTML报告路径 |
| `--concurrency` | `-n` | ✗ | 5 | 并发数量 |
| `--timeout` | | ✗ | 30000 | 超时时间（毫秒） |
| `--width` | | ✗ | 1920 | 浏览器宽度 |
| `--height` | | ✗ | 1080 | 浏览器高度 |
| `--dingding-webhook` | | ✗ | - | 钉钉通知URL |

## 📄 CSV文件格式

```csv
url,name
/products,产品页面
/about,关于页面
https://example.com,外部链接
```

- `url`: 页面URL（必需）
  - 相对路径：使用 `--host` 参数
  - 完整URL：忽略 `--host` 参数
- `name`: 截图名称（可选）

## 🔧 故障排除

### cptools命令找不到
```bash
# 1. 检查虚拟环境
echo $VIRTUAL_ENV

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 重新安装
pip install -e .
```

### Playwright浏览器找不到
```bash
playwright install chromium
```

### 依赖问题
```bash
# 删除并重建虚拟环境
rm -rf venv
./setup_venv.sh
```

## 📱 常见场景

### 桌面端截图（默认）
```bash
cptools screenshot -h http://example.com -c urls.csv
```

### 移动端截图
```bash
cptools screenshot -h http://example.com -c urls.csv \
  --width 375 --height 667
```

### 平板截图
```bash
cptools screenshot -h http://example.com -c urls.csv \
  --width 768 --height 1024
```

### 高并发快速截图
```bash
cptools screenshot -h http://example.com -c urls.csv \
  --concurrency 20
```

### 慢速网站截图
```bash
cptools screenshot -h http://example.com -c urls.csv \
  --timeout 60000 --concurrency 3
```

### 带钉钉通知
```bash
cptools screenshot -h http://example.com -c urls.csv \
  --dingding-webhook "https://oapi.dingtalk.com/robot/send?access_token=TOKEN"
```

## 📊 输出文件

| 文件 | 说明 |
|------|------|
| `screenshots/*.png` | 截图文件 |
| `log.log` | 详细日志 |
| `result.html` | 可视化报告（用浏览器打开） |

## 🎯 最佳实践

1. **始终使用虚拟环境** - `source venv/bin/activate`
2. **合理设置并发数** - 根据网络和机器性能调整
3. **使用有意义的name** - CSV中添加描述性名称
4. **定期查看日志** - 了解失败原因
5. **保存HTML报告** - 便于查看和分享结果

## 📚 文档

| 文档 | 内容 |
|------|------|
| `README.md` | 项目概述 |
| `QUICKSTART.md` | 快速开始 |
| `EXAMPLES.md` | 使用示例 |
| `VENV_GUIDE.md` | 虚拟环境详细指南 |
| `DEVELOPMENT.md` | 开发文档 |
| `GITHUB_UPLOAD.md` | GitHub上传指南 |

## 💡 提示

- **Tab补全**: 输入命令后按Tab键可自动补全
- **历史命令**: 按上箭头键查看历史命令
- **后台运行**: 添加 `&` 在后台运行: `cptools screenshot ... &`
- **输出重定向**: 保存输出: `cptools screenshot ... > output.txt 2>&1`

## 🆘 获取帮助

```bash
# 查看版本
cptools --version

# 查看所有命令
cptools --help

# 查看子命令帮助
cptools screenshot --help

# 运行测试脚本
./test.sh
```

## 🌐 资源链接

- GitHub仓库: `https://github.com/yourusername/cptool_cli`
- Playwright文档: `https://playwright.dev/python/`
- Python venv: `https://docs.python.org/3/library/venv.html`

---

**版本**: 1.0.0  
**更新**: 2024-12-28

