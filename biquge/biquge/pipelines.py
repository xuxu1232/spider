# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import hashlib

class BiqugePipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client['novel']

    def get_md5(self,value):
        md5 = hashlib.md5()
        md5.update(value.encode())
        return md5.hexdigest()
    def process_item(self, item, spider):
        content_hash = self.get_md5(item['content_url'])
        item['content_hash'] = content_hash
        self.db['novel'].update({'content_hash':item['content_hash']},{'$set':dict(item)},True)
        return item
