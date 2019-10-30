import requests
import json

class JinShanCiBa():
    def __init__(self,kw):
        self.base_url = 'http://fy.iciba.com/ajax.php?a=fy'
        self.headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Length': '23',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://fy.iciba.com',
        'Referer': 'http://fy.iciba.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
        self.data = {
        'f': 'auto',
        't': 'auto',
        'w': kw
    }

    def get_response(self):
        response = requests.post(url=self.base_url,headers=self.headers,data=self.data)
        response = json.loads(response.text)
        result = ''
        for i in response['content']['word_mean']:
            result += i
            result += '\n'
        return result

if __name__ == '__main__':
    kw = input('请输入要翻译的单词：')
    word = JinShanCiBa(kw)
    result = word.get_response()
    print(result)


