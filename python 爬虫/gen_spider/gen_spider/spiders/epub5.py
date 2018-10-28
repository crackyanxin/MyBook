# -*- coding: utf-8 -*-
import scrapy
from gen_spider.items import EpubBookClassifyItem, EpubBookItem


class Epub5Spider(scrapy.Spider):
    name = 'epub5'
    allowed_domains = ['www.epub5.com']
    start_urls = ['http://www.epub5.com/freebooks/index.html']

    def parse(self, response):
        book_classify = response.xpath('//div[@class="topmenu cbody"]//li')[1:]
        for book_cls in book_classify:
            item = EpubBookClassifyItem()
            item['classify'] = book_cls.xpath('.//a/text()').extract_first()
            item['url'] = book_cls.xpath('.//a/@href').extract_first()
            yield item
