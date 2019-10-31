import requests
import re
import json
class MaoYan():
    def __init__(self,url,result):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        self.result = result

    def get_html(self):
        try:
            response = requests.get(url=self.url,headers = self.headers)
            response.raise_for_status()
            html = response.content.decode('utf-8')
            return html
        except:
            return False

    def parse_html(self,html):
        dl_pattern = re.compile(r'<dl class="board-wrapper">(.*?)</dl>',re.S)
        dl_content = dl_pattern.findall(html)
        dd_pattern = re.compile(r'<dd>(.*?)</dd>',re.S)
        dds = dd_pattern.findall(dl_content[0])
        for dd in dds:
            movie_dict = {}
            ## 电影名
            pattern_title = re.compile(r'<p class="name">.*?<a.*?>(.*?)</a></p>',re.S)
            title = pattern_title.search(dd).group(1)

            ## 主演
            pattern_star = re.compile(r'<p class="star">(.*?)</p>',re.S)
            star = pattern_star.search(dd).group(1).strip('\n ')[3:]

            ## 上映时间
            pattern_time = re.compile(r'<p class="releasetime">(.*?)</p>',re.S)
            releasetime1 = pattern_time.search(dd).group(1)[5:]
            pattern_time2 = re.compile(r'\d{4}-?\d*-?\d*',re.S)
            releasetime = pattern_time2.search(releasetime1).group()

            ## 评分
            pattern_score1 = re.compile(r'<p class="score">.*?<i class="integer">(.*?)</i>.*?</p>',re.S)
            pattern_score2 = re.compile(r'<p class="score">.*?<i class="fraction">(.*?)</i>.*?</p>',re.S)
            score = pattern_score1.search(dd).group(1)+pattern_score2.search(dd).group(1)
            movie_dict['title'] = title
            movie_dict['star'] = star
            movie_dict['releasetime'] = releasetime
            movie_dict['score'] = score
            self.result.append(movie_dict)
        return self.result


    def save_to_json(self):
        with open('maoyan_movie.json','w',encoding='utf-8') as fp:
            json.dump(self.result,fp)



if __name__ == '__main__':
    base_url = 'https://maoyan.com/board/4'
    result = []
    for i in range(1,11):
        offset = str((i-1)*10)
        url = base_url + '?offset=' + offset
        maoyan = MaoYan(url,result)
        html = maoyan.get_html()
        result = maoyan.parse_html(html)
        maoyan.save_to_json()
