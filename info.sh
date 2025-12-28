#!/bin/bash

# 显示项目信息和快速帮助

cat << 'EOF'
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ██████╗██████╗ ████████╗ ██████╗  ██████╗ ██╗     ███████╗   ║
║  ██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝   ║
║  ██║     ██████╔╝   ██║   ██║   ██║██║   ██║██║     ███████╗   ║
║  ██║     ██╔═══╝    ██║   ██║   ██║██║   ██║██║     ╚════██║   ║
║  ╚██████╗██║        ██║   ╚██████╔╝╚██████╔╝███████╗███████║   ║
║   ╚═════╝╚═╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝   ║
║                                                                  ║
║           命令行工具集 - 网页截屏工具                             ║
║                     Version 1.0.0                                ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

📦 项目信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  名称: CPTools
  版本: 1.0.0
  作者: Joey Zhou
  邮箱: Joeyz@planetart.com
  许可: MIT License
  位置: $(pwd)

🚀 快速开始
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  
  首次使用:
    1. 运行自动安装: ./setup_venv.sh
    2. 等待安装完成
    3. 开始使用！

  日常使用:
    1. 激活环境: source venv/bin/activate
    2. 运行命令: cptools screenshot --help
    3. 退出环境: deactivate

📋 常用命令
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # 查看帮助
  cptools --help
  cptools screenshot --help

  # 基本截图
  cptools screenshot \\
    --host http://example.com \\
    --csv data.csv \\
    --log log.log \\
    --html result.html

  # 高级选项
  cptools screenshot \\
    --host http://example.com \\
    --csv data.csv \\
    --output ./screenshots \\
    -c 10 \\
    --width 1920 \\
    --height 1080 \\
    --dingding-webhook <URL>

📚 文档说明
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  README.md                              - 项目概述和快速开始
  docs/README.md                         - 📚 文档中心（推荐！）
  
  快速入门：
    docs/getting-started/QUICKSTART.md   - 快速开始指南
    docs/getting-started/EXAMPLES.md     - 丰富的使用示例
  
  详细指南：
    docs/guides/VENV_GUIDE.md            - 虚拟环境详细指南
    docs/guides/TEST_GUIDE.md            - 测试指南
    docs/guides/GITHUB_UPLOAD.md         - GitHub上传指南
  
  参考文档：
    docs/reference/CHEATSHEET.md         - 常用命令速查表
  
  开发文档：
    docs/development/DEVELOPMENT.md      - 开发者文档
    docs/development/PROJECT_COMPLETE.md - 项目完成说明

🔧 脚本工具
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ./setup_venv.sh    - 自动安装脚本（Linux/Mac）
  setup_venv.bat     - 自动安装脚本（Windows）
  ./test.sh          - 环境测试脚本
  ./info.sh          - 显示本帮助信息

📁 项目结构
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  cptools/
  ├── cli.py              # 命令行入口
  ├── commands/
  │   └── screenshot.py   # 截屏命令
  └── utils/
      ├── logger.py       # 日志工具
      ├── html_report.py  # HTML报告
      └── dingding.py     # 钉钉通知

🎯 主要特性
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✓ 基于Playwright的高质量截图
  ✓ 异步并发，高效快速
  ✓ 支持相对路径和完整URL
  ✓ 精美的HTML可视化报告
  ✓ 完整的日志记录
  ✓ 钉钉通知集成
  ✓ 自定义浏览器窗口大小
  ✓ 虚拟环境管理
  ✓ 一键安装部署

🆘 常见问题
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Q: cptools命令找不到？
  A: source venv/bin/activate && pip install -e .

  Q: Playwright浏览器找不到？
  A: playwright install chromium

  Q: 如何更新代码？
  A: git pull && source venv/bin/activate && pip install -e .

  Q: 虚拟环境出问题？
  A: rm -rf venv && ./setup_venv.sh

  Q: 需要更多帮助？
  A: 查看 docs/README.md（文档中心）或 docs/reference/CHEATSHEET.md（快速参考）

📞 获取帮助
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  运行测试: ./test.sh
  查看文档: less CHEATSHEET.md
  GitHub: https://github.com/yourusername/cptool_cli

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF

# 检查虚拟环境状态
echo ""
if [ -d "venv" ]; then
    echo "✓ 虚拟环境已创建"
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "✓ 虚拟环境已激活: $VIRTUAL_ENV"
    else
        echo "⚠️  虚拟环境未激活，运行: source venv/bin/activate"
    fi
else
    echo "⚠️  虚拟环境未创建，运行: ./setup_venv.sh"
fi

echo ""
echo "查看文档中心: cat docs/README.md"
echo "查看命令速查: cat docs/reference/CHEATSHEET.md"
echo ""

