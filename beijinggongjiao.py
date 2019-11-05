import requests
import time
from lxml import etree
import random
import json

## 添加随机请求头解决403问题
def get_random_headers():
    my_headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
    ]

    user_agent = random.choice(my_headers)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'beijing.gongjiao.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':user_agent
    }
    return headers

def get_html(url):
    headers =get_random_headers()
    response = requests.get(url=url,headers=headers)
    html = response.content.decode('utf-8')
    return etree.HTML(html)

def parse_detail(url,item):
    html = get_html(url)
    start = html.xpath('//div[contains(@class,"gj01_line_header")]/dl/dt/a[1]/text()')
    end = html.xpath('//div[contains(@class,"gj01_line_header")]/dl/dt/a[2]/text()')
    time = html.xpath('//div[contains(@class,"gj01_line_header")]/dl/dd/b/text()')
    gongsi = html.xpath('//div[contains(@class,"gj01_line_header")]/dl/dd/text()')
    station_count = html.xpath('//div[@class="gj01_lineSite_title"]/b/text()')
    station_up = html.xpath('//ul[contains(@class,"JS-up")]/li/a/text()')
    station_down = html.xpath('//ul[contains(@class,"JS-down")]/li/a/text()')
    item['start'] = start
    item['end'] = end
    item['time'] = time
    item['gongsi'] = gongsi
    item['station_count'] = station_count
    item['station_up'] = station_up
    item['station_down'] = station_down
    result.append(item)
    return result


def parse_bus(url):
    html = get_html(url)
    # print(etree.tostring(html,pretty_print=True,encoding='utf-8'))
    li_list = html.xpath('//div[@class="list"]/ul/li')
    for li in li_list:
        item = {}
        bus_name = li.xpath('./a/text()')
        bus_url = li.xpath('./a/@href')
        item['bus_name'] = bus_name[0]
        item['bus_url'] = bus_url[0]
        # print(bus_url[0])
        time.sleep(1)
        parse_detail(bus_url[0],item)


def parse_index(url):
    html = get_html(url)
    a_list = html.xpath('//div[contains(@class,"gj01_item_01")]//li[contains(@class,"gj01_item_con_hover1")]/a')
    for a in a_list:
        index_url = 'http://beijing.gongjiao.com' + a.xpath('./@href')[0]
        # print(index_url)
        parse_bus(index_url)

def save_to_json(result):
    with open('bus.json','w',encoding='utf-8') as fp:
        json.dump(result,fp)


if __name__ == '__main__':
    result = []
    base_url = 'http://beijing.gongjiao.com/'
    data = parse_index(base_url)
    save_to_json(data)







