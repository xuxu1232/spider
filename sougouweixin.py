import requests
from lxml import etree
import hashlib
import pymongo

class SouGouWX(object):
    def __init__(self,url):
        self.url = url
        self.client = pymongo.MongoClient()
        self.db = self.client['sougouweixin']

    def get_ajax_data(self,url):
        headers = {
            'Referer': 'https://weixin.sogou.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        try:
            response = requests.get(url,headers=headers)
            html = response.content.decode('utf-8')
            return html
        except Exception as e:
            return e

    def get_text(self,text):
        if text:
            return text[0]
        else:
            return ''

    def get_md5(self,value):
        md5 = hashlib.md5()
        md5.update(value.encode())
        return md5.hexdigest()

    def save_to_mongo(self,item):
        hash_url = self.get_md5(item['detail_url'])
        item['hash_url'] = hash_url
        self.db['article'].update({'hash_url':item['hash_url']},{'$set':item},True)


    def parse_html(self):
        for i in range(1,5):
            url = self.url.format(i)
            print(url)
            html = self.get_ajax_data(url)
            xpath_data = etree.HTML(html)
            li_list = xpath_data.xpath('//li')
            for li in li_list:
                item = {}
                title = self.get_text(li.xpath('./div[@class="txt-box"]/h3/a/text()'))
                detail_url =self.get_text(li.xpath('./div[@class="txt-box"]/h3/a/@href'))
                desc = self.get_text(li.xpath('./div[@class="txt-box"]/p/text()'))
                date = self.get_text(li.xpath('./div[@class="txt-box"]/div/span/text()'))
                publisher = self.get_text(li.xpath('./div[@class="txt-box"]/div/a/text()'))
                item['title'] = title
                item['detail_url'] = detail_url
                item['desc'] = desc
                item['date'] = date
                item['publisher'] = publisher
                self.save_to_mongo(item)
                print(item)


if __name__ == '__main__':
    base_url = 'https://weixin.sogou.com/pcindex/pc/pc_0/{}.html'
    s = SouGouWX(base_url)
    s.parse_html()



'https://mp.weixin.qq.com/s?src=11&timestamp=1574085601&ver=1982&signature=Q0RhOq4G7WCgLMDSpeB7e*zER8BsaiyOwCjOfnsoRW89YW*QuzkAIMDqO2QurNsOg84iGrC2LjlbvGxy3pXPUbbSPT1ULAqmCYwC3Bs3kCtw3GPLNpyMD*r7DRLvBuYN&new=1'