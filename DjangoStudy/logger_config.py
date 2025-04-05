import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

# 基础路径配置
BASE_DIR = Path(__file__).resolve().parent.parent  # 项目根目录
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)  # 自动创建日志目录

# 全局日志格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger():
    """配置全局日志记录器"""
    # 基础配置
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[
            # 控制台输出（带颜色）
            logging.StreamHandler(),
            # 文件输出（自动切割）
            RotatingFileHandler(
                filename=LOG_DIR / "app.log",
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding="utf-8"
            )
        ]
    )

    # 特殊模块日志级别调整
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("pymysql").setLevel(logging.INFO)
