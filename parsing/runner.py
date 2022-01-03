from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from parsing import settings
from parsing.spiders.hh_ru import HhRuSpider
from parsing.spiders.superjob_ru import SuperjobRuSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhRuSpider)
    process.crawl(SuperjobRuSpider)

    process.start()
