import requests
from lxml import etree
import os,re
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import threading
from queue import Queue

class Novel(threading.Thread):
    def __init__(self,url=None,q=None):
        super().__init__()
        self.url = url
        self.q = q
        self.driver = webdriver.PhantomJS()
        self.wait = WebDriverWait(self.driver,10)


    def run(self):
        self.parse_chapter_url()

    def get_html_by_requests(self,url):
        headers = {
            'Referer': 'http://www.xbiquge.la/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        response = requests.get(url=url,headers=headers)
        html = response.content.decode('utf-8')
        return html

    def get_html_by_selenium(self,url):
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[@id="content"]')))
        html = self.driver.page_source
        return html

    def get_text(self,text):
        if text:
            return text[0]
        else:
            return ''
    ### 保存成txt
    def save_to_txt(self,result,title):
        dirname = './novel'
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        filepath = dirname+'/'+title+'.txt'
        with open (filepath,'w',encoding='utf-8') as fp:
            fp.write(result)

    ## 获取小说内容
    def parse_novel_content(self,url,item,chapter,title):
        html = self.get_html_by_selenium(url)
        xpath_data = etree.HTML(html)
        content = ''.join(xpath_data.xpath('//div[@id="content"]/text()'))
        content = re.sub(r'\s','',content)
        item[chapter] = content
        self.save_to_txt(str(item),title)



    ## 获取章节的url
    def parse_chapter_url(self):

        while True:
            if self.q.empty():
                break
            novel_url = self.q.get()[0]
            title = self.q.get()[1]
            item = self.q.get()[2]
            html = self.get_html_by_requests(novel_url)
            xpath_data = etree.HTML(html)
            dd_list = xpath_data.xpath('//div[@id="list"]/dl/dd')
            for dd in dd_list:
                chapter = self.get_text(dd.xpath('./a/text()'))
                chapter_url = 'http://www.xbiquge.la' + self.get_text(dd.xpath('./a/@href'))
                print(chapter)
                self.parse_novel_content(chapter_url,item,chapter,title)

    ### 获取小说的url
    def parse_novel_url(self):
        info_list = []
        max_page = self.main()
        for i in range(1,int(max_page)+1):
            url = 'http://www.xbiquge.la/fenlei/1_{}.html'.format(i)
            html = self.get_html_by_requests(url)
            xpath_data = etree.HTML(html)
            li_list = xpath_data.xpath('//div[@id="newscontent"]/div[@class="l"]/ul/li')
            for li in li_list:
                item = {}
                title = ''.join(li.xpath('./span[@class="s2"]//text()'))
                novel_url = self.get_text(li.xpath('./span[@class="s2"]/a/@href'))
                # item['title'] = title
                # self.parse_chapter_url(novel_url,item,title)
                info_list.append((novel_url,title,item))
            return info_list



    def main(self):
        html = self.get_html_by_requests(self.url)
        xpath_data = etree.HTML(html)
        ## 获取最大页
        max_page = self.get_text(xpath_data.xpath('//div[@id="pagelink"]/a[@class="last"]/text()'))
        # for i in range(1,int(max_page)+1):
        #     url = 'http://www.xbiquge.la/fenlei/1_{}.html'.format(i)
        #     self.parse_novel_url(url)
        #     break
        return max_page


if __name__ == '__main__':
    ### 定义一个列表，用于接收小说url
    # info_list = []
    base_url = 'http://www.xbiquge.la/xuanhuanxiaoshuo/'
    q = Queue()
    novel = Novel(url=base_url)
    infos = novel.parse_novel_url()
    # print(infos)
    for info in infos:
        q.put(info)

    crawl_list = ['A','B','C','D']
    for crawl in crawl_list:
        t = Novel(q=q)
        t.start()