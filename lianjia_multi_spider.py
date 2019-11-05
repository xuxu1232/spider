import requests
from lxml import etree
import threading
from queue import Queue


class LianJia(threading.Thread):
    def __init__(self,headers,url=None,q=None):
        super().__init__()
        self.headers = headers
        self.url = url
        self.q = q

    def run(self):
        self.parse()

    def get_text(self, text):
        if text:
            return text[0]
        else:
            return ''

    def get_html(self, url):

        response = requests.get(url=url, headers=headers)
        data = response.content.decode('utf-8')
        return data

    def save_to_json(self, item):
        with open('house.txt', 'a+', encoding='utf-8') as fp:
            fp.write(item)

    def parse_detail(self, url):
        data = self.get_html(url)
        xpath_data = etree.HTML(data)
        li_list = xpath_data.xpath('//ul[@class="sellListContent"]/li')
        house_list = []
        for li in li_list:
            item = {}
            title = self.get_text(li.xpath('.//div[@class="title"]/a/text()'))
            size = self.get_text(li.xpath('.//div[@class="houseInfo"]/text()')).split('|')[0]
            total_price = self.get_text(li.xpath('.//div[@class="totalPrice"]/span/text()')) + '万'
            price = self.get_text(li.xpath('.//div[@class="unitPrice"]/span/text()'))[2:]
            built_time = self.get_text(li.xpath('.//div[@class="houseInfo"]/text()')).split('|')[-2]
            direction = self.get_text(li.xpath('.//div[@class="houseInfo"]/text()')).split('|')[2]
            detail_url = self.get_text(li.xpath('.//div[@class="title"]/a/@href'))
            item['title'] = title
            item['size'] = size
            item['total_price'] = total_price
            item['price'] = price
            item['built_time'] = built_time
            item['direction'] = direction
            item['detail_url'] = detail_url
            house_list.append(item)
        for one in house_list:
            self.save_to_json(str(one))

    def get_url(self):
        url_list = []
        html = self.get_html(self.url)
        xpath_data = etree.HTML(html)
        a_list = xpath_data.xpath('//div[@class="position"]/dl//div[@data-role="ershoufang"]/div/a')
        for a in a_list:
            name = self.get_text(a.xpath('./text()'))
            esf_url = 'https://bj.lianjia.com' + self.get_text(a.xpath('./@href')) + 'pg%s'
            url_list.append((name,esf_url))
        return url_list
    def parse(self):
        while True:
            if self.q.empty():
                break
            esf_url = self.q.get()
            for i in range(5):
                print(esf_url%(i+1))
                self.parse_detail(esf_url % (i + 1))
                # print(esf_url%(i+1))


if __name__ == '__main__':
    base_url = 'https://bj.lianjia.com/ershoufang/'
    headers = {
        'Host': 'bj.lianjia.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    q = Queue()
    lianjia = LianJia( headers=headers,url=base_url)

    url_list = lianjia.get_url()
    for info in url_list:
        q.put(info[1])

    crawl_list = ['aa','bb','cc','dd']
    for crawl in crawl_list:
        t = LianJia(headers=headers,q=q)
        t.start()
