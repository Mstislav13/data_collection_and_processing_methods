# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient


class ParsingPipeline:
    """
    Класс обработки данных
    """
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongobase = client.insta_com

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
