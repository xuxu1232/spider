# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BiqugeItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    chapter = scrapy.Field()
    content = scrapy.Field()
    content_url = scrapy.Field()
    content_hash = scrapy.Field()
