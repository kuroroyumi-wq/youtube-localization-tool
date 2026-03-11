from abc import ABC, abstractmethod


class TranslationService(ABC):
    """翻訳サービスの抽象インターフェース"""

    @abstractmethod
    def translate(self, text: str, target_lang: str) -> str:
        """テキストを指定言語に翻訳して返す"""
        pass