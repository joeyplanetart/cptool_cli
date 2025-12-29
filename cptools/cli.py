"""主命令行入口"""
import click
from cptools.commands.screenshot import screenshot
from cptools.commands.url404 import url404


@click.group()
@click.version_option(version="1.1.0", prog_name="cptools")
def cli():
    """CPTools - 命令行工具集
    
    提供网页截屏、URL 404检测等实用功能。
    
    使用 'cptools COMMAND --help' 查看各命令的详细帮助。
    """
    pass


# 注册子命令
cli.add_command(screenshot)
cli.add_command(url404)


if __name__ == "__main__":
    cli()

