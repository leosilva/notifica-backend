from celery import shared_task
from scripts.bots import CNNCrawler, G1Crawler, MetropolesCrawler, UOLCrawler, Crawler
from scripts.services import VectorDatabase


@shared_task
def buscar_noticias():
    vector_database = VectorDatabase()
    crawlers: list[Crawler] = [
        CNNCrawler(vector_database), 
        G1Crawler(vector_database), 
        MetropolesCrawler(vector_database), 
        UOLCrawler(vector_database)
    ]

    for crawler in crawlers:
        crawler.crawl()
