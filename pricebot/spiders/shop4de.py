import scrapy
from pricebot.items import Product
from itemadapter import ItemAdapter


class Shop4DeSpider(scrapy.Spider):
    name = "shop4de"
    start_urls = ['https://www.shop4de.com/nintendo-switch-games']
    base_url = "https://www.shop4de.com/nintendo-switch-games/page-"

    def parse(self, response):
        for product in response.css("div.product_box"):
            game = Product()
            game['name'] = product.css("div.top_half h3.title a::text").get()
            game['price'] = product.css("div.bot_half b.price::text").get()
            game['url'] = product.css("div.top_half h3.title a::attr(href)").get()
            yield ItemAdapter(game).asdict()

        current_page = response.css('a#load_more::attr(data-page)').get()
        if current_page is not None:
            next_page = str(int(current_page) + 1)
            final_url = self.base_url + next_page
            yield scrapy.Request(final_url, self.parse)