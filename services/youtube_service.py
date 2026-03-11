from models.video_metadata import VideoMetadata, LocalizationEntry
from utils.logger import setup_logger

logger = setup_logger()


def get_video_metadata(youtube, video_id: str) -> VideoMetadata:
    """
    YouTube APIから動画のメタデータを取得して返す。
    """
    response = youtube.videos().list(
        part="snippet,localizations",
        id=video_id
    ).execute()

    items = response.get("items", [])
    if not items:
        logger.error(f"動画が見つかりません: {video_id}")
        raise ValueError(f"動画ID '{video_id}' が見つかりません")

    snippet = items[0]["snippet"]
    raw_localizations = items[0].get("localizations", {})

    localizations = {
        lang: LocalizationEntry(
            title=data.get("title", ""),
            description=data.get("description", "")
        )
        for lang, data in raw_localizations.items()
    }

    metadata = VideoMetadata(
        video_id=video_id,
        default_language=snippet.get("defaultLanguage", ""),
        title=snippet.get("title", ""),
        description=snippet.get("description", ""),
        localizations=localizations
    )

    logger.info(f"動画メタデータ取得完了: {video_id}")
    return metadata


def update_video_localizations(
    youtube,
    video_id: str,
    localizations: dict[str, LocalizationEntry],
    dry_run: bool = True
) -> None:
    """
    YouTube APIで動画のローカライズ情報を更新する。
    dry_run=Trueの場合は更新せずログのみ出力。
    """
    body = {
        "id": video_id,
        "localizations": {
            lang: {
                "title": entry.title,
                "description": entry.description
            }
            for lang, entry in localizations.items()
        }
    }

    if dry_run:
        logger.info(f"[DRY-RUN] 更新内容: {list(localizations.keys())}")
        return

    youtube.videos().update(
        part="localizations",
        body=body
    ).execute()

    logger.info(f"YouTube更新完了: {video_id} / 言語: {list(localizations.keys())}")