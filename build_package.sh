#!/bin/bash

# CPTools 打包脚本
# 用于创建可分发给同事的安装包

set -e

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                  CPTools 打包脚本                                 ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# 检查必要工具
echo "1️⃣  检查环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    exit 1
fi

# 安装打包工具
echo "2️⃣  安装/检查打包工具..."
pip install --upgrade build wheel twine 2>&1 | grep -v "Requirement already satisfied" || true
echo "✅ 打包工具准备就绪"
echo ""

# 清理旧的构建
echo "3️⃣  清理旧构建..."
rm -rf build/ dist/ *.egg-info/
echo "✅ 清理完成"
echo ""

# 构建包
echo "4️⃣  构建分发包..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python setup.py sdist bdist_wheel
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 构建完成"
echo ""

# 显示构建结果
echo "5️⃣  构建结果："
ls -lh dist/
echo ""

# 创建完整安装包
echo "6️⃣  创建完整安装包..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PACKAGE_NAME="cptools-install-${TIMESTAMP}"

mkdir -p "${PACKAGE_NAME}"
cp -r dist/ "${PACKAGE_NAME}/"
cp requirements.txt "${PACKAGE_NAME}/"
cp INSTALL.md "${PACKAGE_NAME}/README.md"

# 创建安装脚本
cat > "${PACKAGE_NAME}/install.sh" << 'EOF'
#!/bin/bash
echo "安装 CPTools..."
echo ""

# 安装依赖
echo "1. 安装依赖..."
pip install -r requirements.txt

# 安装 CPTools
echo ""
echo "2. 安装 CPTools..."
pip install dist/*.whl

# 安装 Playwright
echo ""
echo "3. 安装 Playwright 浏览器..."
playwright install chromium

# 验证
echo ""
echo "4. 验证安装..."
cptools --version

echo ""
echo "✅ 安装完成！"
echo "运行 'cptools --help' 查看帮助"
EOF

chmod +x "${PACKAGE_NAME}/install.sh"

# 创建 Windows 安装脚本
cat > "${PACKAGE_NAME}/install.bat" << 'EOF'
@echo off
echo 安装 CPTools...
echo.

echo 1. 安装依赖...
pip install -r requirements.txt

echo.
echo 2. 安装 CPTools...
for %%f in (dist\*.whl) do pip install %%f

echo.
echo 3. 安装 Playwright 浏览器...
playwright install chromium

echo.
echo 4. 验证安装...
cptools --version

echo.
echo ✅ 安装完成！
echo 运行 'cptools --help' 查看帮助
pause
EOF

# 打包
tar -czf "${PACKAGE_NAME}.tar.gz" "${PACKAGE_NAME}"
zip -r "${PACKAGE_NAME}.zip" "${PACKAGE_NAME}" > /dev/null

echo "✅ 完整安装包创建完成"
echo ""

# 显示结果
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ 打包完成！                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "📦 生成的文件："
echo ""
echo "  dist/                           # Python 包"
ls -lh dist/
echo ""
echo "  ${PACKAGE_NAME}.tar.gz          # Linux/Mac 安装包"
ls -lh "${PACKAGE_NAME}.tar.gz"
echo ""
echo "  ${PACKAGE_NAME}.zip             # Windows 安装包"
ls -lh "${PACKAGE_NAME}.zip"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📤 分发方式："
echo ""
echo "  方式1: 直接分发 .whl 文件"
echo "    给同事: dist/*.whl"
echo "    同事执行: pip install cptools-*.whl"
echo ""
echo "  方式2: 分发完整安装包（推荐）"
echo "    Linux/Mac: ${PACKAGE_NAME}.tar.gz"
echo "    Windows: ${PACKAGE_NAME}.zip"
echo ""
echo "  方式3: 上传到文件服务器"
echo "    上传 dist/ 目录到服务器"
echo "    同事从服务器安装"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 同事安装方法："
echo ""
echo "  # 从 .tar.gz"
echo "  tar -xzf ${PACKAGE_NAME}.tar.gz"
echo "  cd ${PACKAGE_NAME}"
echo "  ./install.sh"
echo ""
echo "  # 从 .zip (Windows)"
echo "  解压 ${PACKAGE_NAME}.zip"
echo "  进入目录，双击 install.bat"
echo ""
echo "  # 直接从 .whl"
echo "  pip install dist/*.whl"
echo "  playwright install chromium"
echo ""

# 清理临时目录
rm -rf "${PACKAGE_NAME}"

echo "完成！"

