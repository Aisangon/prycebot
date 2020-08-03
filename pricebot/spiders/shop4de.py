import scrapy


class Shop4DeSpider(scrapy.Spider):
    name = "shop4de"

    start_urls = [
        'https://www.shop4de.com/nintendo-switch-games'
    ]

    def parse(self, response):
        for product in response.css("div.product_box"):
            yield {
                'name': product.css("div.top_half h3.title a::text").get(),
                'price': product.css("div.bot_half b.price::text").get()
            }