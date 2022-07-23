# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParsingItem(scrapy.Item):
    sub_id = scrapy.Field()
    sub_username = scrapy.Field()
    sub_type = scrapy.Field()
    user_id = scrapy.Field()
    username = scrapy.Field()
    image = scrapy.Field()
    _id = scrapy.Field()
