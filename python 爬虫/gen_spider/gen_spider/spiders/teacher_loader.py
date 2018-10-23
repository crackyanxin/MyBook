# -*- coding: utf-8 -*-
import scrapy


class TeacherLoaderSpider(scrapy.Spider):
    name = 'teacher_loader'
    allowed_domains = ['itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):
        li_content = response.xpath("//div[contains(@class, 'tea_txt')]/ul/li")
        for li in li_content:
            item = {}
            item["href"] = li.xpath("div/img/@data-original").extract_first()
            item["name"] = li.xpath("div/h3/text()").extract_first()
            item["level"] = li.xpath("div/h4/text()").extract_first()
            item["descrption"] = li.xpath("div/p/text()").extract_first()
            yield item

