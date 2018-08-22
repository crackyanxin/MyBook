# -*- coding: utf-8 -*-
__author__ = 'Javk Yan'

from scrapy.cmdline import execute
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.dirname(os.path.abspath(__file__)))

execute(['scrapy', 'crawl', 'get伯乐在线'])

'''
文章列表页
scrapy shell http://python.jobbole.com/all-posts/

文章详细页
scrapy shell http://python.jobbole.com/89252/

'''