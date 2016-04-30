
##### brute force scraping
import scrapy
from comic.items import ComicItem
from comic.items import TableItem


class ComicsalesSpider(scrapy.Spider):
    name = "salestable2012"
    allowed_domains = ["http://www.comichron.com"]
    start_urls = [
    'http://www.comichron.com/monthlycomicssales/2012/2012-01.html',
    'http://www.comichron.com/monthlycomicssales/2012/2012-02.html',
    'http://www.comichron.com/monthlycomicssales/2012/2012-03.html',
    'http://www.comichron.com/monthlycomicssales/2012/2012-04.html',
    'http://www.comichron.com/monthlycomicssales/2012/2012-05.html',
    'http://www.comichron.com/monthlycomicssales/2012/2012-06.html',
    'http://www.comichron.com/monthlycomicssales/2012/2012-07.html',
    'http://www.comichron.com/monthlycomicssales/2012/2012-08.html',
    'http://www.comichron.com/monthlycomicssales/2012/2012-09.html',
    'http://www.comichron.com/monthlycomicssales/2012/2012-10.html',
    'http://www.comichron.com/monthlycomicssales/2012/2012-11.html',
    'http://www.comichron.com/monthlycomicssales/2012/2012-12.html',
    'http://www.comichron.com/monthlycomicssales/2013/2013-01.html',
    'http://www.comichron.com/monthlycomicssales/2013/2013-02.html',
    'http://www.comichron.com/monthlycomicssales/2013/2013-03.html',
    'http://www.comichron.com/monthlycomicssales/2013/2013-04.html',
    'http://www.comichron.com/monthlycomicssales/2013/2013-05.html',
    'http://www.comichron.com/monthlycomicssales/2013/2013-06.html',
    'http://www.comichron.com/monthlycomicssales/2013/2013-07.html',
    'http://www.comichron.com/monthlycomicssales/2013/2013-08.html',
    'http://www.comichron.com/monthlycomicssales/2013/2013-09.html',
    'http://www.comichron.com/monthlycomicssales/2013/2013-10.html',
    'http://www.comichron.com/monthlycomicssales/2013/2013-11.html',
    'http://www.comichron.com/monthlycomicssales/2013/2013-12.html',
    'http://www.comichron.com/monthlycomicssales/2014/2014-01.html',
    'http://www.comichron.com/monthlycomicssales/2014/2014-02.html',
    'http://www.comichron.com/monthlycomicssales/2014/2014-03.html',
    'http://www.comichron.com/monthlycomicssales/2014/2014-04.html',
    'http://www.comichron.com/monthlycomicssales/2014/2014-05.html',
    'http://www.comichron.com/monthlycomicssales/2014/2014-06.html',
    'http://www.comichron.com/monthlycomicssales/2014/2014-07.html',
    'http://www.comichron.com/monthlycomicssales/2014/2014-08.html',
    'http://www.comichron.com/monthlycomicssales/2014/2014-09.html',
    'http://www.comichron.com/monthlycomicssales/2014/2014-10.html',
    'http://www.comichron.com/monthlycomicssales/2014/2014-11.html',
    'http://www.comichron.com/monthlycomicssales/2014/2014-12.html',
    'http://www.comichron.com/monthlycomicssales/2015/2015-01.html',
    'http://www.comichron.com/monthlycomicssales/2015/2015-02.html',
    'http://www.comichron.com/monthlycomicssales/2015/2015-03.html',
    'http://www.comichron.com/monthlycomicssales/2015/2015-04.html',
    'http://www.comichron.com/monthlycomicssales/2015/2015-05.html',
    'http://www.comichron.com/monthlycomicssales/2015/2015-06.html',
    'http://www.comichron.com/monthlycomicssales/2015/2015-07.html',
    'http://www.comichron.com/monthlycomicssales/2015/2015-08.html',
    'http://www.comichron.com/monthlycomicssales/2015/2015-09.html',
    'http://www.comichron.com/monthlycomicssales/2015/2015-10.html',
    'http://www.comichron.com/monthlycomicssales/2015/2015-11.html',
    'http://www.comichron.com/monthlycomicssales/2015/2015-12.html',
    'http://www.comichron.com/monthlycomicssales/2016/2016-01.html',
    'http://www.comichron.com/monthlycomicssales/2016/2016-02.html',
    'http://www.comichron.com/monthlycomicssales/2016/2016-03.html'
        ]

    def parse(self, response):
        date=response.xpath("//div[@id='content']/div/div[4]/big[1]/big/span/big/big/text()").extract()
        for sel in response.xpath("//table[@width='660']/tbody/tr[contains(td[2], 'Trade Paperback')]/preceding-sibling::tr"):
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
