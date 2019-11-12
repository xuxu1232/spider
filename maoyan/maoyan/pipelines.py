# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo,hashlib

class MaoyanPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client['maoyan']

    def get_md5(self,value):  ## 将detail_url进行加密
        md5 = hashlib.md5()
        md5.update(value.encode())
        return md5.hexdigest()
    def process_item(self, item, spider):
        detail_hash = self.get_md5(item['detail_url'])
        item['detail_hash'] = detail_hash
        ### 使用update，如果数据库中有数据就更新，没有数据就插入
        self.db['movie'].update({'detail_hash':item['detail_hash']},{'$set':dict(item)},True)
        return item
