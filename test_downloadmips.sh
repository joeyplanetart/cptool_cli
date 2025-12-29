#!/bin/bash

# 产品主图下载工具测试脚本
# 用于测试 cptools downloadmips 命令

echo "==================================="
echo "产品主图下载工具测试"
echo "==================================="
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行 setup_venv.sh"
    exit 1
fi

# 激活虚拟环境
echo "📦 激活虚拟环境..."
source venv/bin/activate

# 检查测试文件
if [ ! -f "test_downloadmips.csv" ]; then
    echo "📝 创建测试CSV文件..."
    cat > test_downloadmips.csv << EOF
product_no
629442244
EOF
fi

# 运行测试
echo "🚀 开始下载产品主图..."
echo ""
cptools downloadmips \
    --host https://www.cafepress.com \
    --csv test_downloadmips.csv \
    -c 1 \
    --no-dingding

echo ""
echo "==================================="
echo "测试完成！"
echo "==================================="
echo ""
echo "查看结果："
echo "  - 下载的图片: ./mips/629442244/"
echo "  - HTML报告: ./downloadmips_result.html"
echo "  - 日志文件: ./logs/downloadmips_*.log"
echo ""

