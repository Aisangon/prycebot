from pricebot.spiders.shop4de import Shop4DeSpider
from pricebot.spiders.basecom import BaseComSpider
from pricebot.spiders.quotes_spider import QuotesSpider

class AllSpiders():

    def __init__(self, spider_list = []):
        super().__init__()
        self._spider_list = spider_list

    def get_list(self):
        self._spider_list = [Shop4DeSpider, BaseComSpider]
        return self._spider_list