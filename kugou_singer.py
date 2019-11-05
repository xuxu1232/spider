import requests
from lxml import etree
import json

class KuGou(object):
    def __init__(self):
        self.headers = {
        'Referer': 'https://www.kugou.com/yy/singer/index/1-a-2.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }

    def get_html(self,url):

        response = requests.get(url=url,headers=self.headers)
        html = response.content.decode('utf-8')
        return etree.HTML(html)

    def save_to_json(self,result):
        with open('kugou_singer.json','w',encoding='utf-8') as fp:
            json.dump(result,fp)

    ## 获取歌手详细信息
    def parse_detail(self,url,item):
        html = self.get_html(url)
        singer_info = html.xpath('//div[@class="intro"]/p/text()')
        item['singer_info'] = singer_info
        # print(item)
        self.save_to_json(item)


    ## 获取歌手的基本信息
    def parse_singer(self,url):
        html = self.get_html(url)
        singer_name = html.xpath('//ul[@id="list_head"]/li/strong/a/text()') + html.xpath('//div[@id="list1"]//li/a/text()')
        singer_url = html.xpath('//ul[@id="list_head"]/li/a/@href') + html.xpath('//div[@id="list1"]//li/a/@href')
        singer_rank = html.xpath('//ul[@id="list_head"]/li/a/i/text()') + html.xpath('//div[@id="list1"]//li/span[@class="ran"]/text()')

        for index,name in enumerate(singer_name):
            item = {}
            item['singer_name'] = name
            item['singer_url'] = singer_url[index]
            item['singer_rank'] = singer_rank[index]
            self.parse_detail(singer_url[index],item)


    ## 获取分页的url
    def parse_page(self,url):
        html = self.get_html(url)
        page_urls = html.xpath('//span[@id="mypage"]/a[not(@class)]/@href')

        for page_url in page_urls:
            self.parse_singer(page_url)

    ## 获取按字母分类的url
    def parse_zimu(self,url):
        html = self.get_html(url)
        a_list = html.xpath('//div[@class="num"]/a[not(@id)]')
        for a in a_list:
            zimu_url = a.xpath('./@href')
            if zimu_url:
                self.parse_singer(zimu_url[0])
                self.parse_page(zimu_url[0])

    ## 获取按地区分类的url
    def parse_area(self,url):
        html = self.get_html(url)
        lis = html.xpath('//ul[contains(@class,"sng")]/li[not(@class)]|//ul[@class="sng3"]/li[@class="oth"]')
        for li in lis:
            area_url = li.xpath('./a/@href')
            if area_url:
                self.parse_zimu(area_url[0])

if __name__ == '__main__':
    base_url = 'https://www.kugou.com/yy/html/singer.html'
    kugou = KuGou()
    kugou.parse_area(base_url)