# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class ParsingPipeline:
    """
    Класс обработки данных
    """
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongobase = client.leroymerlin_ru

    def process_item(self, item, spider):
        """
        :param item:
        :param spider:
        :return:
        """
        collection = self.mongobase[spider.name]
        if not collection.find_one(item):
            collection.insert_one(item)
        print()
        return item


class LeroyPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        """
        :param item:
        :param info:
        :return:
        """
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as error:
                    print(error)

    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        return item
