# HTML 报告模板

CPTools 提供了多种 HTML 报告模板供选择，每种模板都有独特的风格和布局。

## 📋 可用模板

### 1. Default（默认模板）

**风格**: 现代渐变风格，视觉效果出色

**特点**:
- 🎨 紫色渐变背景
- 📱 响应式卡片布局
- ✨ 悬停动画效果
- 🖼️ 大图预览
- 📊 直观的统计卡片

**适用场景**: 
- 正式的项目报告
- 需要展示给客户或管理层
- 强调视觉效果

**使用方法**:
```bash
cptools screenshot --host http://example.com --csv data.csv --template default
# 或者不指定（默认就是 default）
cptools screenshot --host http://example.com --csv data.csv
```

### 2. Terminal（终端风格）

**风格**: 黑客/终端风格，绿色矩阵主题

**特点**:
- 💻 黑色背景，绿色文字
- ⚡ 终端/命令行风格
- 📋 列表式布局
- 🔢 等宽字体
- 🎯 高对比度

**适用场景**:
- 技术团队内部使用
- 喜欢命令行/终端风格
- 深色主题爱好者

**使用方法**:
```bash
cptools screenshot --host http://example.com --csv data.csv --template terminal
```

### 3. Minimal（简约风格）

**风格**: 极简主义，专注内容

**特点**:
- 🎯 简洁的设计
- ⚪ 白色背景
- 📐 清晰的排版
- 🔍 突出重点信息
- 💡 无干扰的阅读体验

**适用场景**:
- 注重内容而非装饰
- 快速浏览报告
- 打印输出

**使用方法**:
```bash
cptools screenshot --host http://example.com --csv data.csv --template minimal
```

## 🎨 模板对比

| 特性 | Default | Terminal | Minimal |
|------|---------|----------|---------|
| 风格 | 现代渐变 | 黑客终端 | 极简主义 |
| 颜色 | 紫色渐变 | 黑绿色 | 灰白色 |
| 布局 | 网格卡片 | 列表 | 网格卡片 |
| 适合场景 | 正式报告 | 技术团队 | 快速查看 |
| 视觉冲击 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 信息密度 | 中 | 高 | 中 |

## 📸 模板预览

### Default 模板
```
┌─────────────────────────────────────┐
│     📸 截屏报告                      │
│  生成时间: 2024-12-28 15:30:00      │
│  ┌────────┐ ┌────────┐ ┌────────┐  │
│  │ 总数: 100│ │成功: 95│ │失败: 5 │  │
│  └────────┘ └────────┘ └────────┘  │
│                                     │
│  ┌─────┐ ┌─────┐ ┌─────┐          │
│  │ IMG │ │ IMG │ │ IMG │          │
│  │     │ │     │ │     │          │
│  └─────┘ └─────┘ └─────┘          │
└─────────────────────────────────────┘
```

### Terminal 模板
```
╔═══════════════════════════════════════╗
║  ▲ 截屏报告 ▲                         ║
║  > 生成时间: 2024-12-28 15:30:00      ║
╠═══════════════════════════════════════╣
║  [IMG] | 页面名称 | URL... | SUCCESS  ║
║  [IMG] | 页面名称 | URL... | SUCCESS  ║
║  [ERR] | 页面名称 | URL... | FAILED   ║
╚═══════════════════════════════════════╝
```

### Minimal 模板
```
┌─────────────────────────────────────┐
│         截屏报告                     │
│      2024-12-28 15:30:00            │
│                                     │
│   总数: 100  成功: 95  失败: 5      │
│                                     │
│  ┌─────┐ ┌─────┐ ┌─────┐          │
│  │ IMG │ │ IMG │ │ IMG │          │
│  └─────┘ └─────┘ └─────┘          │
└─────────────────────────────────────┘
```

## 🔧 完整使用示例

### 基本使用
```bash
# 使用默认模板
cptools screenshot \
  --host http://example.com \
  --csv data.csv \
  --html result.html

# 使用终端模板
cptools screenshot \
  --host http://example.com \
  --csv data.csv \
  --html result.html \
  --template terminal

# 使用简约模板
cptools screenshot \
  --host http://example.com \
  --csv data.csv \
  --html result.html \
  --template minimal
```

### 高级配置
```bash
# 完整配置 + 终端模板
cptools screenshot \
  --host http://example.com \
  --csv data.csv \
  --output ./screenshots \
  --log ./log.log \
  --html ./report.html \
  --template terminal \
  -c 10 \
  --width 1920 \
  --height 1080
```

## 💡 选择建议

### 何时使用 Default 模板？
- ✅ 需要展示给非技术人员
- ✅ 重视视觉效果
- ✅ 正式场合或客户演示
- ✅ 需要打动观众

### 何时使用 Terminal 模板？
- ✅ 技术团队内部使用
- ✅ 喜欢命令行/终端美学
- ✅ 需要快速扫描大量结果
- ✅ 深色主题环境

### 何时使用 Minimal 模板？
- ✅ 注重内容而非形式
- ✅ 需要打印输出
- ✅ 快速查看测试结果
- ✅ 性能考虑（文件更小）

## 🎯 特殊功能

所有模板都支持以下功能：

### 图片预览
- 点击任意截图可以全屏预览
- 按 ESC 键关闭预览
- 支持缩放和查看细节

### 响应式设计
- 自动适应不同屏幕尺寸
- 移动设备友好
- 支持触摸操作

### 状态标识
- ✅ 成功状态（绿色）
- ❌ 失败状态（红色）
- 清晰的错误信息显示

## 📂 模板文件位置

所有模板文件位于：
```
cptools/templates/
├── default.html      # 默认模板
├── terminal.html     # 终端模板
└── minimal.html      # 简约模板
```

## 🔨 自定义模板

你可以复制现有模板并进行修改：

1. 复制一个模板文件
2. 修改样式和布局
3. 保存为新文件名
4. 使用 `--template 新文件名` 参数

模板使用简单的变量替换系统：
- `{{ title }}` - 报告标题
- `{{ timestamp }}` - 生成时间
- `{{ total }}` - 总数
- `{{ success }}` - 成功数
- `{{ failed }}` - 失败数
- `{{ results_html }}` - 结果列表

## 🆘 故障排除

### 模板不存在
如果指定的模板不存在，系统会自动回退到内置的默认模板。

```bash
# 如果 custom 模板不存在，会使用默认模板
cptools screenshot ... --template custom
# 输出: 警告: 模板 'custom' 不存在，使用默认模板
```

### 查看可用模板
```bash
ls cptools/templates/
# 或
find cptools/templates -name "*.html"
```

## 📊 性能对比

| 模板 | 文件大小 | 加载速度 | 内存占用 |
|------|----------|----------|----------|
| Default | ~15KB | 快 | 低 |
| Terminal | ~13KB | 最快 | 最低 |
| Minimal | ~10KB | 很快 | 很低 |

*注: 以上数据基于100个结果项的测试*

---

**需要帮助？** 查看 [完整文档](../README.md) 或运行 `cptools screenshot --help`

