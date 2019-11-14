import requests
from lxml import etree
import json
import time,random,threading
import re
import pymongo,hashlib
from queue import Queue

class MaFengWo(threading.Thread):
    def __init__(self,url=None,q=None):
        super().__init__()
        self.q = q
        self.url = url
        self.headers = {
            'Referer': 'http://www.mafengwo.cn/flight/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.client = pymongo.MongoClient()
        self.db = self.client['mafengwo']
    def run(self):
        self.parse_detail()

    def get_md5(self,value):
        md5 = hashlib.md5()
        md5.update(value.encode())
        return md5.hexdigest()
    def save_to_mongo(self,item):
        hash_url = self.get_md5(item['detail_url'])
        item['hash_url'] = hash_url
        self.db['travel_addr'].update({'hash_url':item['hash_url']},{'$set':item},True)

    def get_html(self,url):
        try:
            response = requests.get(url=url,headers=self.headers)
            html = response.content.decode('utf-8')
            return html
        except Exception as e:
            return e

    def get_json_data(self,url,params):
        try:
            json_html = requests.get(url=url,params=params,headers=self.headers)
            data = json.loads(json_html.text)
            return data
        except Exception as e:
            return e

    def get_text(self,text):
        if text:
            return text[0]
        else:
            return ''
    ## 获取旅游地点
    def parse_detail(self):
        base_url = 'http://www.mafengwo.cn/sales/ajax_2017.php?'
        while True:
            if self.q.empty():
                break
            to = self.q.get()
            print(to)
            for i in range(1,5):
                params = {
                    'act':'GetContentList',
                    's_dept_time[]':'all',
                    'price[]':'all',
                    'tag_group[9779][]': 'all',
                    'tag_group[12515][]': 'all',
                    'tag_group[12521][]': 'all',
                    'tag_group[12518][]': 'all',
                    'tag_group[12524][]': 'all',
                    'tag_group[9365][]': 'all',
                    'from': '0',
                    'kw':'',
                    'to': to,
                    'salesType':'NaN',
                    'page':str(i),
                    'group':'1',
                    'sort':'smart',
                    'sort_type':'desc',
                    'limit':'20',
                }
                data = self.get_json_data(base_url,params)
                html = data['html']
                xpath_data = etree.HTML(html)
                a_list = xpath_data.xpath('//a')
                for a in a_list:
                    item = {}
                    image = self.get_text(a.xpath('./div[@class="image"]/img/@href'))
                    title = self.get_text(a.xpath('./div[@class="detail"]/div[@class="info"]/h3/text()')).strip('\n ')
                    label = a.xpath('./div[@class="detail"]/div[@class="info"]/div[@class="s-tag"]/span/text()')
                    time = self.get_text(a.xpath('./div[@class="detail"]/div[@class="info"]/p[2]/span/text()'))
                    price = ''.join(a.xpath('./div[@class="detail"]/div[@class="extra"]/span[@class="price"]//text()'))
                    detail_url = 'http://www.mafengwo.cn'+self.get_text(a.xpath('./@href'))
                    item['image'] = image
                    item['title'] = title
                    item['label'] = label
                    item['time'] = time
                    item['price'] = price
                    item['detail_url'] = detail_url
                    self.save_to_mongo(item)
    ### 获取每个城市的url
    def parse_city(self):
        to_list = []
        html_str = self.get_html(self.url)
        xpath_html = etree.HTML(html_str)
        dl_list = xpath_html.xpath('//div[@class="col-left"]/dl|//div[@class="row"]/dl')
        for dl in dl_list:
            city_urls = dl.xpath('./dd/div/span/a/@href')
            city_name = self.get_text(dl.xpath('./dt/text()'))
            for city_url in city_urls:
                if city_name in ['热门','当季热门','高端奢华']:
                    break
                to = re.sub(r'%.*?-',city_name,city_url.split('0-0-')[1])
                to_list.append(to)
        return to_list

if __name__ == '__main__':
    q = Queue()
    base_url = 'http://www.mafengwo.cn/sales/'
    mafengwo = MaFengWo(url=base_url)
    to_list = mafengwo.parse_city()
    for i in to_list:
        q.put(i)

    crawl_list = ['aa','bb','cc','dd']
    for crawl in crawl_list:
        t = MaFengWo(q=q)
        t.start()


