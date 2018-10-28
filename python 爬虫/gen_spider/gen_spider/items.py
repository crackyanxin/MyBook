# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentJobItem(scrapy.Item):
    '''腾讯招聘'''
    position_href = scrapy.Field()
    position_name = scrapy.Field()
    position_category = scrapy.Field()
    job_num = scrapy.Field()
    work_address = scrapy.Field()
    release_time = scrapy.Field()

class EpubBookClassifyItem(scrapy.Item):
    '''Epub网站分类'''
    classify = scrapy.Field()
    url = scrapy.Field()

class EpubBookItem(scrapy.Item):
    '''Epub网站书籍类'''
    book_name = scrapy.Field()
    size = scrapy.Field()
    make_date = scrapy.Field()
    money = scrapy.Field()
    book_description = scrapy.Field()
    update_time = scrapy.Field()
    url = scrapy.Field()