"""日志工具模块"""
import logging
import sys
from pathlib import Path


def setup_logger(log_file=None, level=logging.INFO):
    """设置日志记录器
    
    Args:
        log_file: 日志文件路径
        level: 日志级别
        
    Returns:
        配置好的logger实例
    """
    logger = logging.getLogger("cptools")
    logger.setLevel(level)
    
    # 清除已有的处理器
    logger.handlers.clear()
    
    # 格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

