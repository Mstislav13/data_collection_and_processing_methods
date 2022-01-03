# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParsingItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    salary = scrapy.Field()
    currency = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    pass
