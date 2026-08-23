import feedparser
from sqlalchemy.exc import IntegrityError

from app import app, db
from app.noticias.models import Fonte, Noticia

RSS_FEEDS = {
    'uol': 'https://www.uol.com.br/vueland/api/?loadComponent=XmlFeedRss',
    'metropoles': 'https://metropoleonline.com.br/rss/latest-posts',
    'g1': 'https://g1.globo.com/rss/g1/',
    'cnn': 'https://admin.cnnbrasil.com.br/feed/'
}


def get_imagem(entry) -> str | None:
    for media in entry.get('media_content', []):
        if media.get('medium') == 'image':
            return media.get('url')

    for link in entry.get('links', []):
        if (
            link.get('rel') == 'enclosure'
            and link.get('type', '').startswith('image/')
        ):
            return link.get('href')

    return None


def collect():
    with app.app_context():
        for feed, url in RSS_FEEDS.items():
            parsed_feed = feedparser.parse(url)

            for entry in parsed_feed.entries:
                noticia = Noticia(
                    titulo=(
                        entry.get('summary')
                        if feed == 'uol'
                        else entry.get('title')
                    ),
                    corpo=(
                        None if feed == 'uol'
                        else entry.get('subtitle')
                        or entry.get('summary')
                    ),
                    imagem=get_imagem(entry),
                    url=entry.get('link'),
                    fonte=Fonte(feed)
                )
                db.session.add(noticia)

                try:
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()


if __name__ == '__main__':
    collect()
