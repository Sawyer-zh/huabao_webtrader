#! /usr/bin/env
# -*- coding:utf-8 -*-
import requests
from .util import hex_md5, encrypt
import json
import re
from urllib.parse import quote
from .log import Log

LOGIN_URL = 'https://m.touker.com/account/login/custNoLogin.do'


def get_params():
    """
    获取hbtoke 和 public key
    """
    ret = requests.get(
        "https://m.touker.com/account/login/index.htm?source=stock_trade_h5&referrer=https://m.touker.com/trading/trade/position#/")
    s = ret.text
    cookies = ret.cookies
    cookies_dict = requests.utils.dict_from_cookiejar(cookies)
    try:
        hbtoken = re.search('id="_hbtoken_" value="(.*?)"', s).group(1)
        key = re.search(r'encryptor.setPublicKey\("(.*?)"', s).group(1)
        public_key = '-----BEGIN PUBLIC KEY-----\n' + key + '\n-----END PUBLIC KEY-----'
        b = cookies_dict['_b_']
        return hbtoken, public_key, b
    except:
        Log.e("hbtoke,b,public_key等参数获取失败")
        return False


def login(user):
    """
    采用客户号和密码登录
    """
    hbtoken, public_key, b = get_params()
    plain = json.dumps({
        'md5': hex_md5(hbtoken),
        'loginId': user['custno'],
        'password': user['password']
    })
    encrypted = quote(encrypt(plain, public_key))
    login_params = {
        '_hbtoken_': hbtoken,
        'encrypted': encrypted,
        'appId': None,
        "deviceUUID": None,
        "imgCode": None,
    }
    login_ret = requests.post(
        LOGIN_URL, data=login_params, cookies={'_b_': b},
        headers={
            'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Mobile Safari/537.36"
        }
    )
    headers = login_ret.headers
    try:
        # 不用这个cookie 他把转义搞没了
        #login_cookies = requests.utils.dict_from_cookiejar(login_ret.cookies)
        if login_ret.json()['respCode'] == '000000':
            # 登录成功写入cookie文件
            cookies = headers['Set-Cookie']
            e = re.search('_e_=(.*?);', cookies).group()
            d = re.search('_d_=(.*?);', cookies).group()
            s = re.search('_s_=(.*?);', cookies).group()
            ssid = re.search('ssid=(.*?);', cookies).group()
            b = '_b_="' + b + '";'
            cookies_str = ' '.join([e, d, s, ssid, b])
            with open('cookies_' + user['custno'] + '.txt', 'w') as f:
                f.write(cookies_str)
        return True
    except:
        Log.e("--登录失败--")
        return False


if __name__ == "__main__":
    with open('config.json') as f:
        user = json.load(f)
