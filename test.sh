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
    echo "错误: Python3未安装"
    exit 1
fi
echo "✓ Python检查通过"
echo ""

# 检查是否在虚拟环境中
echo "2. 检查虚拟环境..."
if [ -z "$VIRTUAL_ENV" ]; then
    echo "警告: 未在虚拟环境中，建议创建虚拟环境"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
else
    echo "✓ 虚拟环境: $VIRTUAL_ENV"
fi
echo ""

# 检查依赖
echo "3. 检查依赖..."
pip show playwright > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "警告: Playwright未安装"
    echo "  pip install -r requirements.txt"
    echo "  playwright install chromium"
else
    echo "✓ Playwright已安装"
fi
echo ""

# 检查cptools命令
echo "4. 检查cptools命令..."
which cptools > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "警告: cptools命令不可用"
    echo "  pip install -e ."
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

