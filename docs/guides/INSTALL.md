# CPTools 快速安装

## 🚀 一键安装（推荐）

### 从 GitHub 安装

```bash
pip install git+https://github.com/joeyplanetart/cptool_cli.git
playwright install chromium
cptools --version
```

**就这么简单！**

---

## 📋 详细步骤

### 1. 确保有 Python

```bash
python --version  # 需要 Python 3.8+
```

### 2. 安装 CPTools

```bash
pip install git+https://github.com/joeyplanetart/cptool_cli.git
```

### 3. 安装浏览器驱动

```bash
playwright install chromium
```

### 4. 验证安装

```bash
cptools --version
cptools --help
```

---

## ✅ 快速测试

创建测试文件 `test.csv`：

```csv
url,name
https://www.baidu.com,百度首页
https://www.github.com,GitHub首页
```

运行测试：

```bash
cptools screenshot \
  --host http://example.com \
  --csv test.csv \
  --output ./test_screenshots \
  --html test_result.html
```

打开 `test_result.html` 查看结果！

---

## 🔄 更新版本

```bash
pip install --upgrade git+https://github.com/joeyplanetart/cptool_cli.git
```

---

## 🗑️ 卸载

```bash
pip uninstall cptools
```

---

## ❓ 遇到问题？

### 问题1: pip install 很慢

使用清华镜像：

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple \
  git+https://github.com/joeyplanetart/cptool_cli.git
```

### 问题2: 权限错误

使用 `--user` 参数：

```bash
pip install --user git+https://github.com/joeyplanetart/cptool_cli.git
```

### 问题3: cptools 命令找不到

检查 PATH 或使用：

```bash
python -m cptools --help
```

---

## 📖 完整文档

- 详细安装指南: [docs/guides/PIP_INSTALL.md](guides/PIP_INSTALL.md)
- 使用文档: [docs/README.md](README.md)
- GitHub: https://github.com/joeyplanetart/cptool_cli

---

**需要帮助？** 联系: Joeyz@planetart.com

