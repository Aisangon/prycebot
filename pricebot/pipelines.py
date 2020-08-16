# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pubsub import pub
from re import search


class PricebotPipeline:

    filter_query = ''
    def __init__(self):
        super().__init__()
        pub.subscribe(self.listener2, 'queryTopic')

    def process_item(self, item, spider):
        if search(self.filter_query.lower(), str(item['author']).lower()):
            html = '<i>' + '- ' + item['author'] + '</i>'
            pub.sendMessage('rootTopic', arg1=html)
            
        return item

    def listener2(self, query):
        self.filter_query = query
        return self.filter_query

