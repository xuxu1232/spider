# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo,hashlib
class DoubanPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client['douban']
    def get_md5(self,value):
        md5 = hashlib.md5()
        md5.update(value.encode())
        return md5.hex.digest()
    def process_item(self, item, spider):
        detail_hash = self.get_md5(item['detail_url'])
        item['detail_hash'] = detail_hash
        self.db['python'].update({'detail_hash':item['detail_hash']},{'$set':dict(item)},True)

        return item
