import requests
import re
import json

class TieBa(object):
    def __init__(self,url,result):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        self.result = result

    def get_html(self):

        response = requests.get(url=self.url,headers=self.headers)
        response.raise_for_status()
        html = response.content.decode('utf-8')
        # print(html)
        self.parse_html(html)

    def parse_html(self,html):
        ul_pattern = re.compile(r'<ul id="thread_list".*?>(.*)</ul>',re.S)
        ul_content = ul_pattern.search(html).group()
        li_pattern = re.compile(r'<li class=" j_thread_list.*?>(.*?)</li>',re.S)
        lis = li_pattern.findall(ul_content)
        for li in lis:
            item = {}
            title_pattern = re.compile(r'<div class=".*?pull_left j_th_tit.*?>.*?<a.*?>(.*?)</a>',re.S)
            if title_pattern.search(li):
                if '<span' in title_pattern.search(li).group(1):
                    title = re.sub(r'<span.*?>','',title_pattern.search(li).group(1))
                    title = re.sub(r'</span>','',title)
                else:
                    title = title_pattern.search(li).group(1)
            else:
                title = ''

            ## 回复
            replay_pattern = re.compile(r'<div class="col2_left j_threadlist_li_left">.*?<span.*?>(.*?)</span>',re.S)
            replay = replay_pattern.search(li).group(1)
            # 作者
            author_pattern = re.compile(r'<span class="tb_icon_author ".*?title="(.*?)"',re.S)
            if author_pattern.search(li):
                author = author_pattern.search(li).group(1)[5:]
            else:
                author = ''
            content_pattern = re.compile(r'<div class="threadlist_abs threadlist_abs_onlyline ">(.*?)</div>',re.S)
            content_str = content_pattern.search(li)
            if content_str:
                if 'span' in content_str.group(1).strip(' \n'):
                    content = re.sub(r'<span.*?">','',content_str.group(1).strip(' \n'))
                elif '</span>' in content_str.group(1):
                    content = re.sub(r'</span>','',content_str.group(1).strip(' \n'))
                else:
                    content = content_str.group(1).strip(' \n')
            else:
                content = ''
            item['title'] = title
            item['replay'] = replay
            item['author'] = author
            item['content'] = content
            self.result.append(item)
        self.save_to_json(self.result)

    def save_to_json(self,result):
        with open('tieba.json','w',encoding='utf-8') as fp:
            json.dump(result,fp)

if __name__ == '__main__':
    kw = '易烊千玺'
    result = []
    base_url = 'http://tieba.baidu.com/f?kw={}&pn={}'
    for i in range(1,21):
        print('开始爬取第%i页'%i)
        url = base_url.format(kw,str((i-1)*50))
        tieba = TieBa(url,result)
        tieba.get_html()

