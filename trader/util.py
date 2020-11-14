import hashlib
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA

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

if __name__ == "__main__":
    s = "egshi%2BR436c3MebgIRb3tGm2C4wGbRfs0IWdmP7vR%2Bz2aSa1LOFq7lYshSBSYZ96Pe4Hup8WPn3yNb9DOM7Q%2Bg%3D%3D"
    print(hex_md5(s))
