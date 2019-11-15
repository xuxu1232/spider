import random

import requests
import time
from lxml import etree
import pymongo,hashlib

class YaMaXun(object):
    def __init__(self,url):
        self.url = url
        self.client = pymongo.MongoClient()
        self.db = self.client['yamaxun']

    def get_html(self,url):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'x-wl-uid=1QLe2gqPSztp7q/d35JtFah53bbd0L/jcm1jpzpbAGsO7NmT/HOL3UkmtZ51z2fEfGXNNIvpPTsw=; session-id=457-9096237-1233543; ubid-acbcn=460-9522675-4799024; lc-acbcn=zh_CN; session-id-time=2082729601l; session-token=jTviM6XcWcVE66dn+9mjZEE1AxxXieo56bUs4m5ruuKdckiog8j4B5qW9mfq0ERCZXXUM+T0hMXsWtgM/rVex9BP/WeXv4jhzZ9kpC+XpuxHkXUA0igI8Hq2ggQI/OF7iCK8zOq17IEw5EVyGm8UFChJp4sLqneKsBblmi37n5MB60KruPa1Z03gYMpD+p2CgnGUgBotd8JRCgzST5+ZDFz5QOBrmLUrp3MZ92e0H9ylr/MJDOuEpw==; floatingBannerOnGateway=floatingBannerOnGateway; csm-hit=tb:Z8QFC48Z5K2TSGFP53DR+s-Z8QFC48Z5K2TSGFP53DR|1573782246208&t:1573782246208',
            'Host': 'www.amazon.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        response = requests.get(url=url,headers=headers)
        html = response.content.decode('utf-8')
        return html

    def get_text(self,text):
        if text:
            return text[0]
        else:
            return ''

    def get_max_page(self,url):
        try:
            html = self.get_html(url)
        except Exception as e:
            return e
        xpath_data = etree.HTML(html)
        max_page = self.get_text(xpath_data.xpath('//div[@id="pagn"]/span[@class="pagnDisabled"]/text()'))
        return max_page

    def get_md5(self,value):
        md5 = hashlib.md5()
        md5.update(value.encode())
        return md5.hexdigest()
    def save_to_mongo(self,item):
        hash_url = self.get_md5(item['detail_url'])
        item['hash_url'] = hash_url
        self.db['yamaxun:goods'].update({'hash_url':item['hash_url']},{'$set':item},True)

    def parse_detail_url(self,url,total_title):

        max_page = self.get_max_page(url)
        for i in range(1,int(max_page)+1):
            url_ = 'https://www.amazon.cn/s?rh=n%3A2016156051%2Cn%3A%212016157051%2Cn%3A2152154051&page={}&qid=1573823345&ref=lp_2152154051_pg_{}'.format(i, i)
            try:
                time.sleep(random.randint(1, 2))
                html = self.get_html(url_)
            except Exception as e:
                return e
            if i == 1:
                xpath_data = etree.HTML(html)
                li_list = xpath_data.xpath('//div[@id="mainResults"]/ul/li')
                for li in li_list:
                    item = {}
                    detail_url = self.get_text(li.xpath('.//div[@class="a-row a-spacing-none"]/div[1]/a/@href'))
                    title = self.get_text(li.xpath('.//div[@class="a-row a-spacing-none"]/div[1]/a/h2/text()'))
                    price = self.get_text(li.xpath('.//div[@class="a-row a-spacing-none"]/div[2]/a/span[2]/text()'))
                    score = self.get_text(li.xpath('.//div[@class="a-row a-spacing-none"]/div[@class="a-row a-spacing-top-mini a-spacing-none"]//a/i/span/text()'))
                    comment_num = self.get_text(li.xpath('.//div[@class="a-row a-spacing-none"]/div[3]/a/text()'))
                    item['detail_url'] = detail_url
                    item['title'] = title
                    item['price'] = price
                    item['score'] = score
                    item['comment_num'] = comment_num
                    item['total_title'] = total_title
                    self.save_to_mongo(item)
            else:
                xpath_data = etree.HTML(html)
                div_list = xpath_data.xpath('//div[@class="s-result-list s-search-results sg-row"]/div')
                for div in div_list:
                    item = {}
                    detail_url = 'https://www.amazon.cn'+self.get_text(div.xpath('.//div[@class="a-section a-spacing-medium"]/div[2]/div[3]//h2/a/@href'))
                    title = self.get_text(div.xpath('.//div[@class="a-section a-spacing-medium"]/div[2]/div[3]//h2/a/span/text()'))
                    price = self.get_text(div.xpath('.//div[@class="a-section a-spacing-medium"]/div[2]/div[4]//a/span/span[1]/span/text()'))+'-'+self.get_text(div.xpath('.//div[@class="a-section a-spacing-medium"]/div[2]/div[4]//a/span/span[3]/span/text()'))
                    score = self.get_text(div.xpath('.//div[@class="a-section a-spacing-medium"]/div[2]/div[3]/div/div[2]//i//text()'))
                    comment_num = self.get_text(div.xpath('.//div[@class="a-section a-spacing-medium"]/div[2]/div[3]/div/div[2]/div/span[2]//span/text()'))
                    item['detail_url'] = detail_url
                    item['title'] = title
                    item['price'] = price
                    item['score'] = score
                    item['comment_num'] = comment_num
                    item['total_title'] = total_title
                    self.save_to_mongo(item)




    def parse_index(self):
        html = self.get_html(self.url)
        xpath_data = etree.HTML(html)
        li_list = xpath_data.xpath('//div[@id="siteDirectory"]/div/div[position()>2]/div[2]/div//div[@class="a-row"]/ul/li')
        for li in li_list:
            type_url = 'https://www.amazon.cn' + self.get_text(li.xpath('.//a/@href'))
            title = self.get_text(li.xpath('.//a/text()'))
            self.parse_detail_url(type_url,title)

if __name__ == '__main__':
    base_url = 'https://www.amazon.cn/gp/site-directory?ie=UTF8&ref_=nav_deepshopall_variant_fullstore_l1'
    yamaxun = YaMaXun(base_url)
    yamaxun.parse_index()
