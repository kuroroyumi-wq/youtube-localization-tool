from dataclasses import dataclass, field


@dataclass
class LocalizationEntry:
    """1言語分のローカライズデータ"""
    title: str
    description: str


@dataclass
class VideoMetadata:
    """YouTube動画のメタデータ"""
    video_id: str
    default_language: str
    title: str
    description: str
    localizations: dict[str, LocalizationEntry] = field(default_factory=dict)