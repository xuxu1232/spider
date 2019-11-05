import requests
from lxml import etree
import json

class WangYiYun(object):
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'cookie': '_ntes_nnid=bde7c65abd5e06bbf64efe60691ef247,1566111466592; _ntes_nuid=bde7c65abd5e06bbf64efe60691ef247; __oc_uuid=7c038f50-c185-11e9-86f9-4bd3dd23d629; _iuqxldmzr_=32; WM_TID=cN5fXBJlrPpFQBFRFUM5pc68R2vwXqaF; UM_distinctid=16d9b2096ba1f6-0c3fa044fca013-3f385804-15f900-16d9b2096bb321; P_INFO=lovekk0502@163.com|1570539822|0|163|00&99|bej&1570265765&unireg#bej&null#10#0#0|&0|unireg|lovekk0502@163.com; mail_psc_fingerprint=db28de61b0efc44e30fad7491c2519e4; __root_domain_v=.163.com; _qddaz=QD.887vbv.pz0uqc.k1ut3v9f; hb_MA-BFF5-63705950A31C_source=www.baidu.com; JSESSIONID-WYYY=nCM3UFRCHU%2BN29I40JCdWqeUoK9ODAMvhatJvu55zI3N5TkvtqadSbtPdyhfp9%5C3%2BGu3evqCf6R%5ClFUng2S3yPCh92RD6%2FWvhk2AE6GsIoF%2By8m%5CV%5C%5CPIzx31iRMqK9pp%2B2dvcaNfTK5PmfV9kxB94U%5Cmt6k7MR%5C8bc%2BAS50YMZ6ijBN%3A1572501969558; WM_NI=t0uRHExyLcdgXOVHlLxRzq%2F3shycmWJQ15HvrwOf%2FvY%2F78m60wcmaPJFIVETBrWPHkprlp0M%2B53OC9cPIhhiyAFqmCWHOwIxdr9v3%2FltLFblCA1sqZCopftQL4zBBC3TUWw%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeaddc67f79e8a97e55daab08ea6c54e969f9baeb87f86b88fbbce7cad9f81a3d22af0fea7c3b92ab8f0bbb3cb4fbca78484e76d9c919aa9ef48bc8eb692ae39b1b8b784f05d8a8fffd6cb7eb2a98187ae7e9bf1f9d9f03ef4a9ad8ee45c8a9a87b7c86082ae99b1cb61b4aea491b347e9ebfdb0c233a1908789eb63bb9f8a92f04995988198cc74a8aef797b225b0ac84a7e168819fff94f45281b1c087f75b90ecb6a3c149f18c9bb8f637e2a3',
            'upgrade-insecure-requests': '1'

        }
    def get_html(self,url):
        response = requests.get(url=url,headers=self.headers)
        html = response.content.decode('utf-8')
        xpath_html = etree.HTML(html)
        return xpath_html

    ## 进入歌手主页，获取歌手详细信息
    def parse_detail(self,url,item):
        html = self.get_html(url)
        description = html.xpath('//div[@class="n-artdesc"]/p/text()')
        item['description'] = ''.join(description).replace('\n','')
        self.save_to_json(item)


    ## 解析每个歌手的姓名和url
    def parse_singer(self,url):
        item = {}
        html = self.get_html(url)
        singer_name = html.xpath('//ul[@id="m-artist-box"]/li/p/a[1]/text()')
        singer_url = html.xpath('//ul[@id="m-artist-box"]/li/p/a[1]/@href|//ul[@id="m-artist-box"]/li/a[1]/@href')
        singer_url = [x.strip() for x in singer_url]
        for index,name in enumerate(singer_name):
            item['singer_name'] = name
            new_url = 'https://music.163.com' + singer_url[index]
            item['singer_url'] = new_url
            ## 艺人介绍的url
            url = 'https://music.163.com' + singer_url[index].split('?')[0]+'/desc?'+singer_url[index].split('?')[1]
            self.parse_detail(url,item)
            # print(url)



    ## 抓取按字母分类的url
    def parse_zimu(self,url):
        html = self.get_html(url)
        zimu_url = html.xpath('//ul[@id="initial-selector"]/li/a/@href')
        for one_url in zimu_url:
            new_url = 'https://music.163.com' + one_url
            self.parse_singer(new_url)


    ### 获取首页的内容，抓取地区分类的url
    def parse_index(self,url):
        html = self.get_html(url)
        area_url = html.xpath('//div[@class="blk"]/ul/li/a/@href')
        for one_url in area_url:
            new_url = 'https://music.163.com' + one_url
            self.parse_zimu(new_url)


    def save_to_json(result):
        with open('singer.json','w',encoding='utf-8') as fp:
            json.dump(result,fp)
if __name__ == '__main__':
    base_url = 'https://music.163.com/discover/artist'
    wangyiyun = WangYiYun()
    wangyiyun.parse_index(base_url)