import os
import json
from datetime import datetime
from strategy.arbitrage import get_info


class Strategy():
    """
    可转债套利程序
    """
    def __init__(self) -> None:
        with open(os.path.split(os.path.abspath(__file__))[0] + '/config.json','r') as r:
            self.config = json.load(r)

    def execute(self):
        """
        转债轮动执行策略
        """
        while int(datetime.strftime(datetime.now(), '%H')) < 15:
            overflow = get_info(self.config['stock_code'],self.config['bond_code'],self.config['convert_price'])
            if(overflow < self.config['overflow']):
                
     



