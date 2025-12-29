# CPTools 文档中心

欢迎来到 CPTools 文档！本文档将帮助你快速上手并深入了解 CPTools 的各项功能。

## 📚 文档导航

### 🚀 快速入门

新用户从这里开始：

- **[快速开始指南](getting-started/QUICKSTART.md)** - 5分钟快速上手截屏功能
  - 一键安装脚本
  - 基本使用方法
  - 常见问题解答

- **[URL404 快速开始](getting-started/URL404_QUICKSTART.md)** - 5分钟快速上手 URL 检测
  - URL 检测基础
  - 使用示例
  - 报告解读

- **[使用示例](getting-started/EXAMPLES.md)** - 丰富的实战示例
  - 基本截图示例
  - 高级配置示例
  - 批量处理脚本
  - Python 调用示例
  - 定时任务设置

### 📖 详细指南

深入了解各项功能：

- **[安装指南](guides/INSTALL.md)** - 完整的安装说明
  - 各平台安装方法
  - 依赖说明
  - 故障排除

- **[URL404 使用指南](guides/URL404.md)** - URL 404检测完整教程
  - 功能概述
  - 命令参数
  - 使用示例
  - HTML 报告详解
  - 常见问题

- **[虚拟环境指南](guides/VENV_GUIDE.md)** - 虚拟环境完整教程
  - 什么是虚拟环境
  - 创建和管理
  - 故障排除
  - 最佳实践

- **[测试指南](guides/TEST_GUIDE.md)** - 如何测试你的任务
  - 测试脚本使用
  - 配置建议
  - 问题诊断

- **[GitHub 上传指南](guides/GITHUB_UPLOAD.md)** - 将项目上传到 GitHub
  - 创建仓库
  - 推送代码
  - 常见问题

- **[Pip 安装指南](guides/PIP_INSTALL.md)** - 让同事通过 pip 安装
  - 从 GitHub 安装
  - 本地文件安装
  - 发布到 PyPI
  - 企业内部部署

### 📋 参考文档

快速查找命令和参数：

- **[命令速查表](reference/CHEATSHEET.md)** - 所有命令的快速参考
  - 命令参数表
  - 常用场景
  - 故障排除
  - 最佳实践

- **[HTML报告模板](reference/TEMPLATES.md)** - HTML报告模板指南
  - 可用模板介绍
  - 模板对比
  - 使用示例
  - 自定义模板

- **[反爬虫机制](reference/ANTI_CRAWLER.md)** - 反爬虫策略和优化
  - 已实现的机制
  - 参数调优建议
  - 最佳实践
  - 风险提示

### 🔧 开发文档

为 CPTools 贡献代码：

- **[开发指南](development/DEVELOPMENT.md)** - 开发者文档
  - 项目结构
  - 添加新命令
  - 代码规范
  - 调试技巧
  - 性能优化

- **[项目完成说明](development/PROJECT_COMPLETE.md)** - 项目架构和特性说明
  - 功能特性
  - 架构设计
  - 技术选型

- **[URL404 开发总结](development/URL404_SUMMARY.md)** - URL404 功能开发文档
  - 功能实现细节
  - 技术要点
  - 设计思路

### 📄 其他文档

- **[文档地图](DOCUMENTATION_MAP.md)** - 完整的文档结构索引

## 🎯 根据你的需求选择

### 我是新用户，想快速开始
👉 从 [快速开始指南](getting-started/QUICKSTART.md) 开始

### 我想检测 URL 状态码
👉 查看 [URL404 快速开始](getting-started/URL404_QUICKSTART.md)

### 我想看实际的使用案例
👉 查看 [使用示例](getting-started/EXAMPLES.md)

### 我遇到了问题
👉 查看 [命令速查表](reference/CHEATSHEET.md) 的故障排除部分

### 我想深入了解虚拟环境
👉 阅读 [虚拟环境指南](guides/VENV_GUIDE.md)

### 我想贡献代码
👉 参考 [开发指南](development/DEVELOPMENT.md)

### 我需要快速查命令
👉 使用 [命令速查表](reference/CHEATSHEET.md)

## 📱 快速命令参考

```bash
# 查看版本
cptools --version

# 查看帮助
cptools --help
cptools screenshot --help
cptools url404 --help

# 截屏
cptools screenshot \
  --host http://example.com \
  --csv data.csv \
  -c 10

# URL检测
cptools url404 \
  --host http://example.com \
  --csv data.csv \
  -c 10
```

## 🔗 外部资源

- **GitHub 仓库**: https://github.com/joeyplanetart/cptool_cli
- **Playwright 文档**: https://playwright.dev/python/
- **Python venv 文档**: https://docs.python.org/3/library/venv.html

## 💡 提示

- 所有命令都需要在激活虚拟环境后运行
- 使用 Tab 键可以自动补全命令
- 遇到问题先查看日志文件

---

**版本**: 1.1.0  
**最后更新**: 2024-12-29
