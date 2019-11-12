# -*- coding: utf-8 -*-
import scrapy


class ZhilianSpiderSpider(scrapy.Spider):
    name = 'zhilian_spider'
    allowed_domains = ['www']
    start_urls = []
    #https://sou.zhaopin.com/?p=2&jl=530&kw=python&kt=3&sf=0&st=0
    #https://sou.zhaopin.com/?p=3&jl=530&kw=python&kt=3&sf=0&st=0
    for i in range(1,2):
        url = 'https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=90&cityId=530&kw=python&kt=3'.format(i)
        start_urls.append(url)

    def parse(self, response):
        print(response.text)