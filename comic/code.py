
##### link extractor
class ComicsalesSpider(scrapy.Spider):
    name = "comicsales"
    allowed_domains = ["http://www.comichron.com/"]
    start_urls = [
         "http://www.comichron.com/monthlycomicssales/"
    ]
    rules=Rule(LinkExtractor(allow=))

###### getting urls from monthly sales page
    def parse(self, response):
        for sel in response.xpath('//table[@cellspacing="2"]/tbody/tr/td'):
            print sel
            item = ComicItem()
            item['month'] = sel.xpath("a/big/big/span/text()").extract()
            item['link'] = sel.xpath("a/@href").extract()
            yield item


    def parse(self, response):
        for href in response.xpath('//table[@cellspacing="2"]/tbody/tr/td//a/@href'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_table)

######### parsing sales table
    def parse_table(self, response):
        for sel in response.xpath('//table/tbody/tr[position()>1 and position()<295]'):
            item = TableItem()
            item['rank'] = sel.xpath("td[1]/text()").extract()
            item['title'] = sel.xpath("td[2]/text()").extract()
            item['issue']=sel.xpath("td[3]/text()").extract()
            item['price']=sel.xpath("td[4]/text()").extract()
            item["publisher"]=sel.xpath("td[5]/text()").extract()
            item['orders']=sel.xpath("td[6]/text()").extract()
            yield item

############ following link
def parse(self, response):
    for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
        url = response.urljoin(href.extract())
        yield scrapy.Request(url, callback=self.parse_dir_contents)
def parse_dir_contents(self, response):
    for sel in response.xpath('//ul/li'):
        item = ComicItem()
        item['title'] = sel.xpath('a/text()').extract()
        item['link'] = sel.xpath('a/@href').extract()
        item['desc'] = sel.xpath('text()').extract()
        yield item

##### put rules in url
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class GoogleDirectorySpider(CrawlSpider):
    name = 'directory.google.com'
    allowed_domains = ['directory.google.com']
    start_urls = ['http://directory.google.com/']

    rules = (
        Rule(LinkExtractor(allow='directory\.google\.com/[A-Z][a-zA-Z_/]+$'),
            'parse_category', follow=True,
        ),
    )

    def parse_category(self, response):
    # The path to website links in directory page
        links = response.xpath('//td[descendant::a[contains(@href, "#pagerank")]]/following-sibling::td/font')

        for link in links:
            item = DirectoryItem()
            item['name'] = link.xpath('a/text()').extract()
            item['url'] = link.xpath('a/@href').extract()
            item['description'] = link.xpath('font[2]/text()').extract()
            yield item

######## example of a good spider
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from metacritic.items import MetacriticItem
from string import lowercase


class MetacriticSpider(BaseSpider):
    name = "metacritic"
    allowed_domains = ["metacritic.com"]
    max_id = 5

    def start_requests(self):
        for c in lowercase:
            for i in range(self.max_id):
                yield Request('http://www.metacritic.com/browse/games/title/ps3/{0}?page={1}'.format(c, i),
                              callback=self.parse)

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="product_wrap"]/div')
        items = []

        for site in sites:
            titles = site.xpath('a/text()').extract()
            if titles:
                item = MetacriticItem()
                item['title'] = titles[0].strip()
                items.append(item)
        return items

######### from quick start guide
def parse_articles_follow_next_page(self, response):
      for article in response.xpath("//article"):
          item = ArticleItem()
          item ['title']=sel.xpath('a/text()').extract(head/title)
          yield item

      next_page = response.css("ul.navigation > li.next-page > a::attr('href')")
      if next_page:
          url = response.urljoin(next_page[0].extract())
          yield scrapy.Request(url, self.parse_articles_follow_next_page)
