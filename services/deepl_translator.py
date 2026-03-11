import deepl
from services.translation_service import TranslationService
from utils.logger import setup_logger

logger = setup_logger()


class DeepLTranslator(TranslationService):
    def __init__(self, api_key: str):
        self.translator = deepl.Translator(api_key)

    def translate(self, text: str, target_lang: str) -> str:
        result = self.translator.translate_text(text, target_lang=target_lang)
        logger.info(f"DeepL翻訳完了: {target_lang}")
        return result.text