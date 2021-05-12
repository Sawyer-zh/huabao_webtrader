#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import requests
from .log import Log
import time
from bs4 import BeautifulSoup
import pandas as pd


def get_current_timestamp():
    """
    """
    return str(int(time.time() * 1000))


class TraderApi():
    """
    交易api类
    """
    URL_BASE = "https://m.touker.com/trading/"

    API_DICT = {
        "ENTRUST": "securitiesEntrust.json",
        "BASE_INFO": "baseInfo.json",
        "POSITION": "trade/trading-sub/position",
    }

    def __init__(self, cookies):
        """
        传入cookie  字典或者字符串
        cookie 字符串里面 _e_ 里面的"前面的反斜线需要保留,下面是正确示例
        '_e_': '"{\\\\"id\\\\":\\\\"8B6E72EB4E1FDDDD\\\\",\\\\"_e_\\\\":\\\\"653732DF6C3858D7ABF14C86E611846D\\\\",\\\\"_sign_\\\\":\\\\"27630C84\\\\"}"', 'ssid': '"5S3ASI2n5Hk="', '_s_': '"{\\\\"id\\\\":\\\\"8B6E72EB4E1FDDDD\\\\",\\\\"_e_\\\\":\\\\"653732DF6C3858D7ABF14C86E611846D\\\\",\\\\"_sign_\\\\":\\\\"14D8CA0A\\\\"}"',
        """
        self.cookies = cookies

    def entrust(self, stock_name,
                stock_code,
                exchange,
                security_type,
                price,
                num,
                entrust_type,
                ):
        """

        """
        return self.requests(
            'ENTRUST',
            {
                "stockName": stock_name,
                "stockCode": stock_code,
                "exchange": exchange,
                "securityType": security_type,
                "price": price,
                "num": num,
                "entrustType": entrust_type,
                "channel": "",
                "deviceInfo": '',
            }
        )

    def buy(self, stock_name,
            stock_code,
            exchange,
            security_type,
            price,
            num,
            ):
        """
        买
        """
        return self.entrust(
            stock_name,
            stock_code,
            exchange,
            security_type,
            price,
            num,
            '1',
        )

    def buy_bond(self, stock_name,
                 stock_code,
                 exchange,
                 price,
                 num,
                 ):
        """
        买债券
        """
        return self.buy(
            stock_name,
            stock_code,
            exchange,
            '7',
            price,
            num,
        )

    def buy_stock(self, stock_name,
                  stock_code,
                  exchange,
                  price,
                  num,
                  ):
        """
        买股票
        """
        return self.buy(
            stock_name,
            stock_code,
            exchange,
            '4',
            price,
            num,
        )

    def buy_fund(self, stock_name,
                  stock_code,
                  exchange,
                  price,
                  num,
                  ):
        """
        买基金
        """
        return self.buy(
            stock_name,
            stock_code,
            exchange,
            '3',
            price,
            num,
        )
    
    def sell(self, stock_name,
             stock_code,
             exchange,
             security_type,
             price,
             num,
             ):
        """
        卖
        """
        return self.entrust(
            stock_name,
            stock_code,
            exchange,
            security_type,
            price,
            num,
            '2',
        )

    def sell_bond(self, stock_name,
                  stock_code,
                  exchange,
                  price,
                  num,
                  ):
        """
        卖债券
        """
        return self.sell(
            stock_name,
            stock_code,
            exchange,
            '7',
            price,
            num,
        )

    def sell_stock(self, stock_name,
                   stock_code,
                   exchange,
                   price,
                   num,
                   ):
        """
        卖股票
        """
        return self.sell(
            stock_name,
            stock_code,
            exchange,
            '4',
            price,
            num,
        )

    def sell_fund(self, stock_name,
                   stock_code,
                   exchange,
                   price,
                   num,
                   ):
        """
        卖基金
        """
        return self.sell(
            stock_name,
            stock_code,
            exchange,
            '3',
            price,
            num,
        )

    def baseinfo(self):
        """
        获取资产情况(请使用position接口)
        """
        return self.requests('BASE_INFO', {"_": get_current_timestamp})

    @property
    def position(self):
        """
        获取持仓情况
        """
        s = self.requests('POSITION', {"_": get_current_timestamp()}).text
        soup = BeautifulSoup(s, 'lxml')
        ret = soup.find_all('div', class_='position-my')
        for i in ret:
            r = i.find_all('div', class_='item')
            total_asset = r[0].get_text().strip().split('\n')[1]
            total_profit = r[1].get_text().strip().split('\n')[1]
            today_profit = r[2].get_text().strip('\n').split('\n')[-1]
            securities = r[3].get_text().strip().split('\n')[1]
            usable_money = r[4].get_text().strip().split('\n')[1]
        p = {
            'total_asset': total_asset,
            'total_profit': total_profit,
            'today_profit': today_profit,
            'securities': securities,
            'usable_money': usable_money,
        }
        ret = soup.find_all('div', class_='list-item border-bottom')
        position = []
        for item in ret:
            r = item.find_all('div', class_='item-cell')
            t1 = r[0].get_text().strip().split('\n')
            stock_name, market_value = t1[0::2]
            stock_code, market = t1[1].split('.')
            cost, current = r[1].get_text().strip().split('\n')
            total, usable = r[2].get_text().strip().split('\n')
            try:
                profit, profit_percent = r[3].get_text().strip().split('\n')
            except:
                profit, profit_percent = ['' , '']
            position.append(
                {
                    'stock_name': stock_name,
                    'stock_code': stock_code,
                    'market': market,
                    'market_value': market_value,
                    'cost': cost,
                    'current': current,
                    'total': total,
                    'usable': usable,
                    'profit': profit,
                    'profit_percent': profit_percent,
                }
            )
        p['position'] = pd.DataFrame(position)
        return p

    def requests(self, api, json):
        cookies = {}
        if isinstance(self.cookies, str):
            for item in self.cookies.split('; '):
                k, v = item.split('=', 1)
                cookies[k] = v
        else:
            # 当做字典
            cookies = self.cookies
        Log.i(json)
        return requests.post(self.URL_BASE + self.API_DICT[api], data=json, cookies=cookies)
