# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pubsub import pub


class PricebotPipeline:
    def process_item(self, item, spider):
        html = '<i>' + '- ' + item['author'] + '</i>'
        pub.sendMessage('rootTopic', arg1=html)
        return item
