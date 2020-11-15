#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import pymysql
import json
from .log import Log
from phpserialize import loads, dict_to_list

with open('config.json','r') as r:
    config = json.load(r)

class DB():

    """
    """
    def __init__(self) -> None:
        self.db = pymysql.connect(
                                  config['db_host'],
                                  config['db_user'],
                                  config['db_passwd'],
                                  config['db_name'],
                                  charset='utf8'
                                  )
        self.cursor = self.db.cursor()

    def modify(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
           # 发生错误时回滚
            Log.d("---更新失败---")
            self.db.rollback()
        finally:
            self.cursor.close()
    
    def select(self,sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except:
           Log.d("---查询失败---")
        finally:
            self.cursor.close()
 
# 关闭数据库连接
    def close(self):
        self.db.close()

if __name__ == "__main__":
    data = DB().select("select * from cache where `key`='cb_data'")
    print(data[0][1])
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
    print(ret)
