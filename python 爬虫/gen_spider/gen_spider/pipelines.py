# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, pymysql, logging
from gen_spider.items import EpubBookClassifyItem, EpubBookItem


logger = logging.getLogger(__name__)
jstr = __file__.rsplit('\\', 1)[0] + '\\file\\'


class ItcastTeacherPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'teacher_loader':
            with open(jstr + 'teacher_loader.json', 'a', encoding='utf-8') as f:
                json.dump(item, f, ensure_ascii=False, indent=4)
                f.write("\n")
        return item


class TencentJobPipeline(object):
    def __init__(self):
        self.f = open(jstr + 'tencent_job.json', 'a', encoding='utf-8')
        self.f.write('[')

    def process_item(self, item, spider):
        if spider.name == 'tencent_job':
            json.dump(dict(item), self.f, ensure_ascii=False, indent=4)
            self.f.write(',')
        return item

    def __del__(self):
        self.f.write('],')
        self.f.close()


class EpubBookPipeline(object):
    def open_spider(self, spider):
        if spider.name == 'epub5':
            ip = spider.settings.attributes['MYSQL_IP'].value
            port = spider.settings.attributes['MYSQL_PORT'].value
            self.db = pymysql.connect(host=ip, port=port, user='yan', password="qwer1234",
                                      database='spider_test', charset='utf8')
            self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        if spider.name == 'epub5':
            try:
                if item.isinstance(EpubBookClassifyItem):
                    insert_sql = 'insert into book_classify values(null,%s,%s);'
                    self.cursor.execute(insert_sql, dict(item))
                elif item.isinsstance(EpubBookItem):
                    pass

            except Exception as e:
                spider.logger.log(e)
                self.db.rollback()
        return item

    def close_spider(self, spider):
        if spider.name =='epub5':
            self.cursor.close()
            self.db.close()
