import scrapy
from scrapy import signals

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    message = "Hi"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.response_received, signal=signals.response_received)
        return spider

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

    def get_message(self, response):
        self.message = response

    def item_scraped(self, item, response):
        self.get_message(response)

    def response_received(self, response, request, spider):
        print("received!!!")
        self.message = response
    
