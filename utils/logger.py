import logging
import os
from pathlib import Path


def setup_logger(name: str = "youtube_localizer", level: str = "INFO") -> logging.Logger:
    """
    ロガーを設定して返す。
    コンソールとファイル（logs/app.log）の両方に出力する。
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # すでにハンドラが設定済みの場合は追加しない
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # コンソール出力
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # ファイル出力（logs/app.log）
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_dir / "app.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger