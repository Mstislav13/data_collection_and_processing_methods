import scrapy
import json
import re
from scrapy.http import HtmlResponse
from parsing.items import ParsingItem
from urllib.parse import urlencode
from copy import deepcopy


class InstaComSpider(scrapy.Spider):
    """
    Класс - Spider instagram.com
    """
    name = 'insta_com'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    link_insta_login = 'https://www.instagram.com/accounts/login/ajax/'

    name_insta_login = 'Onliskill_udm'
    pwd_insta_login = '#PWD_INSTAGRAM_BROWSER:10:1642094301' \
                      ':ASZQAK3xQiN26pezmbNTERAktepuAKlWlqcVqr7z3rsE5QVlY3' \
                      '+nAifmia79/DHxjFYAEDdYBKj4jWG' \
                      '+n69gVxvObSIcbyeYMnhZQctoc6QcJo7R7ulkoaD18rDvHEaQm' \
                      '+dFbB28veuLCZFUtGll'

    parse_users = ['marinagafonova', 'dr_polinandreeva']
    subscribers_url = 'https://i.instagram.com/api/v1/friendships'

    subs_count = 12
    headers_api = {'User-Agent': 'Instagram 155.0.0.37.107'}

    def parse(self, response: HtmlResponse):
        """
        :param response:
        :return:
        """
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.link_insta_login,
            method='POST',
            callback=self.login,
            formdata={'username': self.name_insta_login,
                      'enc_password': self.pwd_insta_login},
            headers={'X-CSRFToken': csrf}
        )

    def login(self, response: HtmlResponse):
        """
        :param response:
        :return:
        """
        j_body = response.json()
        if j_body.get('authenticated'):
            for parse_user in self.parse_users:
                yield response.follow(f'/{parse_user}',
                                      callback=self.user_data_parse,
                                      cb_kwargs={'username': parse_user})

    def user_data_parse(self, response: HtmlResponse, username):
        """
        :param response:
        :param username:
        :return:
        """
        user_id = self.fetch_user_id(response.text, username)
        sub_url = f'{self.subscribers_url}/{user_id}/followers/' \
                  f'?count={self.subs_count}'
        yield response.follow(sub_url,
                              callback=self.parse_subscribers,
                              cb_kwargs={'username': username,
                                         'user_id': user_id},
                              headers=self.headers_api)
        subscriptions_url = f'{self.subscribers_url}/{user_id}/' \
                            f'following/?count={self.subs_count}'
        yield response.follow(subscriptions_url,
                              callback=self.parse_subscriptions,
                              cb_kwargs={'username': username,
                                         'user_id': user_id},
                              headers=self.headers_api)

    def parse_subscribers(self, response: HtmlResponse, username, user_id):
        """
        :param response:
        :param username:
        :param user_id:
        :return:
        """
        j_data = response.json()
        next_id = j_data.get('next_max_id')
        if next_id:
            sub_url = f'{self.subscribers_url}/{user_id}/followers/' \
                      f'?count={self.subs_count}&max_id={next_id}' \
                      f'&search_surface=follow_list_page'
            yield response.follow(sub_url,
                                  callback=self.parse_subscribers,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id},
                                  headers=self.headers_api)
        users = j_data.get('users')
        for user in users:
            item = ParsingItem(sub_id=user_id,
                               sub_username=username,
                               sub_type='follower',
                               user_id=user.get('pk'),
                               username=user.get('username'),
                               image=user.get('profile_pic_url'),
                               )
            yield item

    def parse_subscriptions(self, response: HtmlResponse, username, user_id):
        """
        :param response:
        :param username:
        :param user_id:
        :return:
        """
        j_data = response.json()
        next_id = j_data.get('next_max_id')
        if next_id:
            subscriptions_url = f'{self.subscribers_url}/{user_id}/' \
                                f'following/?count={self.subs_count}' \
                                f'&max_id={next_id}'
            yield response.follow(subscriptions_url,
                                  callback=self.parse_subscriptions,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id},
                                  headers=self.headers_api)
            users = j_data.get('users')
            for user in users:
                item = ParsingItem(sub_id=user_id,
                                   sub_username=username,
                                   sub_type='following',
                                   user_id=user.get('pk'),
                                   username=user.get('username'),
                                   image=user.get('profile_pic_url'),
                                   )
                yield item

    def fetch_csrf_token(self, text):
        """
        Получить csrf-токен для авторизации
        :param text:
        :return:
        """
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        """
        :param text:
        :param username:
        :return:
        """
        try:
            matched = re.search(
                '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
            ).group()
            return json.loads(matched).get('id')
        except:
            return re.findall('\"id\":\"\\d+\"', text)[-1].split('"')[-2]
