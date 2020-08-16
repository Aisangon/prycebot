import scrapy
from scrapy.selector import Selector
from pricebot.items import Product
from itemadapter import ItemAdapter
from urllib.parse import urljoin


class BaseComSpider(scrapy.Spider):
    name = "basecom"
    start_urls = ['https://www.base.com/games/switch/pg735/bn10008264/products.htm?filter=a%3a523%3a375630']
    base_url = "https://www.base.com"

    def parse(self, response):
        for product in response.css("div.plist-centered li.cell"):
            game = Product()
            game['name'] = product.css("div.title a::text").get()
            game['price'] = product.css("div.pricedetail a::text").get()
            game['url'] = urljoin(self.base_url, product.css("div.title a::attr(href)").get()) 

            yield ItemAdapter(game).asdict()

        next_page = Selector(response=response).xpath("//a[contains(text(), 'Next')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)