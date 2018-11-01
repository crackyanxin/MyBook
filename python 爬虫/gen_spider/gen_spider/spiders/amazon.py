# -*- coding: utf-8 -*-
import scrapy, copy, re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from gen_spider.items import AmazonClassifyItem, AmazonBookItem


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.cn']
    start_urls = [
        'https://www.amazon.cn/Kindle%E7%94%B5%E5%AD%90%E4%B9%A6/b/ref=sd_allcat_books_l2_b116169071?ie=UTF8&node=116169071']

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
                item['p_name'] = ''
                yield item
                yield response.follow(item['url'], callback=self.next_classify, meta={'item': copy.deepcopy(item)})
                # yield response.follow('https://www.amazon.cn/s/ref=lp_143231071_nr_n_11?fst=as%3Aoff&rh=n%3A116087071%2Cn%3A%21116088071%2Cn%3A116169071%2Cn%3A143231071%2Cn%3A143244071&bbn=143231071&ie=UTF8&qid=1540958531&rnid=143231071', callback=self.next_classify, meta={'item': copy.deepcopy(item)})

    def next_classify(self, response):
        p_item = response.meta['item']
        lis = response.xpath('//h4[text()="%s"]/parent::span/parent::li/following-sibling::ul[1]/div/li' % p_item['classify'])
        # yield response.follow('https://www.amazon.cn/dp/B00G3L13DS/ref=lp_141702071_1_2?s=digital-text&ie=UTF8&qid=1540996098&sr=1-2', callback=self.book_detail, meta={'classify': p_item['classify']})
        if lis:
            #若能抓到li标签，说明还有子节点，继续循环。否则抓取图书列表
            for li in lis:
                item = AmazonClassifyItem()
                item['url'] = li.xpath('.//a/@href').extract_first()
                item['classify'] = li.xpath('.//a/span/text()').extract_first().strip()
                item['p_name'] = p_item['classify']
                yield item
                yield response.follow(item['url'], callback=self.next_classify, meta={'item': copy.deepcopy(item)})
        else:
            detail_urls = response.xpath('//div[@id="mainResults"]//a[contains(@class, "s-access-detail-page")]')
            next_page = response.xpath('//span[@class="pagnRA"]/a/span[text()="下一页"]/parent::a/@href').extract_first()
            for detail_url in detail_urls:
                yield response.follow(detail_url, callback=self.book_detail, meta={'classify': p_item['classify']})
            yield response.follow(next_page, callback=self.next_classify, meta={'item': p_item})

    def book_detail(self, response):
        try:
            item = AmazonBookItem()
            item['classify_id'] = response.meta['classify']
            item['book_name'] = response.xpath('//span[@id="ebooksProductTitle"]/text()').extract_first().strip()
            item['book_author'] = response.xpath('//div[@id="bylineInfo"]//text()').extract()
            item['book_author'] = ' '.join([i for i in item['book_author'] if re.findall(r'\w+', i)])
            item['book_price'] = response.xpath('//li[contains(@class, "swatchElement")]//span[contains(@class, "a-color-base")]/span[contains(@class, "a-color-price")]/text()').extract_first().strip()
            item['publish_date'] = response.xpath('//div[@class="buying"]/span[@style="font-weight: bold;"]/text()').extract_first()
            if item['publish_date']:
                item['publish_date'] = '-'.join(re.search(r'.*?(\d+)年(\d+)月(\d+).*', item['publish_date']).groups())
            item['description'] = ''.join(response.xpath('//div[@id="postBodyPS"]//text()').extract()).strip()
            item['file_size'] = response.xpath('//div[@id="detail_bullets_id"]//div[@class="content"]/ul/li/b[text()="文件大小："]//parent::li/text()').extract_first().strip()
            item['language'] = response.xpath('//div[@id="detail_bullets_id"]//div[@class="content"]/ul/li/b[text()="语种："]//parent::li/text()').extract_first().strip()
            item['publishing_house'] = response.xpath('//div[@id="detail_bullets_id"]//div[@class="content"]/ul/li/b[text()="出版社:"]//parent::li/text()').extract_first()
            yield item
        except Exception as e:
            print(e)
            with open(item['classify_id']+'.html', 'wb') as f:
                f.write(response.body)