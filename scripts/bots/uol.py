import requests, feedparser
from feedparser.api import FeedParserDict
from bs4 import BeautifulSoup
from scripts.bots.base import Crawler


class UOLCrawler(Crawler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.rss_url = 'https://rss.home.uol.com.br/index.xml'


    def crawl(self) -> None:
        feed = feedparser.parse(self.rss_url)
        if feed.status_code != 200:
            exit()

        token = self._get_token()

        for entry in feed.entries:
            if entry is None:
                continue
            
            url: str = entry.link   # type: ignore
            if self._is_repetida(url):   # type: ignore
                continue

            self._indexa_noticia(url)

            noticia = self._montar_noticia(entry)

            result = requests.post(
                f"{self.api_url}/noticia/", 
                json = noticia, headers = {
                    "Authorization": f"Token {token}"
                }
            )
            
            if result.status_code != 201:
                self.logger.error(f"STATUS CODE {result.status_code} PARA {entry.link}.")


    def _montar_noticia(self, noticia: FeedParserDict) -> dict:
        return {
            "titulo": get_title(),  # type: ignore
            "sumario": noticia.summary,
            "link": noticia.link,
            "imagem": self._get_image(noticia.link),  # type: ignore
            "disponivel": True,
        }


    def _get_imagem(self, source: str | FeedParserDict) -> str:
        soup = BeautifulSoup(source, 'html.parser')     # type: ignore
        return soup.find('img').get('src')     # type: ignore

    
    def _get_title(self, url: str) -> str:
        html = requests.get(url).html   # type: ignore
        soup = BeautifulSoup(html, 'html.parser')

        return soup.select_one('h1.title').text     # type: ignore
