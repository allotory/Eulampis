# -*- coding: utf-8 -*-

import base64
import requests
import time
import json

def login(username, password):
    su = base64.b64encode(username.encode('utf-8')).decode('utf-8')

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,id;q=0.4,ja;q=0.2,ru;q=0.2,zh-TW;q=0.2,fr;q=0.2,es;q=0.2,de;q=0.2,pt;q=0.2',
        'Connection': 'keep-alive',
        'Content-Length': '215',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'login.sina.com.cn',
        'Origin': 'http://login.sina.com.cn',
        'Referer': 'http://login.sina.com.cn/signup/signin.php?entry=sso',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
    }
    
    data = {
        'entry': 'sso',
        'gateway': '1',
        'from': 'null',
        'savestate': '30',
        'useticket': '0',
        'pagerefer': '',
        'vsnf': '1',
        'su': su,
        'service': 'sso',
        'sp': password,
        'sr': '1680*1050',
        'encoding': 'UTF-8',
        'cdult': '3',
        'domain': 'sina.com.cn',
        'prelt': '0',
        'returntype': 'TEXT'
    }

    unix_time = str(int(time.time() * 1000))
    
    login_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)&_=' + unix_time

    session = requests.Session()
    resp = session.post(login_url, data=data, headers=headers)
    json_str = resp.content.decode('unicode_escape')
    # print(json_str)

    info = json.loads(json_str)
    if info['retcode'] == '0':
        print('login success.')

        cookies = session.cookies.get_dict()
        cookies = [key + "=" + value for key, value in cookies.items()]
        cookies = "; ".join(cookies)
        # print(cookies)
        session.headers["cookie"] = cookies
    else:
        print('login failure.')
        print('reason:', info['reason'])

    return session


def get_code(session):
    
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,id;q=0.4,ja;q=0.2,ru;q=0.2,zh-TW;q=0.2,fr;q=0.2,es;q=0.2,de;q=0.2,pt;q=0.2',
        'Connection':'keep-alive',
        'Host':'api.weibo.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }

    request_url = 'https://api.weibo.com/oauth2/authorize?redirect_uri=https%3A//api.weibo.com/oauth2/default.html&client_id=2622959781&response_type=code&display=default'

    resp = session.post(request_url, headers=headers)
    return resp.url

if __name__ == '__main__':
    session = login('bauble@sina.cn', 'saseverus1258740')
    code = get_code(session)
    print(code)   
    print(code[-32:])