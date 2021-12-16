from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re

url = 'https://hh.ru'
page = 0
params = {'search_field': 'name',
          'fromSearchLine': 'true',
          'text': 'python',
          'page': page
          }

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/96.0.4664.93 Safari/537.36'}

response = requests.get(url+'/search/vacancy', params=params, headers=headers)

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
        salary = vac.find('div', {'class': 'vacancy-serp-item__sidebar'})
        if not salary:
            min_sal = None
            max_sal = None
            cur_sal = None
        else:
            salary_1 = salary.getText().replace(u'\xa0', u'')
            # print()
            salary_1 = re.split(r'\s|-', salary_1)
            # print(salary_1)
            if salary_1[0] == 'от':
                min_sal = int(salary_1[1]+salary_1[2])
                max_sal = None
                cur_sal = salary_1[3]
            elif salary_1[0] == 'до':
                min_sal = None
                max_sal = int(salary_1[1]+salary_1[2])
                cur_sal = salary_1[3]
            else:
                min_sal = int(salary_1[0]+salary_1[1])
                max_sal = int(salary_1[3]+salary_1[4])
                cur_sal = salary_1[5]

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

        page = data.find('a', class_='bloko-button')
        if not page:
            page = None
        vacancies = url + page['href']
