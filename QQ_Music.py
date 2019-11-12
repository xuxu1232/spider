import requests
import json
from multiprocessing import Pool
import os

class QQMusic(object):
    def __init__(self):
        self.disstid_headers = {
            'Origin': 'https://y.qq.com',
            'Referer': 'https://y.qq.com/portal/playlist.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

        self.songmid_headers = {
            'Referer': 'https://y.qq.com/n/yqq/playlist/7290437289.html',
		    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

        self.vkey_headers = {
            'Referer': 'https://y.qq.com/portal/player.html',
		    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

        self.music_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def save_music(self,purl,name):
        response = requests.get(url=purl,headers=self.music_headers)
        filepath = './music'
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        with open (filepath+'/'+name+'.m4a','wb') as fp:
            fp.write(response.content)
        print('下载结束',name)


    def parse_vkey(self,song_list):
        songmid = song_list[1]
        base_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?'
        params = {
            '-': 'getplaysongvkey28720065500654557',
            'g_tk': '5381',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'notice': '0',
            'platform': 'yqq.json',
            'needNewCode': '0',
            'data': '{"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"6144036204","songmid":["%s"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}'%songmid
        }
        response = requests.get(url=base_url,headers=self.vkey_headers,params=params)
        datas = json.loads(response.text)
        purl = 'http://ws.stream.qqmusic.qq.com/' + datas['req_0']['data']['midurlinfo'][0]['purl']
        songname = song_list[0]
        # print(purl)
        print('开始下载',songname)
        self.save_music(purl,songname)


    def parse_songmid(self,disstid):
        song_list = []
        base_url = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?'
        params = {
            'type': '1',
            'json': '1',
            'utf8': '1',
            'onlysong': '0',
            'new_format': '1',
            'disstid': disstid,
            'g_tk': '5381',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'notice': '0',
            'platform': 'yqq.json',
            'needNewCode': '0',
        }
        response = requests.get(url=base_url,headers=self.songmid_headers,params=params)
        datas = json.loads(response.text)
        for data in datas['cdlist'][0]['songlist']:
            songmid = data['mid']
            songname = data['name']
            song_list.append((songname,songmid))
        p = Pool()
        p.map(self.parse_vkey,song_list)


    def parse_disstid(self):
        base_url = 'https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg?'
        params = {
            'picmid': '1',
            'rnd': '0.17960330810879066',
            'g_tk': '5381',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'notice': '0',
            'platform': 'yqq.json',
            'needNewCode': '0',
            'categoryId': '10000000',
            'sortId': '5',
            'sin': '0',
            'ein': '19',
        }
        response = requests.get(url=base_url,headers=self.disstid_headers,params=params)
        datas = json.loads(response.text)
        for data in datas['data']['list']:
            disstid = data['dissid']
            name = data['dissname']
            print('开始歌单',name)
            self.parse_songmid(disstid)



if __name__ == '__main__':
    music = QQMusic()
    music.parse_disstid()