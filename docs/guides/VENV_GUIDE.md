# Python虚拟环境（venv）使用指南

## 什么是虚拟环境？

虚拟环境是Python项目的独立运行环境，它可以：
- 隔离项目依赖，避免不同项目间的包冲突
- 保持系统Python环境的干净
- 方便在不同机器上复制相同的开发环境
- 便于管理项目依赖版本

## 快速开始

### 自动创建（推荐）

使用提供的脚本一键创建和配置虚拟环境：

```bash
# Linux/Mac
./setup_venv.sh

# Windows
setup_venv.bat
```

### 手动创建

```bash
# Linux/Mac
python3 -m venv venv

# Windows
python -m venv venv
```

## 常用命令

### 激活虚拟环境

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows (CMD):**
```bash
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

激活成功后，命令行提示符前会显示 `(venv)`：
```bash
(venv) user@computer:~/cptool_cli$
```

### 退出虚拟环境

```bash
deactivate
```

### 查看当前环境

```bash
# 查看Python路径（应该指向venv目录）
which python    # Linux/Mac
where python    # Windows

# 查看已安装的包
pip list

# 查看某个包的信息
pip show playwright
```

### 安装依赖

激活虚拟环境后：

```bash
# 从requirements.txt安装
pip install -r requirements.txt

# 安装单个包
pip install package_name

# 以开发模式安装当前项目
pip install -e .
```

### 导出依赖

```bash
# 导出当前环境的所有包
pip freeze > requirements.txt

# 仅导出项目直接依赖（推荐）
pip list --format=freeze > requirements.txt
```

## 工作流程

### 日常开发

```bash
# 1. 进入项目目录
cd /Users/joey/cptool_cli

# 2. 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 3. 使用cptools
cptools screenshot --help

# 4. 完成工作后退出
deactivate
```

### 添加新依赖

```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 安装新包
pip install new-package

# 3. 更新requirements.txt
pip freeze > requirements.txt

# 4. 提交更改
git add requirements.txt
git commit -m "Add new-package dependency"
```

### 在新机器上部署

```bash
# 1. 克隆项目
git clone <repository-url>
cd cptool_cli

# 2. 创建虚拟环境
python3 -m venv venv

# 3. 激活虚拟环境
source venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt
pip install -e .

# 5. 安装Playwright浏览器
playwright install chromium
```

## 常见问题

### Q: 为什么要使用虚拟环境？

A: 
- **隔离性**: 不同项目可能需要同一个包的不同版本
- **干净性**: 不会污染系统Python环境
- **可复制性**: 便于在不同机器上复制环境
- **安全性**: 避免不小心升级系统包导致系统工具损坏

### Q: venv目录可以删除吗？

A: 可以！虚拟环境是可以随时删除和重建的。如果环境出问题，直接：

```bash
rm -rf venv              # Linux/Mac
rmdir /s /q venv        # Windows

# 然后重新创建
./setup_venv.sh
```

### Q: venv目录需要提交到Git吗？

A: **不需要！** `.gitignore`文件已经包含了`venv/`，虚拟环境不应该提交到版本控制。只需提交`requirements.txt`，其他人可以根据它重建环境。

### Q: 忘记激活虚拟环境会怎样？

A: 
- `cptools`命令可能找不到
- 或者会使用系统的Python和包
- 可能会将包安装到系统Python中

**检查方法：**
```bash
# 查看Python路径
which python  # 应该显示 .../cptool_cli/venv/bin/python
```

### Q: 如何在IDE中使用虚拟环境？

A: 

**VS Code:**
1. 打开项目
2. 按 `Cmd/Ctrl + Shift + P`
3. 输入 "Python: Select Interpreter"
4. 选择 `./venv/bin/python`

**PyCharm:**
1. File → Settings → Project → Python Interpreter
2. 点击齿轮图标 → Add
3. 选择 Existing Environment
4. 选择 `venv/bin/python`

### Q: Windows PowerShell提示无法运行脚本？

A: 这是PowerShell的执行策略限制。解决方法：

```powershell
# 临时允许（当前会话）
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 然后激活
venv\Scripts\Activate.ps1
```

或者直接使用CMD而不是PowerShell。

### Q: 虚拟环境占用多少空间？

A: 通常100-500MB，取决于安装的包。对于本项目：
- Python基础: ~20MB
- 项目依赖: ~50MB
- Playwright浏览器: ~200MB
- 总计约: ~300MB

### Q: 可以有多个虚拟环境吗？

A: 可以！你可以创建多个虚拟环境用于不同目的：

```bash
python3 -m venv venv-dev      # 开发环境
python3 -m venv venv-test     # 测试环境
python3 -m venv venv-prod     # 生产环境
```

## 高级技巧

### 1. 使用不同Python版本

```bash
# 指定Python版本创建虚拟环境
python3.9 -m venv venv39
python3.10 -m venv venv310
```

### 2. 复制虚拟环境

```bash
# 不推荐直接复制目录，应该重建
pip freeze > requirements_backup.txt
python3 -m venv venv_new
source venv_new/bin/activate
pip install -r requirements_backup.txt
```

### 3. 清理虚拟环境

```bash
# 激活环境后
pip freeze | xargs pip uninstall -y  # 卸载所有包
pip install -r requirements.txt      # 重新安装
```

### 4. 快捷命令（可选）

在 `~/.bashrc` 或 `~/.zshrc` 中添加别名：

```bash
# 添加别名
alias venv-activate='source venv/bin/activate'
alias venv-create='python3 -m venv venv'
alias venv-install='pip install -r requirements.txt'

# 使用
venv-activate
```

## 最佳实践

1. **总是使用虚拟环境** - 每个项目一个独立环境
2. **不要提交venv目录** - 已在`.gitignore`中排除
3. **及时更新requirements.txt** - 添加新依赖后立即更新
4. **文档化Python版本** - 在README中说明需要的Python版本
5. **激活后再工作** - 养成先激活虚拟环境的习惯

## 故障排除

### 问题：cptools命令找不到

```bash
# 检查虚拟环境是否激活
echo $VIRTUAL_ENV  # 应该显示venv路径

# 重新安装
pip install -e .
```

### 问题：Playwright浏览器找不到

```bash
# 重新安装浏览器
playwright install chromium

# 或指定路径
PLAYWRIGHT_BROWSERS_PATH=0 playwright install chromium
```

### 问题：依赖冲突

```bash
# 删除虚拟环境重建
rm -rf venv
./setup_venv.sh
```

## 参考资源

- [Python官方文档 - venv](https://docs.python.org/3/library/venv.html)
- [pip用户指南](https://pip.pypa.io/en/stable/user_guide/)
- [虚拟环境和包管理](https://docs.python.org/zh-cn/3/tutorial/venv.html)

## 总结

使用虚拟环境是Python开发的最佳实践：

```bash
# 三步走
1. 创建: python3 -m venv venv
2. 激活: source venv/bin/activate
3. 使用: cptools screenshot ...
```

记住：**激活虚拟环境是使用CPTools的第一步！**

