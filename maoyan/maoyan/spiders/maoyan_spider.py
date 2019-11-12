# -*- coding: utf-8 -*-
import scrapy

from maoyan.items import MaoyanItem


class MaoyanSpiderSpider(scrapy.Spider):
    name = 'maoyan_spider'
    # allowed_domains = ['www']
    start_urls = []
    #https://maoyan.com/board/4?offset=10
    for i in range(10):
        url = 'https://maoyan.com/board/4?offset={}'.format(i*10)
        start_urls.append(url)

    def parse(self, response):
        item = MaoyanItem()
        dd_list = response.xpath('//dl[@class="board-wrapper"]/dd')
        for dd in dd_list:
            title = dd.xpath('.//p[@class="name"]/a/text()').extract_first()
            actor = dd.xpath('.//p[@class="star"]/text()').extract_first().strip(' \n')[3:]
            scores = ''.join(dd.xpath('.//p[@class="score"]/i/text()').extract())
            play_time = dd.xpath('.//p[@class="releasetime"]/text()').extract_first()[5:]
            detail_url = 'https://maoyan.com' + dd.xpath('.//p[@class="name"]/a/@href').extract_first()
            item['title'] = title
            item['actor'] = actor
            item['scores'] = scores
            item['play_time'] = play_time
            item['detail_url'] = detail_url
            yield item
