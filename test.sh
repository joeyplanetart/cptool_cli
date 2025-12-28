#!/bin/bash

# CPTools 测试脚本
# 用于验证工具是否正常工作

echo "================================"
echo "CPTools 测试脚本"
echo "================================"
echo ""

# 检查Python版本
echo "1. 检查Python版本..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ 错误: Python3未安装"
    exit 1
fi
echo "✓ Python检查通过"
echo ""

# 检查是否在虚拟环境中
echo "2. 检查虚拟环境..."
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  警告: 未在虚拟环境中运行"
    echo ""
    echo "建议步骤："
    echo "  1. 如果还没有创建虚拟环境，运行: ./setup_venv.sh"
    echo "  2. 激活虚拟环境: source venv/bin/activate"
    echo "  3. 重新运行测试: ./test.sh"
    echo ""
    
    # 检查venv目录是否存在
    if [ -d "venv" ]; then
        echo "检测到venv目录存在，但未激活"
        echo "请运行: source venv/bin/activate"
    else
        echo "未检测到venv目录"
        echo "请运行: ./setup_venv.sh"
    fi
    echo ""
    read -p "是否继续测试（不推荐）? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ 虚拟环境已激活: $VIRTUAL_ENV"
fi
echo ""

# 检查依赖
echo "3. 检查依赖..."
pip show playwright > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️  警告: Playwright未安装"
    if [ -z "$VIRTUAL_ENV" ]; then
        echo "  请先激活虚拟环境: source venv/bin/activate"
        echo "  然后运行: pip install -e ."
    else
        echo "  运行: pip install -e ."
    fi
    echo "  然后: playwright install chromium"
else
    echo "✓ Playwright已安装"
fi
echo ""

# 检查cptools命令
echo "4. 检查cptools命令..."
which cptools > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️  警告: cptools命令不可用"
    if [ -z "$VIRTUAL_ENV" ]; then
        echo "  请先激活虚拟环境: source venv/bin/activate"
        echo "  然后运行: pip install -e ."
    else
        echo "  运行: pip install -e ."
    fi
else
    echo "✓ cptools命令可用"
    cptools --version
fi
echo ""

# 测试帮助命令
echo "5. 测试帮助命令..."
cptools --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ 帮助命令正常"
else
    echo "✗ 帮助命令失败"
fi
echo ""

echo "6. 测试screenshot帮助..."
cptools screenshot --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ screenshot帮助正常"
else
    echo "✗ screenshot帮助失败"
fi
echo ""

# 检查示例文件
echo "7. 检查示例文件..."
if [ -f "example_data.csv" ]; then
    echo "✓ example_data.csv 存在"
else
    echo "✗ example_data.csv 不存在"
fi
echo ""

echo "================================"
echo "测试完成"
echo "================================"
echo ""

if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  提醒: 请在虚拟环境中运行CPTools"
    echo ""
    echo "快速开始："
    echo "  1. 运行自动安装脚本: ./setup_venv.sh"
    echo "  2. 或手动激活: source venv/bin/activate"
    echo ""
else
    echo "✓ 环境检查完成！"
    echo ""
    echo "如果所有检查都通过，可以运行以下命令进行测试："
    echo ""
    echo "cptools screenshot \\"
    echo "  --host http://example.com \\"
    echo "  --csv example_data.csv \\"
    echo "  --output ./test_screenshots \\"
    echo "  --log ./test.log \\"
    echo "  --html ./test_result.html \\"
    echo "  --concurrency 3"
    echo ""
fi

