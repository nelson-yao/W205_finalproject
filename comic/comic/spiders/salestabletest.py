
##### brute force scraping
import scrapy
from comic.items import ComicItem
from comic.items import TableItem


class ComicsalesSpider(scrapy.Spider):
    name = "salestabletest"
    allowed_domains = ["http://www.comichron.com"]
    start_urls = [

    'http://www.comichron.com/monthlycomicssales/2011/2011-10.html',
    'http://www.comichron.com/monthlycomicssales/2011/2011-11.html'

        ]

    def parse(self, response):
        date=response.xpath("//div[@id='content']/div[2]/div[4]/big[1]/big/span/big/big/text()").extract()
        for sel in response.xpath("//table[@width='660']/tbody/tr[contains(td[2], 'Trade Paperback')]/preceding-sibling::tr[not (@class='x168')]"):
            if (sel.xpath("td[1]/text()").extract())[0]!="\n" and (sel.xpath("td[5]/text()").extract())[0]=="Marvel":
                item = TableItem()
                item['date'] = date
                item['rank'] = sel.xpath("td[1]/text()").extract()
                item['title'] = sel.xpath("td[2]/text()").extract()
                item['issue']=sel.xpath("td[3]/text()").extract()
                item['price']=sel.xpath("td[4]/text()").extract()
                item['publisher']=sel.xpath("td[5]/text()").extract()
                item['orders']=sel.xpath("td[6]/text()").extract()
                yield item
