import feedparser, requests
from feedparser.api import FeedParserDict
from bs4 import BeautifulSoup
from newspaper import Article
from scripts.bots.base import Crawler


class CNNCrawler(Crawler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.rss_url = 'https://admin.cnnbrasil.com.br/feed/'


    def crawl(self) -> None:
        feed = feedparser.parse(self.rss_url)

        if feed.status != 200:
            raise requests.exceptions.HTTPError()

        token = self._get_token()

        for entry in feed.entries:
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


    def _get_imagem(self, source: str | FeedParserDict) -> str:
        """Recebe uma notícia e retorna a URL para a imagem de capa da notícia."""
        html = requests.get(source)     # type: ignore
        soup = BeautifulSoup(html.text, 'html.parser')

        imagem = soup.select('img.flex.size-full.object-cover')[2]
        return imagem.get("src")    # type: ignore


    def _montar_noticia(self, noticia: FeedParserDict):
        return {
            "titulo": noticia.title,
            "sumario": noticia.summary + '.',  # type: ignore
            "link": noticia.link,
            "imagem": self._get_imagem(news.link),    # type: ignore
            "disponivel": True,
        }
    