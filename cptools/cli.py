"""主命令行入口"""
import click
from cptools.commands.screenshot import screenshot


@click.group()
@click.version_option(version="1.0.0", prog_name="cptools")
def cli():
    """CPTools - 命令行工具集
    
    提供网页截屏等实用功能。
    
    使用 'cptools COMMAND --help' 查看各命令的详细帮助。
    """
    pass


# 注册子命令
cli.add_command(screenshot)


if __name__ == "__main__":
    cli()

