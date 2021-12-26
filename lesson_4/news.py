import pymongo
from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

url = 'https://lenta.ru'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/96.0.4664.93 Safari/537.36'}

client = MongoClient('127.0.0.1', 27017)
db = client['news_lenta_ru']
news_1 = db.news_1

news_1.create_index([('title', pymongo.TEXT)], name='uniq_info',
                          unique=True)

response = requests.get(url, headers=header)
data = html.fromstring(response.text)

news_block = data.xpath("//a[contains(@class,'_topnews')]")

news_list = []

for news in news_block:
    item = {}
    source_name = url
    news_name = news.xpath(".//span[@class='card-mini__title']/text() | "
                           ".//h3[@class='card-big__title']/text()")
    news_link = news.xpath(".//span[@class='card-mini__title']/../../@href | "
                           ".//h3[@class='card-big__title']/../../@href")
    new_link = ()
    for link in news_link:
        new_link = url + link

    date = news.xpath(".//time[@class='card-mini__date']//text() | "
                      ".//time[@class='card-big__date']//text()")

    item['source'] = source_name
    item['title'] = news_name
    item['link'] = new_link
    item['date'] = date

    news_list.append(item)

    try:
        news_1.insert_one(item)
    except dke:
        pass

pprint(news_list)
