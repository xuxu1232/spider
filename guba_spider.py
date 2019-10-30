import requests
import os

dirname = './guba'
if not os.path.exists(dirname):
    os.mkdir(dirname)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}
for i in range(1,11):
    base_url = 'http://guba.eastmoney.com/default,99_{}.html'.format(i)
    response = requests.get(url=base_url,headers=headers)
    with open(dirname+'/'+'guba_%s.html'%i,'w',encoding='utf-8') as fp:
        fp.write(response.content.decode('utf-8'))


