@echo off
REM CPTools 一键安装脚本 - Windows 版本

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                  CPTools 一键安装脚本                             ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM 检查 Python
echo 1️⃣  检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到 Python
    echo    请先安装 Python 3.8 或更高版本
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ %PYTHON_VERSION%
echo.

REM 检查 pip
echo 2️⃣  检查 pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到 pip
    pause
    exit /b 1
)
echo ✅ pip 可用
echo.

REM 选择镜像源
echo 3️⃣  选择安装源...
echo    1) 默认 (PyPI)
echo    2) 清华镜像 (推荐，国内快)
echo    3) 阿里镜像
set /p choice="请选择 [1-3, 默认 2]: "
if "%choice%"=="" set choice=2

set PIP_INDEX=
if "%choice%"=="1" (
    echo 使用默认 PyPI 源
) else if "%choice%"=="2" (
    set PIP_INDEX=-i https://pypi.tuna.tsinghua.edu.cn/simple
    echo 使用清华镜像源
) else if "%choice%"=="3" (
    set PIP_INDEX=-i https://mirrors.aliyun.com/pypi/simple/
    echo 使用阿里镜像源
)
echo.

REM 安装 CPTools
echo 4️⃣  安装 CPTools...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REM 这里需要替换为你的 GitHub 仓库地址
set GITHUB_URL=https://github.com/joeyplanetart/cptool_cli.git

pip install %PIP_INDEX% git+%GITHUB_URL%
if %errorlevel% neq 0 (
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    echo ❌ CPTools 安装失败
    pause
    exit /b 1
)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ✅ CPTools 安装成功
echo.

REM 安装 Playwright 浏览器
echo 5️⃣  安装 Playwright 浏览器...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
playwright install chromium
if %errorlevel% neq 0 (
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    echo ⚠️  Playwright 浏览器安装失败，可能需要手动安装
    echo    运行: playwright install chromium
) else (
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    echo ✅ Playwright 浏览器安装成功
)
echo.

REM 验证安装
echo 6️⃣  验证安装...
cptools --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('cptools --version') do set VERSION=%%i
    echo ✅ CPTools 安装成功！
    echo    版本: %VERSION%
) else (
    echo ⚠️  cptools 命令未找到
    echo    可以使用: python -m cptools --help
)
echo.

REM 完成
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    ✅ 安装完成！                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 🚀 快速开始：
echo.
echo   # 查看帮助
echo   cptools --help
echo.
echo   # 运行截图
echo   cptools screenshot --host http://example.com --csv data.csv
echo.
echo 📖 查看文档：
echo   https://github.com/joeyplanetart/cptool_cli
echo.

pause

