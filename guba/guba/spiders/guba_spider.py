# -*- coding: utf-8 -*-
import scrapy,re

from guba.items import GubaItem


class GubaSpiderSpider(scrapy.Spider):
    name = 'guba_spider'
    # allowed_domains = ['www']
    start_urls = []
    #http://guba.eastmoney.com/default,99_2.html
    for i in range(1):
        url = 'http://guba.eastmoney.com/default,99_{}.html'.format(i)
        start_urls.append(url)

    def parse(self, response):
        # print(response.text)
        item = GubaItem()
        li_list = response.xpath('//ul[@class="newlist"]/li')
        for li in li_list:
            title = li.xpath('./span[@class="sub"]/a[@class="note"]/text()').extract_first()
            read = re.sub('\s','',li.xpath('./cite[1]/text()').extract_first())
            comment = re.sub('\s','',li.xpath('./cite[2]/text()').extract_first())
            author = li.xpath('./cite[@class="aut"]/a/font/text()').extract_first()
            update_time = li.xpath('./cite[@class="date"]/text()').extract_first()
            detail_url = 'http://guba.eastmoney.com'+li.xpath('./span[@class="sub"]/a[@class="note"]/@href').extract_first()
            item['title'] = title
            item['read'] = read
            item['comment'] = comment
            item['author'] = author
            item['update_time'] = update_time
            item['detail_url'] = detail_url
            print(item)
            print(item)
