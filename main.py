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
from strategy.arbitrage.strategy import Strategy
from trader import client
import pandas as pd


class HeartBeat(threading.Thread):
    """
    心跳
    """
    def __init__(self ) -> None:
        """
        """
        threading.Thread.__init__(self)
    
    def run(self):
        while int(datetime.strftime(datetime.now(),'%H')) < 100:
            Log.i('--heart beat--')
            ret = client.position
            df = pd.DataFrame(ret['position'])
            # 打印持仓信息
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
            Strategy().execute()
            time.sleep(10)


if __name__ == "__main__":
    head_beat = HeartBeat()
    head_beat.start()

    strategy = ExecuteStrategy()
    strategy.start()
        

