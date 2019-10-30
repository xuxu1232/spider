import requests
import json


class FanyiBaidu():
    def __init__(self,kw):
        self.base_url = 'https://fanyi.baidu.com/sug'
        self.data = {
            'kw': kw
        }
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://fanyi.baidu.com',
            'Referer': 'https://fanyi.baidu.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def get_html(self):
        response = requests.post(url=self.base_url,headers=self.headers,data=self.data)
        json_data = json.loads(response.text)
        result = ''
        for data in json_data['data']:
            result += data['v']
            result += '\n'
        return result



spider = FanyiBaidu('python')
print(spider.get_html())