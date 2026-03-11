# YouTube Localization Tool

YouTube動画のタイトル・説明文を複数言語に自動翻訳し、YouTube APIで一括更新するCLIツール。

## 必要環境

- Python 3.9以上
- DeepL APIキー（または Google Cloud 翻訳API）
- Google Cloud プロジェクト（YouTube Data API v3 有効化済み）

## セットアップ

### 1. パッケージインストール

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. 認証情報の配置

Google Cloud ConsoleからOAuthクライアントIDをダウンロードし、プロジェクトルートに配置。

\`\`\`
client_secrets.json
\`\`\`

### 3. 環境変数の設定

\`\`\`.env.example\` をコピーして \`.env\` を作成。

\`\`\`bash
cp .env.example .env
\`\`\`

\`.env\` を編集してAPIキーを設定：

\`\`\`
DEEPL_API_KEY=your_deepl_api_key_here
TRANSLATOR=deepl
DRY_RUN=true
\`\`\`

## 使い方

### 基本コマンド

\`\`\`bash
python main.py --video-id <動画ID> --lang <言語コード>
\`\`\`

### 例

\`\`\`bash
# 英語・スペイン語に翻訳（確認のみ）
python main.py --video-id ABC123 --lang en --lang es --dry-run

# 実際に更新
python main.py --video-id ABC123 --lang en --lang es

# 既存ローカライズをスキップ
python main.py --video-id ABC123 --lang en --policy skip
\`\`\`

### オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `--video-id` | YouTube動画ID（必須） | - |
| `--lang` | 翻訳対象言語コード（複数指定可） | - |
| `--dry-run` | 実際には更新しない | true |
| `--policy` | overwrite / skip / merge | overwrite |

## ディレクトリ構成

\`\`\`
youtube-localization-tool/
├── main.py
├── config/settings.py
├── auth/oauth.py
├── services/
│   ├── youtube_service.py
│   ├── translation_service.py
│   ├── deepl_translator.py
│   └── google_translator.py
├── models/video_metadata.py
├── utils/
│   ├── logger.py
│   └── validator.py
└── .env.example
\`\`\`