# -*- coding: utf-8 -*-
import scrapy, copy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from gen_spider.items import AmazonClassifyItem



class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.cn']
    start_urls = ['https://www.amazon.cn/Kindle%E7%94%B5%E5%AD%90%E4%B9%A6/b/ref=sd_allcat_books_l2_b116169071?ie=UTF8&node=116169071']

    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths='//span[@class="pagnRA"]'), callback='first_classify'),
    #     # Rule(LinkExtractor(restrict_xpaths='//span[@class="pagnRA"]'), callback='parse_item', follow=True),
    # )

    def parse(self, response):
        lis = response.xpath('//li/a/b[text()="【进口原版】"]/parent::a/parent::li/parent::ul/li')
        for li in lis:
            obj = li.xpath('./a/b')
            if obj:
                item = AmazonClassifyItem()
                item['url'] = li.xpath('./a/@href').extract_first()
                item['classify'] = li.xpath('./a/b/text()').re(r'【(\w+)】')[0]
                yield item
                yield response.follow(item['url'], callback=self.next_classify, meta={'item':copy.deepcopy(item)})

    def next_classify(self, response):
        p_item = response.meta['item']
        lis = response.xpath('//h4[text()="%s"]/parent::span/parent::li/following-sibling::ul[1]/div/li' % p_item['classify'])
        for li in lis:
            item = AmazonClassifyItem()
            item['url'] = li.xpath('.//a/@href').extract_first()
            item['classify'] = li.xpath('.//a/span/text()').extract_first().strip()
            item['p_name'] = p_item['classify']
            yield item
            # yield response.follow(item['url'], callback=self.next_classify, meta={'item':copy.deepcopy(item)})

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
