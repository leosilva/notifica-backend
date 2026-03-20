import feedparser, requests
from feedparser.api import FeedParserDict
from scripts.base import Crawler


class G1Crawler(Crawler):
    def __init__(self) -> None:
        self.rss_url = 'https://g1.globo.com/rss/g1/'


    def crawl(self) -> None:
        feed = feedparser.parse(self.rss_url)

        if feed.status != 200:
            raise requests.exceptions.HTTPError()

        token = self._get_token()

        for entry in feed.entries:
            noticia = self._montar_noticia(entry)

            result = requests.post(
                f"{self.api_url}/noticia/",
                json = noticia, headers = {
                    "Authorization": f"Token {token}"
                }
            )

            if result.status_code != 201:
                self.logger.error(f"STATUS CODE {result.status_code} PARA {entry.link}.")


    def _get_imagem(self, source: str | FeedParserDict) -> str:     # type: ignore
        """Recebe uma notícia e retorna a URL para a imagem de capa da notícia."""
        imagem = source.get("media_content", "")    # type: ignore
        if imagem:
            return imagem[0].get("url")     # type: ignore


    def _montar_noticia(self, noticia: FeedParserDict):
        return {
            "titulo": noticia.title,
            "sumario": noticia.get("subtitle", ''),
            "link": noticia.link,
            "disponivel": True,
            "imagem": self._get_imagem(noticia),
        }
