import requests
import re
import json

class GuBa:

    def __init__(self,url,result):

        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        self.result = result
    def get_html(self):
        try:
            response = requests.get(url=self.url,headers=self.headers)
            response.raise_for_status()
            html = response.content.decode('utf-8')
            return html
        except:
            return False

    def parse_html(self,html):
        ul_pattern = re.compile(r'<ul class="newlist".*?>(.*?)</ul>',re.S)
        ul_content = ul_pattern.search(html).group(1)
        li_pattern = re.compile(r'<li>(.*?)</li>',re.S)
        lis = li_pattern.findall(ul_content)

        for li in lis:
            news_dict = {}
            ## 标题
            title_pattern = re.compile(r'<span class="sub">.*?<a.*?class=".*?note">(.*?)</a></span>',re.S)
            title_pattern1 = re.compile(r'<span class="sub">.*?<a.*?class="balink">(.*?)</a>')
            if title_pattern1.search(li):
                title = '[' + title_pattern1.search(li).group(1) + ']' + title_pattern.search(li).group(1)
            else:
                title = title_pattern.search(li).group(1)
            ## 详情页url
            detail_url_pattern = re.compile(r'<span class="sub">.*?<a .*?href="(.*?)".*?class="note">.*?</a></span>',re.S)
            detail_url = 'http://guba.eastmoney.com' + detail_url_pattern.search(li).group(1)
            ## 阅读量
            read_pattern = re.compile(r'<cite>(.*?)</cite>',re.S)
            read = read_pattern.search(li).group(1).strip(' \n\r')
            ## 评论
            comment_pattern = re.compile(r'<cite>.*?</cite>.*?<cite>(.*?)</cite>',re.S)
            comment = comment_pattern.search(li).group(1).strip('\n\r ')
            ## 作者
            author_pattern = re.compile(r'<cite class="aut">.*?<font>(.*?)</font>',re.S)
            author = author_pattern.search(li).group(1)
            ## 更新时间
            update_pattern = re.compile(r'<cite class="last">(.*?)</cite>',re.S)
            update_date = update_pattern.search(li).group(1)
            news_dict['title'] = title
            news_dict['detail_url'] = detail_url
            news_dict['read'] = read
            news_dict['comment'] = comment
            news_dict['author'] = author
            news_dict['update_date'] = update_date
            self.result.append(news_dict)
        return self.result

    def save_to_json(self):
        with open('guba.json','w',encoding='utf-8') as fp:
            json.dump(self.result,fp)


if __name__ == '__main__':
    base_url = 'http://guba.eastmoney.com/default,99_{}.html'
    result = []
    for i in range(1,13):
        print('开始爬取第%s页'%i)
        url = base_url.format(i)
        guba = GuBa(url,result)
        html = guba.get_html()
        result = guba.parse_html(html)
        guba.save_to_json()

