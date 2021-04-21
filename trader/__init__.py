#! /usr/bin/env python3
# -*- coding=utf-8 -*-

import json
from .login import login
from .api import TraderApi as Trader
from .log import Log
from os import path


__author__ = 'sawyer'
__version__ = '1.0.0'

class Client():
    """
    交易客户端
    """
    def __init__(self) -> None:
        """
        """
        with open('config.json') as f:
            if path.exists('cookies.txt'): 
                self.login_with_cookie()
            else:
                user = json.load(f)
                login_ret = login(user)
                if not login_ret:
                    Log.i("---登录失败---")
                    exit()
                else:
                    self.login_with_cookie()
   
    def login_with_cookie(self):
        with open('cookies.txt') as r:
            cookies = r.readline()
            client = Trader(cookies)
            self.client = client
            Log.i('---登录成功---')
    

client = Client().client