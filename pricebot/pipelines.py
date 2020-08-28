# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# Known html tags you can for telegram formatting <a>, <b>, <strong>, <i> and <em>
from itemadapter import ItemAdapter
from pubsub import pub
from re import search
from pricebot.items import Job, Product

class PricebotPipeline:

    filter_query = ''

    def __init__(self):
        super().__init__()
        pub.subscribe(self.get_query, 'queryTopic')

    def process_item(self, item, spider):
        self.format_item(item)
        return item

    def get_query(self, query):
        self.filter_query = query
        return self.filter_query

    def format_item(self, item):
        if isinstance(item, Product):
            if search(self.filter_query.lower(), str(item['name']).lower()):
                itemHtml = "<a href='{0}'>{1}</a>: <strong>{2}</strong>".format(item['url'], item['name'], item['price'])
        else:
            if search(self.filter_query.lower(), str(item['position']).lower()):
                itemHtml = "<a href='{0}'>{1}</a>: <strong>{2}</strong>".format(item['url'], item['position'], item['company'])

        pub.sendMessage('rootTopic', arg1=itemHtml)
