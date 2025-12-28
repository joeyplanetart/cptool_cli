# CPTools 更新日志

## 版本 1.1.0 - 2024-12-28

### 🎨 新增 HTML 报告模板系统

我们为 CPTools 添加了功能强大的 HTML 报告模板系统！现在你可以根据不同场景选择不同风格的报告模板。

#### ✨ 新增功能

1. **三种精美模板**
   - **Default** - 现代渐变风格，紫色主题，适合正式场合
   - **Terminal** - 黑客终端风格，绿色矩阵主题，适合技术团队
   - **Minimal** - 极简主义风格，白色主题，专注内容

2. **图片预览功能**
   - 点击任意截图可全屏预览
   - 支持 ESC 键快速关闭
   - 所有模板均支持

3. **响应式设计**
   - 自适应不同屏幕尺寸
   - 移动设备友好
   - 支持触摸操作

#### 🚀 使用方法

```bash
# 使用默认模板
cptools screenshot --host http://example.com --csv data.csv

# 使用终端模板
cptools screenshot --host http://example.com --csv data.csv --template terminal

# 使用简约模板  
cptools screenshot --host http://example.com --csv data.csv --template minimal
```

#### 📂 新增文件

```
cptools/
├── templates/              # 新增 - 模板目录
│   ├── default.html       # 默认模板
│   ├── terminal.html      # 终端模板
│   └── minimal.html       # 简约模板
└── utils/
    └── html_report.py     # 更新 - 支持模板系统

docs/
└── reference/
    └── TEMPLATES.md       # 新增 - 模板使用文档
```

#### 🔧 更新的命令参数

```bash
cptools screenshot [选项]

新增参数:
  --template [default|terminal|minimal]  HTML报告模板（默认：default）
```

#### 📖 文档

详细的模板使用指南请查看：
- [模板文档](docs/reference/TEMPLATES.md)
- [命令速查表](docs/reference/CHEATSHEET.md)

---

## 版本 1.0.1 - 2024-12-28

### 📚 文档重组

将所有 Markdown 文档移动到 `docs/` 目录并进行分类：

```
docs/
├── README.md              # 文档中心索引
├── getting-started/       # 快速入门
├── guides/               # 详细指南
├── reference/            # 参考文档
└── development/          # 开发文档
```

### ⚡ 参数优化

- 将 `--concurrency` 的短选项从 `-n` 改为 `-c`
- 移除 `--csv` 的短选项以避免冲突
- 统一命令行参数风格

---

## 版本 1.0.0 - 2024-12-27

### 🎉 首次发布

基于 Playwright 的网页截屏工具，支持：
- 异步并发截图
- HTML 可视化报告
- 钉钉通知集成
- 完整的日志记录
- 虚拟环境管理

---

**查看完整文档**: [docs/README.md](docs/README.md)

