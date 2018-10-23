# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


jstr = __file__.rsplit('\\', 1)[0] + '\\file\\'

class ItcastTeacherPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'teacher_loader':
            with open(jstr + 'teacher_loader.json','a',encoding='utf-8') as f:
                json.dump(item, f, ensure_ascii=False, indent=4)
                f.write("\n")
        return item


class TencentJobPipeline(object):
    def __init__(self):
        self.f = open(jstr + 'tencent_job.json','a',encoding='utf-8')
        self.f.write('[')

    def process_item(self, item, spider):
        if spider.name == 'tencent_job':
            json.dump(dict(item), self.f, ensure_ascii=False, indent=4)
            self.f.write(',')
        return item

    def __del__(self):
        self.f.write('],')
        self.f.close()