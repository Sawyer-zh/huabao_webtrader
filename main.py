import threading
import json
import time
from time import sleep

from bs4.element import AttributeValueWithCharsetSubstitution
from trader.login import login
from trader.api import TraderApi as Trader
from trader.log import Log
from datetime import datetime
# from strategy.sdzz.strategy import Strategy
# from strategy.arbitrage.strategy import Strategy
from trader import clients
import pandas as pd


class HeartBeat(threading.Thread):
    """
    心跳
    """

    def __init__(self) -> None:
        """
        """
        threading.Thread.__init__(self)

    def run(self):
        while int(datetime.strftime(datetime.now(), '%H')) < 100:
            Log.i('--heart beat--')
            for k, client in clients.items():
                ret = client.position
                df = pd.DataFrame(ret['position'])
                # 打印持仓信息        'send_area': item['send_position'],

                Log.i("\n{}\ntotal_asset:{}\tsecurities:{}\tusable_money:{}\ttotal_profit:{}\ttoday_profit:{}".format(df,
                                                                                                                      ret['total_asset'],
                                                                                                                      ret['securities'],
                                                                                                                      ret['usable_money'],
                                                                                                                      ret['total_profit'],
                                                                                                                      ret['today_profit'],
                                                                                                                      ))
            time.sleep(60)


class ExecuteStrategy(threading.Thread):
    """
    执行策略
    """

    def __init__(self):
        """
        """
        threading.Thread.__init__(self)

    def run(self):
        """
        """
        while True:
            Log.d('---准备开始执行策略---')
            # Strategy().execute()
            # client.sell_stock('苏州银行','002966','SZ','8.86',100)
            client.sell_fund('弘盈A', '160520', 'SZ', '2.34', 81)
            time.sleep(1)


if __name__ == "__main__":
    head_beat = HeartBeat()
    head_beat.start()
    #client.sell_stock('东方财富','300059', 'SZ', 29.5, 300)
    #strategy = ExecuteStrategy()
    # strategy.start()
