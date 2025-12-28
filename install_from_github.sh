#!/bin/bash

# CPTools 一键安装脚本
# 适用于 Linux/Mac

set -e  # 遇到错误立即退出

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                  CPTools 一键安装脚本                             ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# 检查 Python
echo "1️⃣  检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    echo "   请先安装 Python 3.8 或更高版本"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION"
echo ""

# 检查 pip
echo "2️⃣  检查 pip..."
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ 错误: 未找到 pip"
    exit 1
fi

PIP_CMD="pip3"
if command -v pip &> /dev/null; then
    PIP_CMD="pip"
fi
echo "✅ pip 可用"
echo ""

# 询问是否使用镜像
echo "3️⃣  选择安装源..."
echo "   1) 默认 (PyPI)"
echo "   2) 清华镜像 (推荐，国内快)"
echo "   3) 阿里镜像"
read -p "请选择 [1-3, 默认 2]: " choice
choice=${choice:-2}

PIP_INDEX=""
case $choice in
    1)
        echo "使用默认 PyPI 源"
        ;;
    2)
        PIP_INDEX="-i https://pypi.tuna.tsinghua.edu.cn/simple"
        echo "使用清华镜像源"
        ;;
    3)
        PIP_INDEX="-i https://mirrors.aliyun.com/pypi/simple/"
        echo "使用阿里镜像源"
        ;;
esac
echo ""

# 安装 CPTools
echo "4️⃣  安装 CPTools..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 这里需要替换为你的 GitHub 仓库地址
GITHUB_URL="https://github.com/joeyplanetart/cptool_cli.git"

if $PIP_CMD install $PIP_INDEX git+$GITHUB_URL; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ CPTools 安装成功"
else
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "❌ CPTools 安装失败"
    exit 1
fi
echo ""

# 安装 Playwright 浏览器
echo "5️⃣  安装 Playwright 浏览器..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if playwright install chromium; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ Playwright 浏览器安装成功"
else
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚠️  Playwright 浏览器安装失败，可能需要手动安装"
    echo "   运行: playwright install chromium"
fi
echo ""

# 验证安装
echo "6️⃣  验证安装..."
if command -v cptools &> /dev/null; then
    VERSION=$(cptools --version 2>&1)
    echo "✅ CPTools 安装成功！"
    echo "   版本: $VERSION"
else
    echo "⚠️  cptools 命令未找到"
    echo "   可以使用: python -m cptools --help"
fi
echo ""

# 完成
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ 安装完成！                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 快速开始："
echo ""
echo "  # 查看帮助"
echo "  cptools --help"
echo ""
echo "  # 运行截图"
echo "  cptools screenshot --host http://example.com --csv data.csv"
echo ""
echo "📖 查看文档："
echo "  https://github.com/joeyplanetart/cptool_cli"
echo ""

