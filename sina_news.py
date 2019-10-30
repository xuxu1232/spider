import requests

base_url = 'https://search.sina.com.cn/?'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

key = input('请输入关键字')
params = {
    'q': key,
    'c': 'news',
    'from': 'channel',
    'ie': 'utf-8'
}


response = requests.get(url=base_url,headers=headers,params=params)

# print(response.content.decode('gbk'))
with open('sina_news.html','w',encoding='gbk') as fp:
    fp.write(response.content.decode('gbk'))