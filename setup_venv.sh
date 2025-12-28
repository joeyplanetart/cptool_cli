#!/bin/bash

# CPTools 安装脚本
# 自动创建虚拟环境并安装所有依赖

set -e  # 遇到错误立即退出

echo "================================"
echo "CPTools 自动安装脚本"
echo "================================"
echo ""

# 检查Python3
echo "1. 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
echo "✓ Python版本: $PYTHON_VERSION"
echo ""

# 创建虚拟环境
echo "2. 创建虚拟环境..."
if [ -d "venv" ]; then
    echo "⚠️  虚拟环境已存在，是否删除并重新创建? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "删除旧的虚拟环境..."
        rm -rf venv
    else
        echo "跳过创建虚拟环境"
        echo ""
        echo "3. 激活现有虚拟环境..."
        source venv/bin/activate
        echo "✓ 虚拟环境已激活: $VIRTUAL_ENV"
        echo ""
        echo "4. 升级pip..."
        pip install --upgrade pip
        echo ""
        echo "5. 安装项目依赖..."
        pip install -e .
        echo ""
        echo "6. 检查Playwright..."
        if playwright --help &> /dev/null; then
            echo "✓ Playwright已安装"
            echo ""
            echo "7. 安装Playwright浏览器..."
            playwright install chromium
        fi
        echo ""
        echo "================================"
        echo "✓ 安装完成！"
        echo "================================"
        exit 0
    fi
fi

python3 -m venv venv
echo "✓ 虚拟环境创建成功: venv/"
echo ""

# 激活虚拟环境
echo "3. 激活虚拟环境..."
source venv/bin/activate
echo "✓ 虚拟环境已激活: $VIRTUAL_ENV"
echo ""

# 升级pip
echo "4. 升级pip..."
pip install --upgrade pip
echo ""

# 安装依赖
echo "5. 安装项目依赖..."
pip install -e .
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi
echo "✓ 依赖安装成功"
echo ""

# 安装Playwright浏览器
echo "6. 安装Playwright浏览器..."
playwright install chromium
if [ $? -ne 0 ]; then
    echo "⚠️  Playwright浏览器安装失败，请手动运行: playwright install chromium"
else
    echo "✓ Playwright浏览器安装成功"
fi
echo ""

# 验证安装
echo "7. 验证安装..."
if cptools --version &> /dev/null; then
    echo "✓ cptools命令可用"
    cptools --version
else
    echo "⚠️  cptools命令验证失败"
fi
echo ""

echo "================================"
echo "✓ 安装完成！"
echo "================================"
echo ""
echo "使用方法："
echo ""
echo "1. 激活虚拟环境（每次使用前）："
echo "   source venv/bin/activate"
echo ""
echo "2. 查看帮助："
echo "   cptools --help"
echo "   cptools screenshot --help"
echo ""
echo "3. 运行示例："
echo "   cptools screenshot \\"
echo "     --host http://example.com \\"
echo "     --csv example_data.csv \\"
echo "     --output ./screenshots \\"
echo "     --log ./log.log \\"
echo "     --html ./result.html"
echo ""
echo "4. 退出虚拟环境："
echo "   deactivate"
echo ""
echo "运行测试脚本："
echo "   ./test.sh"
echo ""

