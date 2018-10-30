# -*- coding: utf-8 -*-
import scrapy, time
from gen_spider.items import EpubBookClassifyItem, EpubBookItem


class Epub5Spider(scrapy.Spider):
    name = 'epub5'
    allowed_domains = ['www.epub5.com']
    start_urls = ['http://www.epub5.com/freebooks/index.html']
    classify_count = 0

    def parse(self, response):
        if Epub5Spider.classify_count == 0:
            book_classify = response.xpath('//div[@class="topmenu cbody"]//li')[1:]
            for book_cls in book_classify:
                item = EpubBookClassifyItem()
                item['classify'] = book_cls.xpath('.//a/text()').extract_first()
                item['url'] = book_cls.xpath('.//a/@href').extract_first()
                yield item
                # yield response.follow(item['url'], callback=self.parse)
            Epub5Spider.classify_count += 1

        detail_urls = response.xpath('//ul[contains(@class, "listbody")]/li/a[2]/@href').extract()
        # for url in detail_urls:
        #     yield response.follow(url, callback=self.parse_detail)
        #
        # next_url = response.xpath('//div[@class="page_list"]/a[text()="下页"]/@href').extract_first()
        # yield response.follow(next_url, callback=self.parse)



    def parse_detail(self, response):
        item = EpubBookItem()
        uls = response.xpath('//div[@class="sinfo"]/ul')
        for ul in uls:
            item['book_name'] = ul.xpath('li[1]/h1/text()').extract_first()
            item['book_author'] = ul.xpath('li[2]/text()').extract_first()
            item['size'] = ul.xpath('li[4]/text()').extract_first()
            item['make_date'] = ul.xpath('li[6]/text()').extract_first()
            item['money'] = ul.xpath('li[6]/em/text()').extract_first()
            item['book_description'] = ul.xpath('../../div[@class="sintro"]/span/text()').extract_first()
            item['url'] = response.url
            item['classify_name'] = response.xpath('//li[@class="thisclass"]/a/text()').extract_first()
            yield item