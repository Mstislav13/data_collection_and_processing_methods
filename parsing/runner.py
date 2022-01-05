from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from parsing import settings
from parsing.spiders.leroymerlin_ru import LeroymerlinRuSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    search_item = input('Введите название товара для поиска: ')
    process.crawl(LeroymerlinRuSpider, search_item)
    process.start()
