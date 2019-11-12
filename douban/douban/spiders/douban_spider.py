# -*- coding: utf-8 -*-
import scrapy

from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    # allowed_domains = ['www']
    # start_urls = []

    ### 将请求初始url 放在start_requests方法中，作用和start_urls一样
    def start_requests(self):
        for i in range(1):
            url = 'https://search.douban.com/book/subject_search?search_text=python&cat=1001&start={}'.format(i * 15)
            yield scrapy.Request(url=url,callback=self.parse,meta={'xpath':'//div[@id="root"]'})
    def parse(self, response):
        div_list = response.xpath('//div[@id="root"]/div/div/div/div/div')
        response.urljoin()
        # print(div_list)
        for div in div_list:
            item = DoubanItem()
            title = div.xpath('.//div[@class="title"]/a/text()').extract_first()
            author = div.xpath('.//div[@class="meta abstract"]/text()').extract_first()
            score = div.xpath('.//span[@class="rating_nums"]/text()').extract_first()
            comment_num = div.xpath('.//span[@class="pl"]/text()').extract_first()
            detail_url = div.xpath('.//div[@class="title"]/a/@href').extract_first()
            if all([title,detail_url]):

                item['title'] = title
                item['author'] = author.split('/')[:-3]
                item['score'] = score
                item['comment_num'] = comment_num
                item['detail_url'] = detail_url
                yield item
