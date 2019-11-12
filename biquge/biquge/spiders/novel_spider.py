# -*- coding: utf-8 -*-
import re
import scrapy

from biquge.items import BiqugeItem


class NovelSpiderSpider(scrapy.Spider):
    name = 'novel_spider'
    # allowed_domains = ['www']
    start_urls = ['http://www.xbiquge.la/xuanhuanxiaoshuo/']

    def parse(self, response):
        max_page = response.xpath('//div[@id="pagelink"]/a[@class="last"]/text()').extract_first()
        base_url = response.xpath('//div[@id="pagelink"]/a[@class="last"]/@href').extract_first()
        for i in range(1,int(max_page)+1):
            url = base_url.split('1_401')[0]+'1_{}'+base_url.split('1_401')[1]
            url = url.format(i)
            yield scrapy.Request(url=url,callback=self.parse_novel,dont_filter=True,encoding='utf-8')


    def parse_novel(self,response):
        li_list = response.xpath('//div[@id="newscontent"]/div/ul/li')
        for li in li_list:
            novel_url = li.xpath('./span[@class="s2"]/a/@href').extract_first()
            yield scrapy.Request(url=novel_url,callback=self.parse_chapter,dont_filter=True,encoding='utf-8')


    def parse_chapter(self,response):

        dd_list = response.xpath('//div[@id="list"]/dl/dd')
        for dd in dd_list:
            chapter_url = 'http://www.xbiquge.la' + dd.xpath('./a/@href').extract_first()
            yield scrapy.Request(url=chapter_url,callback=self.parse_content,dont_filter=True,encoding='utf-8')


    def parse_content(self,response):
        item = BiqugeItem()
        title = response.xpath('//div[@class="con_top"]/a[last()]/text()').extract_first()
        chapter = response.xpath('//div[@class="bookname"]/h1/text()').extract_first()
        content = re.sub(r'\s','',''.join(response.xpath('//div[@id="content"]/text()').extract()))
        item['title'] = title
        item['chapter'] = chapter
        item['content'] = content
        item['content'] = response.url
        # print(1)
        yield item


