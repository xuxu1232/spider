import requests
from lxml import etree
import json

class ShanBei(object):
    def __init__(self,url,result):
        self.url = url
        self.result = result
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def get_html(self):
        try:
            response = requests.get(url=self.url,headers=self.headers)
            response.raise_for_status()
            html = response.content.decode('utf-8')
            # print(html)
            self.parse_html(html)
        except:
            return False
    def parse_html(self,html):
        xpath_html = etree.HTML(html)
        trs = xpath_html.xpath('//table[contains(@class,"table-bordered")]/tbody/tr')
        for tr in trs:
            item = {}
            word = tr.xpath('./td[@class="span2"]/strong/text()')[0]
            means = tr.xpath('./td[@class="span10"]/text()')[0]
            item[word] = means
            self.result.append(item)
        self.save_to_json(self.result)

    def save_to_json(self,result):
        with open('shanbei.json','w',encoding='utf-8') as fp:
            json.dump(result,fp)

if __name__ == '__main__':
    result = []
    base_url = 'https://www.shanbay.com/wordlist/110521/232414/?page={}'
    for i in range(1,4):
        url = base_url.format(i)
        shanbei = ShanBei(url,result)
        shanbei.get_html()