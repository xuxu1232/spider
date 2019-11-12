# -*- coding: utf-8 -*-
import scrapy

from music.items import MusicItem


class MusicSpiderSpider(scrapy.Spider):
    name = 'music_spider'
    allowed_domains = ['music.163.com'] ## 限制二次请求可以请求的域名
    ### 起初的url
    start_urls = ['https://music.163.com/discover/artist']

    def parse(self, response):
        li_list = response.xpath('//div[@class="blk"]/ul/li')
        for li in li_list:
            area_url = 'https://music.163.com' + li.xpath('./a/@href').extract_first()
            # print(area_url)
            yield scrapy.Request(url=area_url,callback=self.parse_zimu,dont_filter=True)
            return


    def parse_zimu(self,response):
        # print(response.text)
        li_list = response.xpath('//ul[@id="initial-selector"]/li[position()>1]')
        for li in li_list:
            zimu_url = 'https://music.163.com' + li.xpath('./a/@href').extract_first()
            yield scrapy.Request(url=zimu_url,callback=self.parse_singer,dont_filter=True)
            return
    def parse_singer(self,response):
        li_list = response.xpath('//ul[@id="m-artist-box"]/li')
        for li in li_list:
            item = MusicItem()
            name = li.xpath('./p/a[1]/text()|./a[1]/text()').extract_first()
            #https://music.163.com/#/artist/desc?id=28387245
            #https://music.163.com /artist?id=28387245
            url = 'https://music.163.com' + li.xpath('./p/a[1]/@href|./a[1]/@href').extract_first().split('?')[0].lstrip()+'/desc?'+li.xpath('./p/a[1]/@href|./a[1]/@href').extract_first().split('?')[1]
            item['name'] = name
            item['url'] = url
            yield scrapy.Request(url=url,callback=self.parse_desc,meta={'item':item},dont_filter=True)

    def parse_desc(self,response):
        item = response.meta['item']
        desc = response.xpath('//div[@class="n-artdesc"]/p/text()').extract_first()
        item['desc'] = desc
        print(item)
