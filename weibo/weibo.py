#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.04'
__author__ = 'Liao Xuefeng (askxuefeng@gmail.com)'
__publish__ = 'http://www.cnblogs.com/txw1958/'

'''
Python3 client SDK for sina weibo API using OAuth 2.
'''

try:
    import json
except ImportError:
    import simplejson as json
import time
import urllib.request
import logging


import base64
import requests
import mysql.connector


def _obj_hook(pairs):
    '''
    convert json object to python object.
    '''
    o = JsonObject()
    for k, v in pairs.items():
        o[str(k)] = v
    return o

class APIError(Exception):
    '''
    raise APIError if got failed json message.
    '''
    def __init__(self, error_code, error, request):
        self.error_code = error_code
        self.error = error
        self.request = request
        Exception.__init__(self, error)

    def __str__(self):
        return 'APIError: %s: %s, request: %s' % (self.error_code, self.error, self.request)

class JsonObject(dict):
    '''
    general json object that can bind any fields but also act as a dict.
    '''
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

def _encode_params(**kw):
    '''
    Encode parameters.
    '''
    args = []
    for k, v in kw.items():
        qv = v.encode('utf-8') if isinstance(v, str) else str(v)
        args.append('%s=%s' % (k, urllib.parse.quote(qv)))
    return '&'.join(args)

def _encode_multipart(**kw):
    '''
    Build a multipart/form-data body with generated random boundary.
    '''
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    for k, v in kw.items():
        data.append('--%s' % boundary)
        if hasattr(v, 'read'):
            filename = getattr(v, 'name', '')
            n = filename.rfind('.')
            ext = filename[n:].lower() if n != (-1) else ""
            content = v.read()
            content = content.decode('ISO-8859-1')
            data.append('Content-Disposition: form-data; name="%s"; filename="hidden"' % k)
            data.append('Content-Length: %d' % len(content))
            data.append('Content-Type: %s\r\n' % _guess_content_type(ext))
            data.append(content)
        else:
            data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
            data.append(v if isinstance(v, str) else v.decode('utf-8'))
    data.append('--%s--\r\n' % boundary)
    return '\r\n'.join(data), boundary

_CONTENT_TYPES = { '.png': 'image/png', '.gif': 'image/gif', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.jpe': 'image/jpeg' }

def _guess_content_type(ext):
    return _CONTENT_TYPES.get(ext, 'application/octet-stream')

_HTTP_GET = 0
_HTTP_POST = 1
_HTTP_UPLOAD = 2

def _http_get(url, authorization=None, **kw):
    logging.info('GET %s' % url)
    return _http_call(url, _HTTP_GET, authorization, **kw)

def _http_post(url, authorization=None, **kw):
    logging.info('POST %s' % url)
    return _http_call(url, _HTTP_POST, authorization, **kw)

def _http_upload(url, authorization=None, **kw):
    logging.info('MULTIPART POST %s' % url)
    return _http_call(url, _HTTP_UPLOAD, authorization, **kw)

def _http_call(url, method, authorization, **kw):
    '''
    send an http request and expect to return a json object if no error.
    '''
    params = None
    boundary = None
    if method==_HTTP_UPLOAD:
        params, boundary = _encode_multipart(**kw)
    else:
        params = _encode_params(**kw)
    http_url = '%s?%s' % (url, params) if method==_HTTP_GET else url
    http_body = None if method==_HTTP_GET else params.encode(encoding='utf-8')
    req = urllib.request.Request(http_url, data=http_body)
    if authorization:
        req.add_header('Authorization', 'OAuth2 %s' % authorization)
    if boundary:
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    resp = urllib.request.urlopen(req)
    body = resp.read().decode("utf-8")
    r = json.loads(body, object_hook=_obj_hook)
    if 'error_code' in r:
        raise APIError(r.error_code, r['error_code'], r['request'])
    return r

class HttpObject(object):

    def __init__(self, client, method):
        self.client = client
        self.method = method

    def __getattr__(self, attr):
        def wrap(**kw):
            if self.client.is_expires():
                raise APIError('21327', 'expired_token', attr)
            return _http_call('%s%s.json' % (self.client.api_url, attr.replace('__', '/')), self.method, self.client.access_token, **kw)
        return wrap

class APIClient(object):
    '''
    API client using synchronized invocation.
    '''
    def __init__(self, app_key, app_secret, redirect_uri=None, response_type='code', domain='api.weibo.com', version='2'):
        self.client_id = app_key
        self.client_secret = app_secret
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.auth_url = 'https://%s/oauth2/' % domain
        self.api_url = 'https://%s/%s/' % (domain, version)
        self.access_token = None
        self.expires = 0.0
        self.get = HttpObject(self, _HTTP_GET)
        self.post = HttpObject(self, _HTTP_POST)
        self.upload = HttpObject(self, _HTTP_UPLOAD)

    def set_access_token(self, access_token, expires_in):
        self.access_token = str(access_token)
        self.expires = float(expires_in)

    def get_authorize_url(self, redirect_uri=None, display='default'):
        '''
        return the authroize url that should be redirect.
        '''
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        if not redirect:
            raise APIError('21305', 'Parameter absent: redirect_uri', 'OAuth2 request')
        return '%s%s?%s' % (self.auth_url, 'authorize', \
                _encode_params(client_id = self.client_id, \
                        response_type = 'code', \
                        display = display, \
                        redirect_uri = redirect))

    def request_access_token(self, code, redirect_uri=None):
        '''
        return access token as object: {"access_token":"your-access-token","expires_in":12345678}, expires_in is standard unix-epoch-time
        '''
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        if not redirect:
            raise APIError('21305', 'Parameter absent: redirect_uri', 'OAuth2 request')

        r = _http_post('%s%s' % (self.auth_url, 'access_token'), \
                client_id = self.client_id, \
                client_secret = self.client_secret, \
                redirect_uri = redirect, \
                code = code, grant_type = 'authorization_code')

        r.expires_in += int(time.time())
        return r

    def is_expires(self):
        return not self.access_token or time.time() > self.expires

    def __getattr__(self, attr):
        return getattr(self.get, attr)


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


def get_code(session, request_url):
    
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,id;q=0.4,ja;q=0.2,ru;q=0.2,zh-TW;q=0.2,fr;q=0.2,es;q=0.2,de;q=0.2,pt;q=0.2',
        'Connection':'keep-alive',
        'Host':'api.weibo.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }

    # request_url = 'https://api.weibo.com/oauth2/authorize?redirect_uri=https%3A//api.weibo.com/oauth2/default.html&client_id=2622959781&response_type=code&display=default'

    resp = session.post(request_url, headers=headers)
    return resp.url

def get_data(id):
    conn = mysql.connector.connect(user='root', passwd='root', db='eulampis')

    cursor = conn.cursor()
    cursor.execute('select wb_index from weibo_index where id=1')
    index = cursor.fetchall()
    print(index[0][0])

    cursor = conn.cursor()
    cursor.execute('select * from weibo where id=' + str(index[0][0]))
    values = cursor.fetchall()

    cursor = conn.cursor()
    cursor.execute('update weibo_index set wb_index=' + str(index[0][0] + 1))

    cursor.close()
    conn.commit()
    conn.close()

    return values


def main():
    try:
        # step 1 定义 app key，app secret，回调地址：
        APP_KEY = "2622959781"
        APP_SECRET = "b50cefdc8052c9841436f1abc3737a01"
        CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
        # step 2 引导用户到授权地址
        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
        print(client.get_authorize_url())

        session = login('bauble@sina.cn', 'saseverus1258740')
        code = get_code(session, client.get_authorize_url())[-32:]

        # step 3 换取Access Token
        # r = client.request_access_token(input("Input code:"))#输入授权地址中获得的CODE
        r = client.request_access_token(code)#输入授权地址中获得的CODE
        client.set_access_token(r.access_token, r.expires_in)
        print('====' + str(r.expires_in))

        # step 4 使用获得的OAuth2.0 Access Token调用API
        print(client.get.account__get_uid())
        print(client.post.statuses__update(status='测试Python3 + OAuth 2.0发微博 '+ str(time.time())))
        # print(client.post.statuses__update(status='测试Python3 + OAuth 2.0发微博 '+ get_data()[0][1] + str(time.time())))
        # print(client.upload.statuses__upload(status='测试Python3 OAuth 2.0带图片发微博 ' + str(time.time()), pic=open('test.png', 'rb')))

    except Exception as pyOauth2Error:
        print(pyOauth2Error)

if __name__ == '__main__':
    main()