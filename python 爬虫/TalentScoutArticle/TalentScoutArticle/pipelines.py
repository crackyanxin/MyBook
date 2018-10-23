# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import uuid
from scrapy.pipelines.images import ImagesPipeline

class DownPicturePipeline(object):
    '''
    手写版图片下载器
    '''
    def process_item(self, item, spider):
        local_url = './Talentscoutarticle/picture/' + item['pic_name']
        down_picture = requests.get(item['detial_img'])
        with open(local_url, 'wb') as f:
            f.write(down_picture.content)
        return item

class ExtendImagesPipeline(ImagesPipeline):
    '''
    图片下载后得到其真实存放路径并存入 pic_name 中
    '''
    def item_completed(self, results, item, info):
        for ok, real_path in results:
            if ok:
                item['pic_name'] = real_path['path']



class ToMysqlPipeline(object):
    '''
    将下载的数据处理完后存入mysql中
    '''
    def process_item(self, item, spider):
        picture = item['detial_img'][0]
        tail = picture.rsplit('.', 1)
        pic_name = uuid.uuid1().hex + '.' + tail[1]
        item['pic_name'] = pic_name



        return item