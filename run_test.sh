#!/bin/bash

# 使用实际CSV文件测试截图功能
# 用法: ./run_test.sh [主机地址] [CSV文件] [并发数]

# 默认参数
HOST="${1:-http://www.cafepress.com}"
CSV_FILE="${2:-csv_data/categories_172 1-100.csv}"
CONCURRENCY="${3:-5}"

# 创建输出目录
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="./test_screenshots_${TIMESTAMP}"
LOG_FILE="./test_logs/test_${TIMESTAMP}.log"
HTML_FILE="./test_reports/report_${TIMESTAMP}.html"

# 创建必要的目录
mkdir -p test_logs
mkdir -p test_reports

echo "================================"
echo "CPTools 截图测试"
echo "================================"
echo ""
echo "配置信息："
echo "  主机地址: $HOST"
echo "  CSV文件: $CSV_FILE"
echo "  并发数: $CONCURRENCY"
echo "  输出目录: $OUTPUT_DIR"
echo "  日志文件: $LOG_FILE"
echo "  HTML报告: $HTML_FILE"
echo ""

# 检查CSV文件
if [ ! -f "$CSV_FILE" ]; then
    echo "❌ 错误: CSV文件不存在: $CSV_FILE"
    exit 1
fi

# 检查虚拟环境
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  警告: 虚拟环境未激活"
    echo "正在尝试激活虚拟环境..."
    
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        echo "✓ 虚拟环境已激活"
    else
        echo "❌ 错误: 虚拟环境不存在，请先运行: ./setup_venv.sh"
        exit 1
    fi
fi
echo ""

# 显示CSV文件前5行
echo "CSV文件预览（前5行）："
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
head -n 5 "$CSV_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 统计URL数量
URL_COUNT=$(tail -n +2 "$CSV_FILE" | wc -l | tr -d ' ')
echo "总共将截取 $URL_COUNT 个页面"
echo ""

# 询问确认
read -p "是否继续执行? (y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi
echo ""

# 记录开始时间
START_TIME=$(date +%s)

echo "开始执行截图任务..."
echo ""

# 执行截图
cptools screenshot \
  --host "$HOST" \
  --csv "$CSV_FILE" \
  --output "$OUTPUT_DIR" \
  --log "$LOG_FILE" \
  --html "$HTML_FILE" \
  --concurrency "$CONCURRENCY" \
  --timeout 30000

EXIT_CODE=$?

# 记录结束时间
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "================================"
echo "测试完成"
echo "================================"
echo ""
echo "执行时间: ${DURATION}秒"
echo "退出代码: $EXIT_CODE"
echo ""
echo "输出文件："
echo "  截图目录: $OUTPUT_DIR"
echo "  日志文件: $LOG_FILE"
echo "  HTML报告: $HTML_FILE"
echo ""

# 显示结果统计
if [ -f "$LOG_FILE" ]; then
    echo "日志摘要："
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    grep "截屏任务完成" -A 5 "$LOG_FILE" | tail -6
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
fi

# 打开HTML报告（Mac）
if [ "$(uname)" == "Darwin" ]; then
    echo "是否打开HTML报告? (y/N) "
    read -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open "$HTML_FILE"
    fi
fi

echo ""
echo "查看详细日志: less $LOG_FILE"
echo "查看HTML报告: open $HTML_FILE"
echo ""

exit $EXIT_CODE

