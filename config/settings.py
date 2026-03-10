from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # YouTube API
    youtube_client_secrets_file: str = "client_secrets.json"

    # 翻訳API選択（"deepl" または "google"）
    translator: str = "deepl"
    deepl_api_key: str = ""
    google_application_credentials: str = ""

    # 動作設定
    default_language: str = "ja"
    dry_run: bool = True
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()