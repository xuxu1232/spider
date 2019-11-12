import requests
import json
from lxml import etree
import re
import threading
from queue import Queue
'''
改成多线程
'''
class YouXin(threading.Thread):
    def __init__(self,url=None,q=None):
        super().__init__()
        self.url = url
        self.q = q
    def run(self):
        self.parse_detail()

    ## 获取json数据
    def get_json_data(self,url):
        headers = {
            'Referer': 'https://www.xin.com/beijing/?channel=a49b117c44837d110753e751863f53',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        response = requests.get(url=url,headers=headers)
        json_data = response.text
        return json_data
    ## 定义判断xpath返回的数据是否为空
    def get_text(self,text):
        if text:
            return text[0]
        else:
            return ''

    ## 获取HTML页面
    def get_html(self,url):
        headers = {
            'Referer': 'https://www.xin.com/beijing/aodi/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        response = requests.get(url=url,headers=headers)
        html = response.content.decode('utf-8')
        return html

    def save_to_json(self,result):
        with open('car.json','a+',encoding='utf-8') as fp:
            json.dump(result,fp)
    def get_max_page(self,url):
        html = self.get_html(url)
        xpath_data = etree.HTML(html)
        max_page = self.get_text(xpath_data.xpath('//div[@class="con-page search_page_link"]/a[last()-1]/text()'))
        return max_page

    ## 解析HTML页面返回的数据
    def parse_detail(self):
        while True:
            if self.q.empty():
                break
            url = self.q.get()
            # print(url)
            max_page = self.get_max_page(url)
            if max_page:
                for i in range(1,int(max_page)+1):
                    #https://www.xin.com/beijing/aodi/i1/?channel=a49b117c44837d110753e751863f53
                    car_url = url.split('?')[0] + 'i{}/?'+url.split('?')[1]
                    # print(car_url.format(i))
                    html = self.get_html(car_url)
                    xpath_data = etree.HTML(html)
                    li_list = xpath_data.xpath('//div[contains(@class,"_list-con")]/ul/li')
                    result_list = []
                    for li in li_list:
                        item = {}
                        title = self.get_text(li.xpath('.//div[@class="pad"]/h2/span/text()'))
                        price = re.sub(r'\s','',self.get_text(li.xpath('.//div[@class="pad"]/p/em/text()')))
                        year = li.xpath('.//div[@class="pad"]/span[1]/text()')[0].strip('\n ')
                        kilometre = li.xpath('.//div[@class="pad"]/span[1]/text()')[1].strip('\n ')
                        detail_url = 'https:' + self.get_text(li.xpath('./div[@class="across"]/a/@href'))
                        image = self.get_text(li.xpath('./div[@class="across"]/a/img/@data-original'))
                        payprice = re.sub(r'\s','',self.get_text(li.xpath('.//div[@class="pad"]/span[@class="pay-price"]/text()')))
                        identification = self.get_text(li.xpath('.//span[contains(@class,"caritem-icon")]/text()'))
                        item['title'] = title
                        item['price'] = price
                        item['year'] = year
                        item['kilometre'] = kilometre
                        item['detail_url'] = detail_url
                        item['image'] = image
                        item['payprice'] = payprice
                        item['identification'] = identification
                        result_list.append(item)
                    # print(result_list)
                        ### 放到字典，保存到json
                    for one in result_list:
                        self.save_to_json(one)

    ### 解析json数据,获取品牌的url
    def parse_json(self):
        car_url_list = []
        json_data = self.get_json_data(self.url)
        p_data = json.loads(json_data)
        for data in p_data['data']:
            for key,value in data.items():
                for one in value:
                    car_url = 'https://www.xin.com/beijing/{}/?channel=a49b117c44837d110753e751863f53'.format(one['pinyin'])
                    car_url_list.append(car_url)
        return car_url_list

if __name__ == '__main__':
    q = Queue()
    base_url = 'https://www.xin.com/apis/Ajax_home/get_home_brand/'
    youxin = YouXin(url=base_url)
    url_list = youxin.parse_json()
    for url in url_list:
        q.put(url)

    crawl_list = ['A','B','C','D']
    for crawl in crawl_list:
        t = YouXin(q=q)
        t.start()





