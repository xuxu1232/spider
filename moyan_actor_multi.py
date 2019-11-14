import hashlib
import redis
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import etree
from queue import Queue
import threading

class MaoYanActor(threading.Thread):
    def __init__(self,name,q):
        super().__init__()
        self.name = name
        self.q = q
        self.driver = webdriver.PhantomJS()
        self.wait = WebDriverWait(self.driver,20)

    def run(self):
        self.parse()

    def get_text(self,text):
        if text:
            return text[0]
        return ''

    ### 加密
    def get_md5(self,value):
        md5 = hashlib.md5()
        md5.update(value.encode())
        return md5.hexdigest()

    ## 对响应进行去重（针对页面是否更新，是否重复）
    ## 重复返回True
    def response_seen(self,text):
        hash_text = self.get_md5(text)
        red = redis.Redis()
        result = red.sadd('maoyan:text',hash_text)
        if result == 0:
            return True
        else:
            return False

    ## 对url进行去重，利用redis的集合进行url去重
    ## 重复返回True
    def request_seen(self,url):
        hash_url = self.get_md5(url)
        red = redis.Redis()
        ## 如果set里面有该url，就设置不进去，返回0，如果没有，就可以设置进去，返回0
        result = red.sadd('maoyan:actor_url',hash_url)
        if result == 0:
            return True
        else:
            return False


    def get_html_by_selenium(self,url,xpath):
        self.driver.get(url)
        webelement = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        webelement.click()
        html_str = self.driver.page_source
        if not self.response_seen(html_str):
            return html_str
        return None


    def parse(self):
        while True:
            if self.q.empty():
                break
            url = self.q.get()
            if self.request_seen(url):
                continue
            try:
                html = self.get_html_by_selenium(url,'//div[@class="introduce"]/div[2]/a')
                # print(html)
                xpath_html = etree.HTML(html)
                name = self.get_text(xpath_html.xpath('//dl[@class="dl-left"]/dd[1]/text()'))
                # print(name)
                print('{}============{}'.format(self.name,name))
                actor_url = xpath_html.xpath('//div[@class="item"]/div/a/@href')
                for u in actor_url:
                    self.q.put('https://maoyan.com'+u)
            except Exception:
                print('页面为空')

if __name__ == '__main__':
    q = Queue()
    # base_url = 'https://maoyan.com/films/celebrity/385315'
    start_urls = [
        'https://maoyan.com/films/celebrity/385315',
        'https://maoyan.com/films/celebrity/5928',
        'https://maoyan.com/films/celebrity/2924113'
    ]
    for url in start_urls:
        q.put(url)

    crawl_list = ['aa','bb','cc']
    for crawl in crawl_list:
        t = MaoYanActor(crawl,q)
        t.start()

