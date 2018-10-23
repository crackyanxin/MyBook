# -*- coding: utf-8 -*-
import scrapy
from gen_spider.items import TencentJobItem
from urllib import parse


class TencentJobSpider(scrapy.Spider):
    name = 'tencent_job'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    def parse(self, response):
        tr_content = response.xpath('//table[@class="tablelist"]//tr')[1:-1]
        next_url = response.xpath('//a[text()="下一页"]/@href').extract_first()
        for tr in tr_content:
            item = TencentJobItem()
            item['position_href'] = tr.xpath('./td/a/@href').extract_first()
            item['position_name'] = tr.xpath('./td/a/text()').extract_first()
            item['position_category'] = tr.xpath('./td[2]/text()').extract_first()
            item['job_num'] = tr.xpath('./td[3]/text()').extract_first()
            item['work_address'] = tr.xpath('./td[4]/text()').extract_first()
            item['release_time'] = tr.xpath('./td[5]/text()').extract_first()
            # print(item)
            yield item
        if next_url != 'javascript:;':
            next_url = parse.urljoin(TencentJobSpider.start_urls[0], next_url)
            yield scrapy.Request(next_url, callback=self.parse)

