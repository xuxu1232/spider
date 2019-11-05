import requests,json,re
from lxml import etree
import threading
from queue import Queue

class DouBan(threading.Thread):
    def __init__(self,url=None,q=None):
        super().__init__()
        self.url = url
        self.q = q
    def run(self):
        self.parse_ajax()

    def get_text(self,text):
        if text:
            return text[0]
        else:
            return ''

    def get_content(self,url,headers):

        response = requests.get(url=url,headers=headers)
        return response.text


    def parse_json(self,json_data):
        result = []
        for data in json_data:
            item = {}
            rating = data['rating']
            image = data['cover_url']
            types = data['types']
            title = data['title']
            detail_url = data['url']
            vote_count = data['vote_count']
            actors = data['actors']
            item['rating'] = rating
            item['image'] = image
            item['types'] = types
            item['title'] = title
            item['detail_url'] = detail_url
            item['vote_count'] = vote_count
            item['actors'] = actors
            result.append(item)
        print(result)

    def parse_ajax(self):
        base_url = 'https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start={}&limit=20'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'

        }
        while True:
            if self.q.empty():
                break
            type_num = self.q.get()
            i = 0
            while True:
                url = base_url.format(type_num,i)
                # print(url)
                json_str = self.get_content(url,headers=headers)
                if json_str == '[]':
                    break
                json_data = json.loads(json_str)
                self.parse_json(json_data)
                i += 20
    def get_types(self):

        headers = {
            'Referer': 'https://movie.douban.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        html = self.get_content(self.url, headers)
        xpath_data = etree.HTML(html)
        span_list = xpath_data.xpath('//div[@class="types"]/span')
        type_list = []
        for span in span_list:
            type_ = self.get_text(span.xpath('./a/@href'))
            type_num = re.search(r'.*?type_name=(.*?)&type=(.*?)&interval_id.*?', type_).group(2)
            type_name = re.search(r'.*?type_name=(.*?)&type=(.*?)&interval_id.*?', type_).group(1)
            type_list.append((type_num,type_name))
        return type_list
if __name__ == '__main__':
    base_url = 'https://movie.douban.com/chart'
    d = DouBan(url=base_url)
    type_info = d.get_types()
    q = Queue()
    for info in type_info:
        q.put(info[0])

    crawl_list = [1,2,3,4]
    for crawl in crawl_list:
        t = DouBan(q=q)
        t.start()

