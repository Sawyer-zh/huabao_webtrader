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
    交易客户端:
    添加多个账户
    """
    clients = {

    }

    def __init__(self) -> None:
        """
        """
        with open('config.json') as f:
            accounts = json.load(f)['accounts']
            for i in range(len(accounts)):
                user = accounts[i]
                if path.exists("cookies_" + user['custno'] + '.txt'):
                    self.login_with_cookie(user)
                else:
                    login_ret = login(user)
                    if not login_ret:
                        Log.i("---客户:{}---登录失败".format(user['custno']))
                    else:
                        self.login_with_cookie(user)

    def login_with_cookie(self, user):
        with open('cookies_' + user['custno'] + '.txt') as r:
            cookies = r.readline()
            client = Trader(cookies)
            self.clients[user['custno']] = client
            Log.i('-客户:{}--登录成功---'.format(user['custno']))


clients = Client().clients
