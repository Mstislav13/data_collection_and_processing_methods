import pymongo
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

url = 'https://hh.ru'
prof = input('Введите инересующую вас вакансию: ')
params = {'search_field': 'name',
          'fromSearchLine': 'true',
          'text': 'python',
          'page': 0
          }

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/96.0.4664.93 Safari/537.36'}

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies_hh_ru']
jobs = db.jobs

response = requests.get(url + '/search/vacancy', params=params,
                        headers=headers)

while True:
    if response.ok:
        data = bs(response.text, 'html.parser')
        vacancies = data.find_all('div', class_='vacancy-serp-item')
        vacancies_list = []
        for vac in vacancies:
            vac_data = {}
            title_and_link = vac.find('a',
                                      {'data-qa': 'vacancy-serp__vacancy-title'})
            title = title_and_link.text
            link = title_and_link['href']
            about = vac.find('div', class_='g-user-content')
            about_info = about.text
            city = vac.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
            job_city = city.text
            salary = vac.find('span',
                              {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if not salary:
                min_sal = None
                max_sal = None
                cur_sal = None
            else:
                salary_1 = salary.text.replace(u'\u202f', u'')
                salary_1 = re.split(r'\s|-', salary_1)
                if salary_1[0] == 'от':
                    min_sal = int(salary_1[1])
                    max_sal = None
                    cur_sal = salary_1[2]
                elif salary_1[0] == 'до':
                    min_sal = None
                    max_sal = int(salary_1[1])
                    cur_sal = salary_1[2]
                else:
                    min_sal = int(salary_1[0])
                    max_sal = int(salary_1[2])
                    cur_sal = salary_1[3]

            site = url

            vac_data['Вакансия'] = title
            vac_data['Вакансия(ссылка)'] = link
            vac_data['Инфо'] = about_info
            vac_data['Город'] = job_city
            vac_data['Зарплата(мин.)'] = min_sal
            vac_data['Зарплата(макс.)'] = max_sal
            vac_data['Зарплата(валюта)'] = cur_sal
            vac_data['Сайт'] = site
            vacancies_list.append(vac_data)
            pprint(vacancies_list)

            try:
                jobs.create_index([('Инфо', pymongo.TEXT)], name='uniq_info',
                                  unique=True)
                jobs.insert_one(vac_data)
            except dke:
                pass

        next_page = data.find('a', {'data-qa': 'pager-next'})
        response = requests.get(url + next_page['href'], headers=headers)
        if not next_page:
            break
    else:
        break

how_many_sal = int(input('Интересующая зарплата: '))

for sal in jobs.find({'$or': [{'Зарплата(мин.)': {'$gte': how_many_sal}},
                              {'Зарплата(макс.)': {'$gte': how_many_sal}}
                              ]}):
    print(sal)
