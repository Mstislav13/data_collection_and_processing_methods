# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def clear(value):
    """
    :param value:
    :return:
    """
    value = value.replace(' ', '').replace('\n', '')
    try:
        value = value
    except:
        pass
    finally:
        return value


class ParsingItem(scrapy.Item):
    _id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    price_currency = scrapy.Field(output_processor=TakeFirst())
    spec_name = scrapy.Field()
    spec_value = scrapy.Field(
        input_processor=MapCompose(clear))
    photo = scrapy.Field()
