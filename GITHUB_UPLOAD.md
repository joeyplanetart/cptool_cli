# 如何上传到GitHub

## 方法1：通过命令行上传（推荐）

### 步骤1：在GitHub上创建新仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - Repository name: `cptool_cli`
   - Description: `基于Python的命令行工具集，提供网页截屏等实用功能`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"（因为我们本地已有文件）
3. 点击 "Create repository"

### 步骤2：关联远程仓库并推送

在项目目录执行以下命令：

```bash
# 关联远程仓库（替换 yourusername 为你的GitHub用户名）
git remote add origin https://github.com/yourusername/cptool_cli.git

# 重命名分支为 main（如果需要）
git branch -M main

# 推送代码到GitHub
git push -u origin main
```

### 步骤3：验证

访问 `https://github.com/yourusername/cptool_cli` 查看项目是否上传成功。

## 方法2：使用GitHub CLI

如果已安装 GitHub CLI (`gh`)：

```bash
# 登录GitHub（如果还没登录）
gh auth login

# 创建仓库并推送
gh repo create cptool_cli --public --source=. --remote=origin --push
```

## 方法3：使用GitHub Desktop

1. 下载并安装 [GitHub Desktop](https://desktop.github.com/)
2. 打开 GitHub Desktop
3. 点击 File → Add Local Repository
4. 选择项目目录 `/Users/joey/cptool_cli`
5. 点击 "Publish repository" 按钮
6. 填写仓库信息并发布

## 后续更新

当你修改了代码后，可以通过以下命令更新到GitHub：

```bash
# 查看修改状态
git status

# 添加修改的文件
git add .

# 提交修改
git commit -m "描述你的修改"

# 推送到GitHub
git push
```

## 常见问题

### Q: 推送时提示 "Authentication failed"

A: 使用以下两种方式之一：

**方式1：使用Personal Access Token**

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择 `repo` 权限
4. 生成token并复制
5. 推送时使用token作为密码：
   ```bash
   git push
   # Username: 你的GitHub用户名
   # Password: 粘贴你的token
   ```

**方式2：使用SSH**

```bash
# 生成SSH密钥（如果还没有）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 将公钥添加到GitHub
cat ~/.ssh/id_ed25519.pub
# 复制输出内容，到 https://github.com/settings/keys 添加

# 修改远程仓库地址为SSH格式
git remote set-url origin git@github.com:yourusername/cptool_cli.git

# 推送
git push -u origin main
```

### Q: 推送时提示 "rejected"

A: 可能是远程仓库有更新，先拉取：

```bash
git pull origin main --rebase
git push origin main
```

### Q: 如何更新README中的GitHub链接

A: 修改以下文件：

1. `README.md` - 更新克隆URL
2. `setup.py` - 更新 `url` 字段

```bash
# 批量替换（替换 yourusername 为你的用户名）
sed -i '' 's/yourusername/你的GitHub用户名/g' README.md setup.py

# 提交修改
git add README.md setup.py
git commit -m "Update GitHub URLs"
git push
```

## 完整命令示例

假设你的GitHub用户名是 `joey`：

```bash
# 进入项目目录
cd /Users/joey/cptool_cli

# 关联远程仓库
git remote add origin https://github.com/joey/cptool_cli.git

# 或使用SSH（推荐）
git remote add origin git@github.com:joey/cptool_cli.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

## 添加徽章到README（可选）

在GitHub上传成功后，可以在 `README.md` 顶部添加徽章：

```markdown
# CPTools - 命令行工具集

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GitHub Stars](https://img.shields.io/github/stars/yourusername/cptool_cli.svg)

...
```

