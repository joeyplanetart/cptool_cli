# 开发说明

## 项目结构

```
cptool_cli/
├── cptools/                    # 主包
│   ├── __init__.py
│   ├── cli.py                  # 命令行入口
│   ├── commands/               # 命令模块
│   │   ├── __init__.py
│   │   └── screenshot.py       # 截屏命令
│   └── utils/                  # 工具模块
│       ├── __init__.py
│       ├── logger.py           # 日志工具
│       ├── html_report.py      # HTML报告生成
│       └── dingding.py         # 钉钉通知
├── setup.py                    # 安装配置
├── requirements.txt            # 依赖列表
├── .gitignore                  # Git忽略文件
├── LICENSE                     # 许可证
├── README.md                   # 项目说明
├── QUICKSTART.md              # 快速开始
├── EXAMPLES.md                # 使用示例
├── GITHUB_UPLOAD.md           # GitHub上传指南
├── DEVELOPMENT.md             # 本文件
├── example_data.csv           # 示例数据
└── test.sh                    # 测试脚本
```

## 技术栈

- **Python 3.8+**: 主要编程语言
- **Click**: 命令行界面框架
- **Playwright**: 浏览器自动化和截屏
- **aiohttp**: 异步HTTP客户端（钉钉通知）
- **pandas**: CSV文件处理
- **asyncio**: 异步并发控制

## 添加新命令

### 1. 创建命令文件

在 `cptools/commands/` 目录下创建新的命令文件，例如 `new_tool.py`:

```python
"""新工具命令"""
import click

@click.command()
@click.option('--input', '-i', required=True, help='输入参数')
def new_tool(input):
    """新工具的描述"""
    click.echo(f"执行新工具: {input}")
    # 实现你的逻辑
```

### 2. 注册命令

在 `cptools/cli.py` 中导入并注册新命令：

```python
from cptools.commands.screenshot import screenshot
from cptools.commands.new_tool import new_tool  # 导入新命令

@click.group()
@click.version_option(version="1.0.0", prog_name="cptools")
def cli():
    """CPTools - 命令行工具集"""
    pass

cli.add_command(screenshot)
cli.add_command(new_tool)  # 注册新命令
```

### 3. 测试新命令

```bash
cptools new-tool --help
cptools new-tool --input test
```

## 开发环境设置

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd cptool_cli
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装开发依赖

```bash
pip install -e .
playwright install chromium
```

### 4. 运行测试

```bash
./test.sh
```

## 代码规范

### Python代码风格

遵循 PEP 8 规范：

```bash
# 安装代码检查工具
pip install flake8 black

# 检查代码
flake8 cptools/

# 格式化代码
black cptools/
```

### 文档字符串

使用Google风格的文档字符串：

```python
def function_name(param1, param2):
    """简短描述
    
    详细描述（可选）
    
    Args:
        param1: 参数1描述
        param2: 参数2描述
        
    Returns:
        返回值描述
        
    Raises:
        异常描述
    """
    pass
```

## 调试技巧

### 1. 启用详细日志

修改 `screenshot.py` 中的日志级别：

```python
logger = setup_logger(log, level=logging.DEBUG)
```

### 2. 浏览器可视模式

修改 `screenshot.py`，将浏览器改为非无头模式：

```python
browser = await p.chromium.launch(headless=False)  # 改为False
```

### 3. 减少并发测试

```bash
cptools screenshot ... -c 1
```

## 性能优化

### 1. 调整并发数

根据机器性能和网络情况调整：

```bash
# CPU密集型: 2-4个并发
cptools screenshot ... -c 3

# 网络密集型: 10-20个并发
cptools screenshot ... -c 15
```

### 2. 优化超时设置

```bash
# 快速网站
cptools screenshot ... --timeout 10000

# 慢速网站
cptools screenshot ... --timeout 60000
```

### 3. 截图优化

在 `screenshot.py` 中可以调整截图质量：

```python
await page.screenshot(
    path=str(screenshot_path),
    full_page=True,
    type='jpeg',  # 使用JPEG减少文件大小
    quality=80    # 调整质量
)
```

## 错误处理

### 常见错误

1. **Playwright未安装**
   ```bash
   pip install playwright
   playwright install chromium
   ```

2. **依赖冲突**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

3. **CSV编码问题**
   
   确保CSV文件使用UTF-8编码保存

## 发布新版本

### 1. 更新版本号

修改以下文件中的版本号：
- `setup.py`
- `cptools/__init__.py`
- `cptools/cli.py`

### 2. 提交更改

```bash
git add .
git commit -m "Release v1.1.0"
git tag v1.1.0
git push origin main --tags
```

### 3. 发布到PyPI（可选）

```bash
# 安装打包工具
pip install build twine

# 构建
python -m build

# 上传到PyPI
twine upload dist/*
```

## 贡献指南

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 测试清单

在提交代码前，确保：

- [ ] 代码符合PEP 8规范
- [ ] 添加了必要的文档字符串
- [ ] 功能测试通过
- [ ] 更新了相关文档
- [ ] 没有引入新的依赖（或已添加到requirements.txt）
- [ ] Git提交信息清晰

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交Issue: https://github.com/joeyplanetart/cptool_cli/issues
- Email: your.email@example.com

## 许可证

本项目采用MIT许可证，详见 LICENSE 文件。

