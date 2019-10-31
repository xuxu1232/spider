import json
import requests
import re

class YaoWang:
    def __init__(self,url,result):
        self.url = url
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        self.result = result
    def get_html(self):
        try:
            response = requests.get(url=self.url,headers=self.headers)
            response.raise_for_status()
            html = response.content.decode('gbk')
            self.parse_html(html)
        except:
            return False

    def parse_html(self,html):
        ul_pattern = re.compile(r'<ul id="itemSearchList".*?>(.*?)</ul>',re.S)
        ul_content = ul_pattern.search(html).group(1)
        li_pattern = re.compile(r'<li.*?>(.*?)</li>',re.S)
        lis = li_pattern.findall(ul_content)
        for li in lis:
            medicine_dict = {}
            price_pattern = re.compile(r'<p class="price".*?<span>(.*?)</span>',re.S)
            price = price_pattern.search(li).group(1).strip('\n\r ')
            description_pattern = re.compile(r'<p class="titleBox">.*?<a class="productName.*?></span>(.*?)</a>',re.S)
            description = re.sub(r'\n','',description_pattern.search(li).group(1)).strip()
            comment_pattern = re.compile(r'<div class="sell_type_div">.*?<em>(.*?)</em>',re.S)
            if comment_pattern.search(li):
                comment = comment_pattern.search(li).group(1)
            else:
                comment = 0

            detail_pattern = re.compile(r'<p class="titleBox">.*?<a class="productName.*?href="(.*?)".*?>',re.S)
            detail = 'https:'+detail_pattern.search(li).group(1)
            medicine_dict['price'] = price
            medicine_dict['description'] = description
            medicine_dict['detail'] = detail
            medicine_dict['comment'] = comment
            self.result.append(medicine_dict)
        self.save_to_json(self.result)



    def save_to_json(self,result):
        with open('yaowang.json','w',encoding='gbk') as fp:
            json.dump(result,fp)

if __name__ == '__main__':
    result = []
    base_url = 'https://www.111.com.cn/categories/953710-j{}.html'
    for i in range(1,51):
        url = base_url.format(i)
        print('开始爬取第%s页'%i)
        yaowang = YaoWang(base_url,result)
        yaowang.get_html()
