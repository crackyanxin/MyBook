# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TalentscoutarticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DetialPageItem(scrapy.Item):
    title = scrapy.Field()
    article_date = scrapy.Field()
    praise = scrapy.Field()
    enshrine = scrapy.Field()
    comment = scrapy.Field()
    detial_img = scrapy.Field()
    pic_name = scrapy.Field()

    # def __str__(self):
    #     return '标题：%s' % title, '发布时间：%s' % article_date, '点赞数：%s' % praise,\
    #           '收藏数：%s' % enshrine, '评论数：%s' % comment