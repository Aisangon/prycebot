# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PricebotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()

class Book(scrapy.Item):
    author = scrapy.Field()
