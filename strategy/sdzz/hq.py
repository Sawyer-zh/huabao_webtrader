from trader.db import DB
import pandas as pd
from phpserialize import dict_to_list, loads
import json

class HQ():
    """
    获取行情数据
    """
    @classmethod
    def get_hq(cls):
        """
        从数据库获取行情
        """
        data = DB().select("select * from cache where `key`='cb_data'")
        cb_lists = dict_to_list(loads(data[0][1].encode('utf-8')))
        ret = []
        for item in cb_lists:
            d ={}
            for (k, v) in item.items():
                if type(k) is bytes:
                    k = k.decode()
                if type(v) is bytes:
                    v = v.decode()
                d[k] = v
            ret.append(d)
        return pd.DataFrame(ret)

    @classmethod
    def get_redeem(cls):
        """
        获取强赎代码列表
        """
        data = DB().select("select info from cb_stock where `type`={} order by id desc limit 10".format(10001))
        return json.loads(data[0][0])


if __name__ == "__main__":
    print(HQ.get_hq().sort_values(by='score').head(10))
    print(HQ.get_redeem())


