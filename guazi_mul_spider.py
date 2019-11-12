import requests
from lxml import etree
import threading
from queue import Queue

class GuaZi(threading.Thread):
    def __init__(self,url=None,q=None):
        super().__init__()
        self.url = url
        self.q = q

    def run(self):
        self.parse_index()
    def get_text(self,text):
        if text:
            return text[0]
        else:
            return ''

    def get_html(self,url):
        headers = {
            'Referer': 'https://www.guazi.com/bj/?ca_s=pz_baidu&ca_n=tbmkbturl&scode=10103000312&tk_p_mti=ad.pz_baidu.tbmkbturl.1.7535205225402368',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie': 'track_id=7535205225402368; uuid=52468921-359d-4a96-f00e-9deff02b0065; antipas=1P479N1324193629486J96tE6; cityDomain=bj; clueSourceCode=10103000312%2300; user_city_id=12; ganji_uuid=4188309842525416832503; sessionid=0855bf6e-cb90-42a1-eb10-38eb4b8dfe14; lg=1; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22pz_baidu%22%2C%22ca_n%22%3A%22tbmkbturl%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22%22%2C%22ca_campaign%22%3A%22%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%2210103000312%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22ca_transid%22%3A%22%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22track_id%22%3A%227535205225402368%22%2C%22display_finance_flag%22%3A%22-%22%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%2252468921-359d-4a96-f00e-9deff02b0065%22%2C%22ca_city%22%3A%22bj%22%2C%22sessionid%22%3A%220855bf6e-cb90-42a1-eb10-38eb4b8dfe14%22%7D; preTime=%7B%22last%22%3A1572951735%2C%22this%22%3A1572951733%2C%22pre%22%3A1572951733%7D'
        }
        response = requests.get(url=url,headers=headers)
        html = response.content.decode('utf-8')
        return html

    def parse_detail(self,url):
        html = self.get_html(url)
        xpath_data = etree.HTML(html)
        li_list = xpath_data.xpath('//ul[contains(@class,"carlist")]/li')
        car_list = []
        for li in li_list:
            item = {}
            title = self.get_text(li.xpath('.//h2[@class="t"]/text()'))
            price = self.get_text(li.xpath('.//div[@class="t-price"]/p/text()')) +'万'
            year = li.xpath('.//div[@class="t-i"]/text()')[0]
            kilometre = li.xpath('.//div[@class="t-i"]/text()')[1]
            image = self.get_text(li.xpath('//img/@src'))
            detail_url = self.get_text(li.xpath('./a/@href'))
            item['title'] = title
            item['price'] = price
            item['year'] = year
            item['kilometre'] = kilometre
            item['detail_url'] = detail_url
            item['image'] = image
            car_list.append(item)
        print(car_list)
        # for one in car_list:
        #     self.save_to_json(str(one))

    def parse_index(self):
        while True:
            if self.q.empty():
                break
            escar_url = self.q.get()
            html = self.get_html(escar_url)
            xpath_data = etree.HTML(html)
            ## 获取最大页码，进行分页操作
            max_page = self.get_text(xpath_data.xpath('//ul[@class="pageLink clearfix"]/li[last()-1]/a/span/text()'))
            if max_page:
                for i in range(1,int(max_page)+1):
                    url = escar_url.split('#')[0] + 'o{}/' + escar_url.split('#')[1]
                    self.parse_detail(url.format(i))

    def get_es_url(self):
        html = self.get_html(self.url)
        xpath_data = etree.HTML(html)
        a_list = xpath_data.xpath('//div[contains(@class,"js-brand")]/ul/li/p/a')
        car_url_list = []
        for a in a_list:
            escar_url = 'https://www.guazi.com' + self.get_text(a.xpath('./@href'))
            car_url_list.append(escar_url)
        return car_url_list


    def save_to_json(self,result):
        with open('car.txt','a+',encoding='utf-8') as fp:
            fp.write(result)

if __name__ == '__main__':
    base_url = 'https://www.guazi.com/bj/buy/'
    q = Queue()
    guazi = GuaZi(url=base_url)
    es_car_url = guazi.get_es_url()
    # print(es_car_url)
    for one in es_car_url:
        q.put(one)
    crawl_list = ['A','B','C','D']
    for crawl in crawl_list:
        t = GuaZi(q=q)
        t.start()

