from pricebot.spiders.shop4de import Shop4DeSpider
from pricebot.spiders.basecom import BaseComSpider
from pricebot.spiders.remotive import RemotiveSpider
from pricebot.spiders.remoteok import RemoteOkSpider
from pricebot.spiders.workingnomads import WorkingNomadsSpider

class AllSpiders():

    def __init__(self, spider_list = dict()):
        super().__init__()
        self._spider_list = spider_list

    def get_list(self):
        self._spider_list = dict(
            Games=[Shop4DeSpider, BaseComSpider],
            Jobs=[RemotiveSpider, RemoteOkSpider, WorkingNomadsSpider]
        )
        return self._spider_list