import argparse
import sys
from config.settings import settings
from auth.oauth import build_oauth_client
from services.youtube_service import get_video_metadata, update_video_localizations
from services.deepl_translator import DeepLTranslator
from services.google_translator import GoogleTranslator
from models.video_metadata import LocalizationEntry
from utils.validator import validate_input
from utils.logger import setup_logger

logger = setup_logger(level=settings.log_level)


def build_translator():
    if settings.translator == "deepl":
        return DeepLTranslator(api_key=settings.deepl_api_key)
    elif settings.translator == "google":
        return GoogleTranslator()
    else:
        raise ValueError(f"未対応の翻訳サービス: {settings.translator}")


def run(video_id: str, languages: list[str], policy: str, dry_run: bool):
    # 入力値検証
    validate_input(video_id, languages, policy)

    # YouTube認証
    youtube = build_oauth_client(settings.youtube_client_secrets_file)

    # 動画メタデータ取得
    metadata = get_video_metadata(youtube, video_id)
    logger.info(f"取得完了: {metadata.title}")

    # 翻訳サービス初期化
    translator = build_translator()

    # 翻訳＆ローカライズ辞書を構築
    new_localizations = dict(metadata.localizations)

    for lang in languages:
        if policy == "skip" and lang in new_localizations:
            logger.info(f"スキップ: {lang} (既存)")
            continue

        try:
            translated_title = translator.translate(metadata.title, lang)
            translated_desc = translator.translate(metadata.description, lang)
            new_localizations[lang] = LocalizationEntry(
                title=translated_title,
                description=translated_desc
            )
            logger.info(f"翻訳完了: {lang}")
        except Exception as e:
            logger.error(f"翻訳失敗 ({lang}): {e}")
            continue

    # YouTube更新
    update_video_localizations(youtube, video_id, new_localizations, dry_run=dry_run)

    if dry_run:
        logger.info("DRY-RUN完了。実際の更新は行われていません。")
    else:
        logger.info("YouTube更新完了。")


def main():
    parser = argparse.ArgumentParser(description="YouTube動画ローカライズ自動化ツール")
    parser.add_argument("--video-id", required=True, help="YouTube動画ID")
    parser.add_argument("--lang", required=True, action="append", dest="languages", help="翻訳対象言語コード")
    parser.add_argument("--dry-run", action="store_true", default=settings.dry_run, help="実際には更新しない")
    parser.add_argument("--policy", default="overwrite", choices=["overwrite", "skip", "merge"], help="更新ポリシー")

    args = parser.parse_args()
    run(
        video_id=args.video_id,
        languages=args.languages,
        policy=args.policy,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()
