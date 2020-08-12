import scrapy
from scrapy import signals
from pubsub import pub
from pricebot.items import Book
import json
from itemadapter import ItemAdapter

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            book = Book()
            book['author'] = quote.css('small.author::text').get()
            yield ItemAdapter(book).asdict()
    
            # yield {
            #     # 'text': quote.css('span.text::text').get(),
            #     'author': quote.css('small.author::text').get()
            #     # 'tags': quote.css('div.tags a.tag::text').getall(),
            # }