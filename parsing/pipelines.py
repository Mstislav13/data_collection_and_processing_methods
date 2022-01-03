# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class ParsingPipeline:
    """
    Класс обработки данных
    """
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongobase = client.vacncies_hh_sj

    def process_item(self, item, spider):
        """
        :param item:
        :param spider:
        :return:
        """
        if spider.name == 'hh_ru':
            item['currency'], \
            item['salary_min'], \
            item['salary_max'] = self.sort_sal_hh_ru(item['salary'])
        else:
            item['currency'], \
            item['salary_min'], \
            item['salary_max'] = self.sort_sal_superjob_ru(item['salary'])
        del item['salary']
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def sort_sal_hh_ru(self, salary):
        """
        :param salary:
        :return:
        """
        if salary[0] == 'з/п не указана':
            salary_min = None
            salary_max = None
            currency = None
        elif salary[0] == 'до ':
            salary_min = None
            salary_max = int(salary[1].replace('\xa0', ''))
            currency = salary[3]
        elif salary[0] == 'от ' and salary[2] == ' до ':
            salary_min = int(salary[1].replace('\xa0', ''))
            salary_max = int(salary[3].replace('\xa0', ''))
            currency = salary[5]
        else:
            salary_min = int(salary[1].replace('\xa0', ''))
            salary_max = None
            currency = salary[3]
        return salary_min, salary_max, currency

    def sort_sal_superjob_ru(self, salary):
        """
        :param salary:
        :return:
        """
        if salary[0] == 'По договорённости':
            salary_min = None
            salary_max = None
            currency = None
        elif salary[0] == 'от':
            salary_list = salary[2].split('\xa0')
            salary_min = int(''.join(salary_list[:2]))
            salary_max = None
            currency = salary_list[2]
        elif salary[0] == 'до':
            salary_list = salary[2].split('\xa0')
            salary_min = None
            salary_max = int(''.join(salary_list[:2]))
            currency = salary_list[2]
        else:
            salary_min = int(salary[0].replace('\xa0', ''))
            salary_max = int(salary[4].replace('\xa0', ''))
            currency = salary[6]
        return salary_min, salary_max, currency
