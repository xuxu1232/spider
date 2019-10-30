import requests
import os

base_url = 'http://tieba.baidu.com/f?'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

kw = '易烊千玺'
dirname = './tieba/'+kw
parent_dir = os.path.dirname(dirname)  ## 查找上一级目录
if not os.path.exists(parent_dir):  ## 判断指定目录是否存在，不存在就创建
    os.mkdir(parent_dir)
if not os.path.exists(dirname):
    os.mkdir(dirname)

for page in range(1,11):
    pn = (page-1)*50
    params = {
        'ie': 'utf-8',
        'kw': kw,
        'pn': str(pn)
    }

    response = requests.get(url=base_url,headers=headers,params=params)
    with open(dirname+'/'+kw+'_%s.html'%page,'w',encoding='utf-8') as fp:
        fp.write(response.content.decode('utf-8'))