import os
from googleapiclient.discovery import build


class APIMixin:
    """Класс для предоставления доступа к API."""

    api_key: str = os.getenv('YouTube-API')

    @classmethod
    def get_service(cls) -> build:
        """Возвращает объект для работы с API youtube."""
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube
