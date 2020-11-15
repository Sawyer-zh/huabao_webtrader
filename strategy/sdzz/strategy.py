#! /usr/bin/env python3
# -*- coding:utf-8 -*-
from datetime import datetime
import os
import json
from trader.log import Log
from .hq import HQ
import time
from datetime import datetime
from threading import Thread

class Strategy():

    """
    双低转债轮动策略
    """
    def __init__(self) -> None:
        with open(os.path.split(os.path.abspath(__file__))[0] + '/config.json','r') as r:
            self.config = json.load(r)

    def execute(self):
        """
        转债轮动执行策略
        """
        redeem_list = HQ.get_redeem()
        while int(datetime.strftime(datetime.now(), '%H')) < 15:
            Log.d('----策略轮询中----')
            position = position()['position']

            # 获取转债数据
            bond_list = []
            for item in position:
                if item['stock_code'][0] == '1' and item['usable'] > 0:
                    if item['current'] >= 125:
                        pass
                        


        
class Entrust(Thread):
    """
    """
    def __init__(self) -> None:
        Thread.__init__(self)
         



if __name__ == "__main__":
    print(Strategy())
