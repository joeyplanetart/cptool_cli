#!/bin/bash

# URL 404检测工具测试脚本

echo "=========================================="
echo "URL 404检测工具测试"
echo "=========================================="
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行 ./setup_venv.sh"
    exit 1
fi

# 激活虚拟环境
echo "📦 激活虚拟环境..."
. venv/bin/activate

# 检查命令是否可用
echo "🔍 检查 cptools url404 命令..."
if ! cptools url404 --help > /dev/null 2>&1; then
    echo "❌ cptools url404 命令不可用"
    exit 1
fi

echo "✅ cptools url404 命令可用"
echo ""

# 测试1: 基本检测
echo "=========================================="
echo "测试1: 基本 URL 检测"
echo "=========================================="
echo "命令: cptools url404 --host http://www.cafepress.com --csv test_10.csv"
echo ""

cptools url404 \
  --host http://www.cafepress.com \
  --csv test_10.csv \
  --html ./test_results/url404_basic.html

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 测试1 通过"
else
    echo ""
    echo "❌ 测试1 失败"
fi

echo ""
echo "=========================================="
echo "测试2: 自定义并发数"
echo "=========================================="
echo "命令: cptools url404 -h http://www.cafepress.com --csv test_10.csv -c 3"
echo ""

cptools url404 \
  -h http://www.cafepress.com \
  --csv test_10.csv \
  -c 3 \
  --html ./test_results/url404_concurrent.html

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 测试2 通过"
else
    echo ""
    echo "❌ 测试2 失败"
fi

echo ""
echo "=========================================="
echo "测试完成"
echo "=========================================="
echo ""
echo "📊 查看生成的报告:"
echo "   - ./test_results/url404_basic.html"
echo "   - ./test_results/url404_concurrent.html"
echo ""
echo "📝 查看日志:"
echo "   - ls -lh logs/url404_*.log"
echo ""

