import scrapy
from scrapy.http import HtmlResponse
from parsing.items import ParsingItem
from scrapy.loader import ItemLoader


class LeroymerlinRuSpider(scrapy.Spider):
    name = 'leroymerlin_ru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search_item):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search_item}']

    def parse(self, response: HtmlResponse):
        """
        :param response:
        """
        next_page = response.xpath(
            "//a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='product-name']")
        for link in links:
            yield response.follow(link, callback=self.parse_goods)

    def parse_goods(self, response: HtmlResponse):

        loader = ItemLoader(item=ParsingItem(), response=response)
        loader.add_xpath('_id', "//span[@slot='article']/@content")
        loader.add_xpath('name', "//h1/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('price', "//meta[@itemprop='price']/@content")
        loader.add_xpath(
            'price_currency', "//meta[@itemprop='priceCurrency']/@content")
        loader.add_xpath(
            'spec_name', "//dt[@class='def-list__term']/text()")
        loader.add_xpath(
            'spec_value', "//dd[@class='def-list__definition']/text()")
        loader.add_xpath(
            'photo', "//source[contains(@media, '1024px')]/@srcset")
        yield loader.load_item()

        # _id = response.xpath("//span[@slot='article']/@content").get()
        # name = response.xpath("//h1/text()").get()
        # url = response.url
        # price = response.xpath("//meta[@itemprop='price']/@content").get()
        # price_currency = response.xpath(
        #     "//meta[@itemprop='priceCurrency']/@content").get()
        # spec_name = response.xpath(
        #     "//dt[@class='def-list__term']/text()").getall()
        # spec_value = response.xpath(
        #     "//dd[@class='def-list__definition']/text()").getall()
        # photo = response.xpath(
        #     "//source[contains(@media, '1024px')]/@srcset").getall()
        # yield ParsingItem(_id=_id, name=name, url=url, price=price,
        #                   price_currency=price_currency, spec_name=spec_name,
        #                   spec_value=spec_value, photo=photo)
