import hashlib
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
import requests
import re

def hex_md5(str):
    """
    js 代码里面的hex_md5 python实现
    """ 
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    return md5.hexdigest()

def encrypt(password, public_key):
    """
    jsencrypt 里面的encrypt的python实现
    """
    rsakey = RSA.importKey(public_key)
    cipher = Cipher_pksc1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
    return cipher_text.decode()

def quotation(code):
    """
    新浪财经实时行情
    http://hq.sinajs.cn/list=sz128128
    """
    ret = requests.get("http://hq.sinajs.cn/list=" + code)
    print(ret.text)
    hq = re.search('"(.*?)"',ret.text)
    l = hq.group(1).split(',')
    data = {
        'name': l[0],
        'today_open':l[1],
        'yest_close':l[2],
        'price':l[3],
        'high':l[4],
        'low':l[5],
        'bid1':l[11],
        'bid2':l[13],
        'bid3':l[15],
        'bid4':l[17],
        'bid5':l[19],
        'ask1':l[21],
        'ask2':l[23],
        'ask3':l[25],
        'ask4':l[27],
        'ask5':l[29],
        'date':l[30],
        'time':l[31],
    }
    return data

def get_market(code):
    """
    获取市场 sz  sh
    """
    code = str(code)
    if code[0:2] == '11':
        return 'sh' 
    elif code[0:2] == '12':
        return 'sz'
    elif code[0] in ['0','3']:
        return 'sz'
    elif code[0] == '6':
        return 'sh'
    else:
        return False

def drop_sell(quotation, price, drop):
    """
    回落卖出信号
    价格高于price, 回落drop(百分比)
    """
    high = quotation['high']
    cur_price = quotation['price']
    return price <= cur_price and drop >= (high - cur_price) / high

if __name__ == "__main__":
    s = "egshi%2BR436c3MebgIRb3tGm2C4wGbRfs0IWdmP7vR%2Bz2aSa1LOFq7lYshSBSYZ96Pe4Hup8WPn3yNb9DOM7Q%2Bg%3D%3D"
    print(hex_md5(s))
    quot = quotation('sz128128') 
    print(quot)

