# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib import parse
from TalentScoutArticle.items import DetialPageItem


# import urlparse  此为python2中的解析函数，用于自动判断当前域名，并拼接出完整的路径


class GetJobbleSpider(scrapy.Spider):
    name = 'get伯乐在线'
    allowed_domains = ['python.jobbole.com']
    start_urls = ['http://python.jobbole.com/all-posts/']

    def parse(self, response):
        # 解析出每个详细页地址，并交给scrapy
        detail_list = response.css('.post.floated-thumb .post-thumb a')
        if detail_list:
            for detial in detail_list:
                detial_page = detial.css('a::attr(href)').extract_first()
                detial_img = detial.css('a img::attr(src)').extract_first()
                yield Request(url=parse.urljoin(response.url, detial_page), meta={'detial_img':detial_img}, callback=self.parse_detail)

        # 爬取下一页
        next_page = response.css('.next.page-numbers::attr(href)').extract_first()
        # print('下一页是：',parse.urljoin(response.url, next_page))
        if next_page:
            yield Request(url=parse.urljoin(response.url, next_page), callback=self.parse)

    def parse_detail(self, response):

        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        article_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first()\
                .strip().replace('·', '')
        # praise = response.xpath('//span[re:test(@class,".*vote-post-up.*")]/h10/text()').extract()
        praise = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract_first()
        praise = self.get_first(praise)
        enshrine = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').re('\d+')
        enshrine = self.get_first(enshrine)
        comment = response.xpath('//span[contains(@class,"hide-on-480")]/text()').re('\d+')
        comment = self.get_first(comment)



        article = DetialPageItem()

        article['title'] = title
        article['article_date'] = article_date
        article['praise'] = praise
        article['enshrine'] = enshrine
        article['comment'] = comment
        article['detial_img'] = [response.meta['detial_img']]

        yield article

    def get_first(self, obj):
        if obj:
            return obj[0]
        else:
            return 0
