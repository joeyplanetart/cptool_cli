# 📚 文档地图

所有 Markdown 文档已重新组织到 `docs/` 目录下，按功能分类。

## 📂 新的文档结构

```
docs/
├── README.md                              # 📚 文档中心索引（从这里开始！）
│
├── getting-started/                       # 🚀 快速入门
│   ├── QUICKSTART.md                     # 5分钟快速开始
│   └── EXAMPLES.md                        # 实战示例集合
│
├── guides/                                # 📖 详细指南
│   ├── VENV_GUIDE.md                     # 虚拟环境完整教程
│   ├── TEST_GUIDE.md                     # 测试指南
│   └── GITHUB_UPLOAD.md                  # GitHub 上传指南
│
├── reference/                             # 📋 参考文档
│   └── CHEATSHEET.md                     # 命令速查表
│
└── development/                           # 🔧 开发文档
    ├── DEVELOPMENT.md                    # 开发者指南
    └── PROJECT_COMPLETE.md               # 项目架构说明
```

## 🎯 快速导航

### 我想...

| 需求 | 查看文档 |
|------|----------|
| 快速开始使用 | [docs/getting-started/QUICKSTART.md](docs/getting-started/QUICKSTART.md) |
| 查看使用示例 | [docs/getting-started/EXAMPLES.md](docs/getting-started/EXAMPLES.md) |
| 快速查命令 | [docs/reference/CHEATSHEET.md](docs/reference/CHEATSHEET.md) |
| 了解虚拟环境 | [docs/guides/VENV_GUIDE.md](docs/guides/VENV_GUIDE.md) |
| 测试功能 | [docs/guides/TEST_GUIDE.md](docs/guides/TEST_GUIDE.md) |
| 上传到 GitHub | [docs/guides/GITHUB_UPLOAD.md](docs/guides/GITHUB_UPLOAD.md) |
| 贡献代码 | [docs/development/DEVELOPMENT.md](docs/development/DEVELOPMENT.md) |
| 了解项目架构 | [docs/development/PROJECT_COMPLETE.md](docs/development/PROJECT_COMPLETE.md) |

## 📖 推荐阅读路径

### 新手路径
1. [README.md](README.md) - 项目概述
2. [docs/getting-started/QUICKSTART.md](docs/getting-started/QUICKSTART.md) - 快速开始
3. [docs/getting-started/EXAMPLES.md](docs/getting-started/EXAMPLES.md) - 实战示例
4. [docs/reference/CHEATSHEET.md](docs/reference/CHEATSHEET.md) - 常用命令

### 深度使用路径
1. [docs/guides/VENV_GUIDE.md](docs/guides/VENV_GUIDE.md) - 虚拟环境详解
2. [docs/guides/TEST_GUIDE.md](docs/guides/TEST_GUIDE.md) - 测试最佳实践
3. [docs/reference/CHEATSHEET.md](docs/reference/CHEATSHEET.md) - 完整参考

### 开发者路径
1. [docs/development/DEVELOPMENT.md](docs/development/DEVELOPMENT.md) - 开发指南
2. [docs/development/PROJECT_COMPLETE.md](docs/development/PROJECT_COMPLETE.md) - 架构设计
3. [docs/guides/GITHUB_UPLOAD.md](docs/guides/GITHUB_UPLOAD.md) - 版本管理

## 🔧 命令行快捷方式

```bash
# 查看文档中心
cat docs/README.md

# 查看快速开始
cat docs/getting-started/QUICKSTART.md

# 查看命令速查表
cat docs/reference/CHEATSHEET.md

# 查看所有文档列表
find docs -name "*.md" -type f
```

## 📱 移动端/在线查看

如果你将项目上传到 GitHub，所有文档都可以在线查看：

```
https://github.com/你的用户名/cptool_cli/tree/main/docs
```

## 🆕 文档更新日志

### 2024-12-28
- ✅ 重组所有文档到 `docs/` 目录
- ✅ 按功能分类：getting-started、guides、reference、development
- ✅ 创建文档中心索引 (docs/README.md)
- ✅ 更新主 README.md
- ✅ 更新 info.sh 脚本

## 💡 提示

- 所有旧的文档路径都已移到 `docs/` 下
- 如果你有书签或脚本引用旧路径，请更新
- 使用 `./info.sh` 查看项目信息和文档位置

---

**从这里开始**: [docs/README.md](docs/README.md)

