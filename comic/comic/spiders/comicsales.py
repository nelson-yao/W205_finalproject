# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from comic.items import ComicItem, TableItem


class ComicsalesSpider(scrapy.Spider):
    name = "comicsales"
    allowed_domains = ["http://www.comichron.com"]
    start_urls = [
         "http://www.comichron.com/monthlycomicssales/"
    ]
#    rules=Rule(LinkExtractor(allow="/[1995-2016]-[0-1][1-9]"))

    def parse(self, response):
        for sel in response.xpath('//table[@cellspacing="2"]/tbody/tr/td'):
            print sel
            item = ComicItem()
            item['month'] = sel.xpath("a/big/big/span/text()").extract()
            item['link'] = sel.xpath("a/@href").extract()
            yield item

    def parse_table(self, response):
        for sel in response.xpath('//table/tbody/tr[position()>1 and position()<295]'):
            item = TableItem()
            item['rank'] = sel.xpath("td[1]/text()").extract()
            item['title'] = sel.xpath("td[2]/text()").extract()
            item['issue']=sel.xpath("td[3]/text()").extract()
            item['price']=sel.xpath("td[4]/text()").extract()
            item['publisher']=sel.xpath("td[5]/text()").extract()
            item['orders']=sel.xpath("td[6]/text()").extract()
            yield item
