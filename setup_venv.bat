@echo off
REM CPTools Windows 安装脚本
REM 自动创建虚拟环境并安装所有依赖

echo ================================
echo CPTools 自动安装脚本 (Windows)
echo ================================
echo.

REM 检查Python
echo 1. 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo X 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo √ Python版本: %PYTHON_VERSION%
echo.

REM 创建虚拟环境
echo 2. 创建虚拟环境...
if exist venv (
    echo ! 虚拟环境已存在，是否删除并重新创建? (Y/N^)
    set /p response=
    if /i "%response%"=="Y" (
        echo 删除旧的虚拟环境...
        rmdir /s /q venv
    ) else (
        echo 跳过创建虚拟环境
        goto activate
    )
)

python -m venv venv
echo √ 虚拟环境创建成功: venv\
echo.

:activate
REM 激活虚拟环境
echo 3. 激活虚拟环境...
call venv\Scripts\activate.bat
echo √ 虚拟环境已激活
echo.

REM 升级pip
echo 4. 升级pip...
python -m pip install --upgrade pip
echo.

REM 安装依赖
echo 5. 安装项目依赖...
pip install -e .
if errorlevel 1 (
    echo X 依赖安装失败
    pause
    exit /b 1
)
echo √ 依赖安装成功
echo.

REM 安装Playwright浏览器
echo 6. 安装Playwright浏览器...
playwright install chromium
if errorlevel 1 (
    echo ! Playwright浏览器安装失败，请手动运行: playwright install chromium
) else (
    echo √ Playwright浏览器安装成功
)
echo.

REM 验证安装
echo 7. 验证安装...
cptools --version >nul 2>&1
if errorlevel 1 (
    echo ! cptools命令验证失败
) else (
    echo √ cptools命令可用
    cptools --version
)
echo.

echo ================================
echo √ 安装完成！
echo ================================
echo.
echo 使用方法：
echo.
echo 1. 激活虚拟环境（每次使用前）：
echo    venv\Scripts\activate
echo.
echo 2. 查看帮助：
echo    cptools --help
echo    cptools screenshot --help
echo.
echo 3. 运行示例：
echo    cptools screenshot ^
echo      --host http://example.com ^
echo      --csv example_data.csv ^
echo      --output ./screenshots ^
echo      --log ./log.log ^
echo      --html ./result.html
echo.
echo 4. 退出虚拟环境：
echo    deactivate
echo.
pause

