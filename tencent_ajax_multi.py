import requests,json,time,threading
from queue import Queue

class Tencent(threading.Thread):
    def __init__(self,url,headers,name,q):
        super().__init__()
        self.url = url
        self.headers = headers
        self.name = name
        self.q = q

    def run(self):
        self.get_json_data()

    def get_json_data(self):
        while True:
            if q.empty():
                break
            page = q.get()
            params = {
                'timestamp': str(time.time() * 1000),
                'countryId': ' ',
                'cityId': ' ',
                'bgIds': ' ',
                'productId': ' ',
                'categoryId': ' ',
                'parentCategoryId': ' ',
                'attrId': ' ',
                'keyword': ' ',
                'pageIndex': str(page),
                'pageSize': ' 10',
                'language': ' zh-cn',
                'area': ' cn',
            }
            print(f'线程{self.name}开始抓取第{page}页')
            response = requests.get(url=self.url, headers=self.headers, params=params)
            json_data = json.loads(response.text)
            self.parse_detail_url(json_data)

    def parse_detail_url(self,data):
            # print(json_data)
            tencent_list = []
            for data in data['Data']['Posts']:
                item = {}
                RecruitPostName = data['RecruitPostName']
                CountryName = data['CountryName']
                LocationName = data['LocationName']
                Responsibility = data['Responsibility']
                ProductName = data['ProductName']
                CategoryName = data['CategoryName']
                LastUpdateTime = data['LastUpdateTime']
                detail_url = data['PostURL']
                item['detail_url'] = detail_url
                item['RecruitPostName'] = RecruitPostName
                item['CountryName'] = CountryName
                item['LocationName'] = LocationName
                item['Responsibility'] = Responsibility
                item['ProductName'] = ProductName
                item['CategoryName'] = CategoryName
                item['LastUpdateTime'] = LastUpdateTime
                tencent_list.append(item)
            self.save_to_json(str(tencent_list))
    def save_to_json(self,item):
        with open('tencent_data.txt','a+',encoding='utf-8') as fp:
            fp.write(item)

if __name__ == '__main__':
    start = time.time()
    base_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }

    ## 创建队列任务
    q = Queue()
    ## 将每页的页码加入队列中
    for page in range(1,31):
        q.put(page)
    ## 创建一个列表
    crawl_list = ['aa','bb','cc','dd']
    list_ = []### 用于计算运行时间
    for crawl in crawl_list:
        t = Tencent(base_url,headers,crawl,q)
        t.start()
        list_.append(t)
    for i in list_:
        i.join()
    print(time.time()-start)

