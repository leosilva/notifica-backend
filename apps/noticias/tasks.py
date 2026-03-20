from celery import shared_task
from scripts.bots import CNNCrawler, G1Crawler, MetropolesCrawler, UOLCrawler, Crawler


@shared_task
def buscar_noticias():
    crawlers: list[Crawler] = [CNNCrawler(), G1Crawler(), MetropolesCrawler(), UOLCrawler()]
    for crawler in crawlers:
        crawler.crawl()
