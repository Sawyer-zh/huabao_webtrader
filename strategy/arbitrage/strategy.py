import os
import json
from datetime import datetime
from typing import overload
from strategy.arbitrage import get_info
from trader import client
import math
from .config import config


class Strategy():
    """
    可转债套利程序:
    难点: 如何判断是否已经成交
    """

    def __init__(self) -> None:
        self.config = config

    def execute(self):
        """
        转债轮动执行策略
        """
        self.bond_to_stock()

    def stock_to_bond(self):
        """
        卖股买债
        """
        overflow, overflow_1, stock_bid3, bond_ask3, _, _, _ = get_info(
            self.config['stock_code'], self.config['bond_code'], self.config['convert_price'])
        print(overflow, overflow_1, stock_bid3, bond_ask3)
        if(overflow_1 < self.config['overflow_1']):
            # 卖股票 买转债
            df_position = client.position['position']
            stock_value = df_position.loc[df_position['stock_code']
                                          == self.config['stock_code'][2:]].market_value
            stock_amount = df_position.loc[df_position['stock_code']
                                           == self.config['stock_code'][2:]].usable
            if 'SH' == df_position.loc[df_position['stock_code']
                                       == self.config['stock_code'][2:]].market:
                bond_should_buy_amount = math.floor(
                    float(stock_value) / float(bond_ask3) / 10)
            else:
                bond_should_buy_amount = math.floor(
                    float(stock_value) / float(bond_ask3) / 10) * 10
            sell_stock_ret = client.sell_stock(
                self.config['stock_name'], self.config['stock_code'][2:], self.config['stock_code'][0:2].upper(), stock_bid3, stock_amount)
            print(sell_stock_ret)
            buy_bond_ret = client.buy_bond(
                self.config['bond_name'], self.config['bond_code'][2:], self.config['bond_code'][0:2].upper(), bond_ask3, bond_should_buy_amount)
            print(buy_bond_ret)
            exit()

    def bond_to_stock(self):
        """
        卖债买股
        """
        overflow, _, _, _, overflow_2, bond_bid3, stock_ask3 = get_info(
            self.config['stock_code'], self.config['bond_code'], self.config['convert_price'])
        print(overflow, overflow_2, stock_ask3, bond_bid3)
        if(overflow_2 > self.config['overflow_2']):
            # 卖股票 买转债
            df_position = client.position['position']
            bond_value = df_position.loc[df_position['stock_code']
                                         == self.config['bond_code'][2:]].market_value
            bond_amount = df_position.loc[df_position['stock_code']
                                          == self.config['bond_code'][2:]].usable
            stock_should_buy_amount = math.floor(
                float(bond_value) / float(stock_ask3) / 100) * 100
            sell_bond_ret = client.sell_bond(
                self.config['bond_name'], self.config['bond_code'][2:], self.config['bond_code'][0:2].upper(), bond_bid3, bond_amount)
            buy_stock_ret = client.buy_stock(
                self.config['stock_name'], self.config['stock_code'][2:], self.config['stock_code'][0:2].upper(), stock_ask3, stock_should_buy_amount)
            exit()
