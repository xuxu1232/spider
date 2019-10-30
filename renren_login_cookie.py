import requests

base_url = 'http://www.renren.com/972694403/profile'  ## 你想要访问的网页的url

headers = {
    "Cookie": "_uuid=A276AEDB-A085-3845-B740-9DF4B7CD932162161infoc; buvid3=4CB45669-DC58-4902-BE2D-ADD7756EB146190954infoc; LIVE_BUVID=AUTO5315654020787669; CURRENT_FNVAL=16; stardustvideo=1; rpdid=|(k|~uYmR)ku0J'ulYlR|kmJJ; UM_distinctid=16d1b50c015756-0180b3643c4fd5-3f385804-15f900-16d1b50c0169cc; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1568121364; sid=ac58b8fy; DedeUserID=381101265; DedeUserID__ckMd5=c71cf071756110f3; SESSDATA=9609952b%2C1573389457%2Ca1cd93a1; bili_jct=eccf38a2c7c31679f10550ff9103c1ef; bp_t_offset_381101265=310126484504484032; CNZZDATA2724999=cnzz_eid%3D981707917-1568116571-https%253A%252F%252Fwww.bilibili.com%252F%26ntime%3D1572310860",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}


response = requests.get(url=base_url,headers=headers)
if '46506937625_bili' in response.text:
    print('登陆成功')
else:
    print('登陆失败')

# print(response.content.decode('utf-8'))