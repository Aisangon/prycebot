from pricebot.spiders.shop4de import Shop4DeSpider
from pricebot.spiders.basecom import BaseComSpider
from pricebot.spiders.remotive import RemotiveSpider

class AllSpiders():

    def __init__(self, spider_list = dict()):
        super().__init__()
        self._spider_list = spider_list

    def get_list(self):
        self._spider_list = dict(
            Games=[Shop4DeSpider, BaseComSpider],
            Jobs=[RemotiveSpider]
        )
        return self._spider_list