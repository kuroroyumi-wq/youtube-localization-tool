from google.cloud import translate_v2 as translate
from services.translation_service import TranslationService
from utils.logger import setup_logger

logger = setup_logger()


class GoogleTranslator(TranslationService):
    def __init__(self):
        self.client = translate.Client()

    def translate(self, text: str, target_lang: str) -> str:
        result = self.client.translate(text, target_language=target_lang)
        logger.info(f"Google翻訳完了: {target_lang}")
        return result["translatedText"]