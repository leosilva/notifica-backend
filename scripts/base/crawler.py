import requests
from feedparser.api import FeedParserDict
from abc import ABC, abstractmethod
import logging, os


class Crawler(ABC):
    def __init__(self) -> None:
        self.api_url = os.getenv('API_URL')
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            filename=".log", filemode="w",
            format="%(asctime)s - %(message)s"
        )
    

    def _get_token(self) -> str:
        response = requests.post(f"{self.api_url}/login/", json = {
            "username": os.getenv("SUPER_USER_USERNAME"),
            "password": os.getenv("SUPER_USER_PASSWORD"),
        })

        body = response.json()
        token = body.get('access')
        
        return token


    @abstractmethod
    def _montar_noticia(self, noticia: FeedParserDict) -> dict:
        pass


    @abstractmethod
    def _get_imagem(self, source: str | FeedParserDict) -> str:
        pass


    @abstractmethod
    def crawl(self) -> None:
        pass
