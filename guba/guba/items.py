# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GubaItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    read = scrapy.Field()
    comment = scrapy.Field()
    author = scrapy.Field()
    update_time = scrapy.Field()
    detail_url = scrapy.Field()

