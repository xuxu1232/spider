import requests
from lxml import etree

def get_html(base_url):

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    try:
        response = requests.get(base_url,headers = headers)
        response.raise_for_status()
        html = response.content.decode('utf-8')
        return html
    except:
        return False

def parse_html(html):
    xpath_html = etree.HTML(html)
    divs = xpath_html.xpath('//div[@id="content"]/div[contains(@class,"con")]')
    product_list = []
    for div in divs:
        product_dict = {}
        name = div.xpath('./div[2]/a/text()')[0]
        description = div.xpath('./div[2]/span/text()')[0]
        product_dict['name'] = name
        product_dict['description'] = description
        product_list.append(product_dict)
    return product_list



# response = response.content.decode('utf-8')
# response.encoding = 'utf-8'
# print(response.status_code) ## 响应状态码
# print(response.headers)  ## 响应头
# print(type(response.text))   ## 字符串格式
# print(type(response.content))  ## 二进制格式

if __name__ == '__main__':
    base_url = 'https://www.baidu.com/more/'
    html = get_html(base_url)
    result = parse_html(html)
    print(result)



## 写入文件
# with open('baidu_product.html','w',encoding='utf-8') as fp:
#     fp.write(response)