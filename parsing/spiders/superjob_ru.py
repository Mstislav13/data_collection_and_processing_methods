import scrapy
from scrapy.http import HtmlResponse
from parsing.items import ParsingItem


class SuperjobRuSpider(scrapy.Spider):
    name = 'superjob_ru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python'
                  '&geo%5Br%5D%5B0%5D=3&geo%5Br%5D%5B1%5D=2',
                  'https://www.superjob.ru/vacancy/search/?keywords=python'
                  '&geo%5Br%5D%5B0%5D=4&geo%5Br%5D%5B1%5D=5&geo%5Br%5D%5B2'
                  '%5D=6&geo%5Br%5D%5B3%5D=8',
                  'https://www.superjob.ru/vacancy/search/?keywords=python'
                  '&geo%5Br%5D%5B0%5D=7&geo%5Br%5D%5B1%5D=27 '
                  ]

    def parse(self, response: HtmlResponse):
        """
        :param response:
        :return:
        """
        next_page = response.xpath("//a[contains(@class,"
                                   "'f-test-button-dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//span/a[contains(@class,'icMQ_ "
                               "_6AfZ9')]/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        """
        :param response:
        :return:
        """
        title = response.xpath("//h1//text()").get()
        salary = response.xpath("//span[contains(@class,'ZON4b')]//text()").getall()
        url = response.url
        yield ParsingItem(title=title, salary=salary, url=url)
