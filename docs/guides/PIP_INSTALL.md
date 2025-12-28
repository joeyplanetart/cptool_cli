# Pip 安装指南

这个文档教你如何让同事通过 pip 安装 CPTools。

## 🎯 安装方式概览

有 4 种方式可以让同事安装 CPTools：

| 方式 | 难度 | 适用场景 |
|------|------|----------|
| [方式1: 从 GitHub 安装](#方式1从-github-安装推荐) | ⭐ 简单 | 项目已上传到 GitHub |
| [方式2: 从本地文件安装](#方式2从本地文件安装) | ⭐⭐ 中等 | 内网或无法访问 GitHub |
| [方式3: 发布到 PyPI](#方式3发布到-pypi官方) | ⭐⭐⭐ 复杂 | 公开发布，最专业 |
| [方式4: 私有 PyPI 服务器](#方式4私有-pypi-服务器企业用) | ⭐⭐⭐⭐ 很复杂 | 企业内部使用 |

---

## 方式1：从 GitHub 安装（推荐）

### 前提条件
- 项目已上传到 GitHub
- 仓库地址：`https://github.com/joeyplanetart/cptool_cli`

### 安装步骤

**同事执行以下命令：**

```bash
# 方法 A: 直接从 GitHub 安装
pip install git+https://github.com/joeyplanetart/cptool_cli.git

# 方法 B: 安装特定分支
pip install git+https://github.com/joeyplanetart/cptool_cli.git@main

# 方法 C: 安装特定版本（tag）
pip install git+https://github.com/joeyplanetart/cptool_cli.git@v1.0.0

# 安装后安装 Playwright 浏览器
playwright install chromium

# 验证安装
cptools --version
```

### 一键安装脚本

创建 `install.sh` 给同事：

```bash
#!/bin/bash
echo "开始安装 CPTools..."

# 安装包
pip install git+https://github.com/joeyplanetart/cptool_cli.git

# 安装 Playwright 浏览器
playwright install chromium

# 验证
cptools --version

echo "安装完成！运行 'cptools --help' 查看帮助"
```

使用方法：
```bash
chmod +x install.sh
./install.sh
```

---

## 方式2：从本地文件安装

### 适用场景
- 内网环境无法访问 GitHub
- 需要离线安装
- 快速测试

### 步骤

#### 第一步：打包项目

在你的电脑上执行：

```bash
# 进入项目目录
cd /Users/joey/cptool_cli

# 创建分发包
python setup.py sdist bdist_wheel

# 会生成 dist 目录，包含：
# - cptools-1.0.0.tar.gz
# - cptools-1.0.0-py3-none-any.whl
```

如果没有 wheel，先安装：
```bash
pip install wheel
```

#### 第二步：传给同事

将 `dist` 目录打包发给同事：

```bash
# 创建完整安装包（包含依赖）
tar -czf cptools-install.tar.gz dist/ requirements.txt

# 或者只打包必要文件
zip -r cptools-install.zip dist/ requirements.txt
```

#### 第三步：同事安装

同事收到文件后：

```bash
# 解压
tar -xzf cptools-install.tar.gz
# 或
unzip cptools-install.zip

# 安装依赖
pip install -r requirements.txt

# 安装 CPTools
pip install dist/cptools-1.0.0-py3-none-any.whl
# 或
pip install dist/cptools-1.0.0.tar.gz

# 安装 Playwright 浏览器
playwright install chromium

# 验证
cptools --version
```

---

## 方式3：发布到 PyPI（官方）

### 适用场景
- 希望公开发布
- 方便全世界开发者使用
- 最专业的分发方式

### 步骤

#### 1. 注册 PyPI 账号

访问 https://pypi.org/ 注册账号

#### 2. 安装发布工具

```bash
pip install build twine
```

#### 3. 更新项目信息

确保 `setup.py` 中的信息正确：

```python
setup(
    name="cptools",  # 包名（需要在 PyPI 上唯一）
    version="1.0.0",
    author="Joey Zhou",
    author_email="Joeyz@planetart.com",
    description="命令行工具集，包含截屏等功能",
    url="https://github.com/joeyplanetart/cptool_cli",
    # ...
)
```

#### 4. 构建分发包

```bash
python -m build
```

#### 5. 上传到 PyPI

```bash
# 上传到 PyPI（会要求输入用户名和密码）
twine upload dist/*

# 或使用 API token（更安全）
twine upload --repository pypi dist/* -u __token__ -p pypi-你的token
```

#### 6. 同事安装

上传成功后，任何人都可以直接安装：

```bash
pip install cptools
playwright install chromium
cptools --version
```

### 注意事项

⚠️ **重要提醒：**
1. 包名必须在 PyPI 上唯一
2. 版本号不能重复上传
3. 一旦发布无法删除，只能标记为 yanked
4. 建议先发布到 TestPyPI 测试

#### 发布到 TestPyPI（测试）

```bash
# 注册 TestPyPI 账号：https://test.pypi.org/

# 上传到 TestPyPI
twine upload --repository testpypi dist/*

# 从 TestPyPI 安装测试
pip install --index-url https://test.pypi.org/simple/ cptools
```

---

## 方式4：私有 PyPI 服务器（企业用）

### 适用场景
- 企业内部使用
- 不想公开发布
- 需要权限控制

### 选项

#### A. 使用 devpi（简单）

```bash
# 服务器端安装 devpi
pip install devpi-server devpi-web
devpi-init
devpi-server --start

# 上传包
devpi use http://localhost:3141
devpi user -c 用户名 password=密码
devpi login 用户名 --password=密码
devpi upload dist/*

# 客户端安装
pip install --index-url http://localhost:3141/用户名/dev cptools
```

#### B. 使用文件服务器

```bash
# 在服务器上创建简单的 PyPI 索引
pip install pypiserver
pypiserver -p 8080 /path/to/packages/

# 客户端安装
pip install --index-url http://服务器IP:8080/simple/ cptools
```

---

## 📝 推荐的安装文档

为同事创建一个简单的安装文档 `INSTALL.md`：

```markdown
# CPTools 安装指南

## 快速安装

### 从 GitHub 安装（推荐）

\`\`\`bash
# 1. 安装 CPTools
pip install git+https://github.com/joeyplanetart/cptool_cli.git

# 2. 安装 Playwright 浏览器
playwright install chromium

# 3. 验证安装
cptools --version
\`\`\`

## 使用方法

\`\`\`bash
cptools screenshot --host http://example.com --csv data.csv
\`\`\`

## 查看帮助

\`\`\`bash
cptools --help
cptools screenshot --help
\`\`\`

## 需要帮助？

查看完整文档：https://github.com/joeyplanetart/cptool_cli
```

---

## 🔧 卸载

如果需要卸载：

```bash
pip uninstall cptools
```

---

## 🆘 常见问题

### Q: pip install 速度很慢？

**A: 使用国内镜像**

```bash
# 临时使用
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple git+https://github.com/joeyplanetart/cptool_cli.git

# 永久配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: 权限错误？

**A: 使用 --user 参数**

```bash
pip install --user git+https://github.com/joeyplanetart/cptool_cli.git
```

### Q: 需要升级版本？

**A: 使用 --upgrade 参数**

```bash
pip install --upgrade git+https://github.com/joeyplanetart/cptool_cli.git
```

### Q: 想指定安装位置？

**A: 使用 --target 参数**

```bash
pip install --target=/path/to/directory git+https://github.com/joeyplanetart/cptool_cli.git
```

---

## 📦 完整的部署检查清单

发布前确认：

- [ ] `setup.py` 信息完整准确
- [ ] `requirements.txt` 包含所有依赖
- [ ] `README.md` 有清晰的说明
- [ ] GitHub 仓库设为公开（如果从 GitHub 安装）
- [ ] 测试在干净环境中安装
- [ ] 文档中的 GitHub URL 已更新
- [ ] 版本号正确

---

## 💡 最佳实践建议

### 开发阶段
- 使用 `pip install -e .` 可编辑模式
- 同事使用从 GitHub 安装

### 生产阶段
- 使用语义化版本号（1.0.0, 1.1.0, 2.0.0）
- 发布到 PyPI
- 使用 GitHub Releases 管理版本

### 企业内部
- 搭建私有 PyPI 服务器
- 或使用文件共享 + 本地安装

---

**下一步**: 选择适合你团队的安装方式，创建对应的安装文档！

