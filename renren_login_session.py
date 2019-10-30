import requests

## 登录页的url
login_url = 'http://www.renren.com/SysHome.do'
headers = {
    'Host': 'space.bilibili.com',
    'Referer': 'https://www.bilibili.com/',
}

### 登录需要的数据
data = {
    'email':'xxx',
    'password':'xxx'
}

session = requests.session()

## 登录
session.post(url=login_url,headers=headers,data=data)

### 登陆成功后获取个人中心页
personal_url = ''
response = session.get(url=personal_url,headers=headers)


