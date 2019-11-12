# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    actor = scrapy.Field()
    scores = scrapy.Field()
    play_time = scrapy.Field()
    detail_url = scrapy.Field()
    detail_hash = scrapy.Field()

