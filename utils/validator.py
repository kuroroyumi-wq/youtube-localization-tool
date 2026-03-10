import re
from utils.logger import setup_logger

logger = setup_logger()

# BCP 47準拠の言語コード例（en, ja, zh-TW など）
LANGUAGE_CODE_PATTERN = re.compile(r"^[a-z]{2,3}(-[A-Z][a-z]{3})?(-[A-Z]{2}|\d{3})?$")

VALID_POLICIES = {"overwrite", "skip", "merge"}


def validate_video_id(video_id: str) -> None:
    """動画IDが空でないことを確認する"""
    if not video_id or not video_id.strip():
        logger.error("動画IDが指定されていません")
        raise ValueError("動画IDを指定してください")


def validate_languages(languages: list[str]) -> None:
    """言語コードのリストが有効かを確認する"""
    if not languages:
        logger.error("対象言語が指定されていません")
        raise ValueError("対象言語を1つ以上指定してください")

    for lang in languages:
        if not LANGUAGE_CODE_PATTERN.match(lang):
            logger.error(f"無効な言語コード: {lang}")
            raise ValueError(f"無効な言語コードです: {lang}")


def validate_policy(policy: str) -> None:
    """更新ポリシーが有効な値かを確認する"""
    if policy not in VALID_POLICIES:
        logger.error(f"無効なポリシー: {policy}")
        raise ValueError(f"ポリシーは overwrite / skip / merge のいずれかを指定してください")


def validate_input(video_id: str, languages: list[str], policy: str) -> None:
    """全入力値をまとめて検証する"""
    validate_video_id(video_id)
    validate_languages(languages)
    validate_policy(policy)
    logger.info("入力値検証OK")