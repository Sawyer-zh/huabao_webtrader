import threading
import json
import time
from time import sleep
from trader.login import login
from trader.api import TraderApi as Trader
from trader.log import Log
from datetime import datetime
from strategy.sdzz.strategy import Strategy


class HeartBeat(threading.Thread):
    """
    心跳
    """
    def __init__(self ) -> None:
        """
        """
        threading.Thread.__init__(self)
    
    def run(self):
        while int(datetime.strftime(datetime.now(),'%H')) < 15:
            ret = client.position() 
            Log.i(ret)
            time.sleep(60)
            Log.i('--heart beat--')
        

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
        Log.d('---准备开始执行策略---')
        Strategy.execute()


if __name__ == "__main__":
    with open('config.json') as f:
        user = json.load(f)
    login_ret = login(user)
    if not login_ret:
        exit()
    else:
        with open('cookies.txt') as r:
            cookies = r.readline()
        client = Trader(cookies)
        head_beat = HeartBeat(client)
        head_beat.start()
        strategy = ExecuteStrategy(client)
        strategy.start()
        

