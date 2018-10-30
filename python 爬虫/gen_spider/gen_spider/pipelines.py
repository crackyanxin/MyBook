# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, pymysql, logging
from gen_spider.items import EpubBookClassifyItem, EpubBookItem, AmazonClassifyItem

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
        ip = spider.settings.attributes['MYSQL_IP'].value
        port = spider.settings.attributes['MYSQL_PORT'].value
        self.db = pymysql.connect(host=ip, port=port, user='yan', password="qwer1234",
                                  database='spider_test', charset='utf8')
        self.cursor = self.db.cursor()
        self.cursor.execute('select classify, id from book_classify')
        self.classify = dict(self.cursor.fetchall())
        spider.mysql_cli = self

    def process_item(self, item, spider):
        if spider.name == 'epub5':
            try:
                if isinstance(item, AmazonClassifyItem):
                    insert_sql = 'insert into book_classify(classify, url) values(%(classify)s,%(url)s);'
                elif isinstance(item, EpubBookItem):
                    classify_id = str(self.classify[item['classify_name']])
                    insert_sql = 'insert into book(book_name, book_author, size, make_date, money, book_description,' \
                                 'update_time, url, classify_id) values(%(book_name)s,%(book_author)s,%(size)s,' \
                                 '%(make_date)s,%(money)s,%(book_description)s,now(),%(url)s,' + classify_id + ')'
                self.cursor.execute(insert_sql, dict(item))
                self.db.commit()
            except Exception as e:
                logger.error(e)
                self.db.rollback()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()


class AmazonClassifyPipeline(object):

    def open_spider(self, spider):
        #启动时预先加载所有classify避免后期过度搜索
        spider.mysql_cli.cursor.execute('select classify, id, pid from amazon_book_classify')
        self.classify = dict(spider.mysql_cli.cursor.fetchall())
        pass

    def process_item(self, item, spider):
        if spider.name == 'amazon':
            try:
                if isinstance(item, AmazonClassifyItem):
                    #判断父分类是否存在，如果存在则创建子分类，否则创建父分类
                    insert_sql = None
                    for detail in self.classify:
                        if item['p_name'] in self.classify:
                            insert_sql = 'insert into amazon_book_classify(classify, url, pid) values(%(classify)s,%(url)s,%(p_name)s);'
                            item['p_name'] = detail['pid']
                    if not insert_sql:
                        insert_sql = 'insert into amazon_book_classify(classify, url) values(%(classify)s,%(url)s);'
                    spider.mysql_cli.cursor.execute(insert_sql, dict(item))
                    spider.mysql_cli.db.commit()
                    self.open_spider(spider)
                # elif isinstance(item, EpubBookItem):
                #     classify_id = str(self.classify[item['classify_name']])
                #     insert_sql = 'insert into book(book_name, book_author, size, make_date, money, book_description,' \
                #                  'update_time, url, classify_id) values(%(book_name)s,%(book_author)s,%(size)s,' \
                #                  '%(make_date)s,%(money)s,%(book_description)s,now(),%(url)s,' + classify_id + ')'
                # self.cursor.execute(insert_sql, dict(item))
                # self.db.commit()
            except Exception as e:
                logger.error(e)
                self.db.rollback()
        return item
