# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentJobItem(scrapy.Item):
    position_href = scrapy.Field()
    position_name = scrapy.Field()
    position_category = scrapy.Field()
    job_num = scrapy.Field()
    work_address = scrapy.Field()
    release_time = scrapy.Field()
