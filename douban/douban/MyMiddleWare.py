import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse
## 自定义下载中间件,用于获取网页的内容
## 下载中间件是一个类，必须实现process_request(self,request,spider)方法

class MyMiddlewares(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.wait = WebDriverWait(self.driver,10)

    #### 获取网页内容，返回一个HtmlResponse对象
        ### 参数：url：请求的url,body:从网页获取的页面，request,encoding
    def process_request(self, request, spider):
        # print(request.url)
        xpath = request.meta.get('xpath')
        self.driver.get(request.url)
        if xpath:
            self.wait.until(EC.presence_of_element_located((By.XPATH,xpath)))
        else:
            time.sleep(3)
        html = self.driver.page_source
        return HtmlResponse(url=request.url,body=html,encoding='utf-8',request=request)
