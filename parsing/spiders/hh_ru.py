import scrapy
from scrapy.http import HtmlResponse
from parsing.items import ParsingItem


class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&search_field=name'
                  '&search_field=company_name&search_field=description'
                  '&clusters=true&ored_clusters=true&enable_snippets=true'
                  '&text=python',
                  'https://hh.ru/search/vacancy?area=2&search_field=name'
                  '&search_field=company_name&search_field=description'
                  '&clusters=true&ored_clusters=true&enable_snippets=true'
                  '&text=python',
                  'https://hh.ru/search/vacancy?area=231&search_field=name'
                  '&search_field=company_name&search_field=description'
                  '&clusters=true&ored_clusters=true&enable_snippets=true'
                  '&text=python '
                  ]

    def parse(self, response: HtmlResponse):
        """
        :param response:
        :return:
        """
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//span/a[@data-qa='vacancy-serp__vacancy"
                               "-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        """
        :param response:
        :return:
        """
        title = response.xpath("//h1//text()").get()
        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        url = response.url
        yield ParsingItem(title=title, salary=salary, url=url)
