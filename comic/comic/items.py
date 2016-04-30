# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ComicItem(scrapy.Item):
    month = scrapy.Field()
    link = scrapy.Field()

class ArticleItem(scrapy.Item):
    title = scrapy.Field()

class TableItem(scrapy.Item):
    date=scrapy.Field()
    rank= scrapy.Field()
    title = scrapy.Field()
    issue = scrapy.Field()
    price = scrapy.Field()
    publisher =scrapy.Field()
    orders = scrapy.Field()
