import logging
import sys
from datetime import datetime

str_def_fmt = "%(asctime)s.%(msecs)03d %(thread)d %(levelname)s " \
              "%(module)s %(filename)s:%(lineno)d %(funcName)s: %(message)s"

# 控制日志输出到终端或者文件
logging.basicConfig(level=logging.DEBUG
                    , format=str_def_fmt
                    , datefmt="%Y-%m-%d %H:%M:%S"
                    , stream=sys.stdout
                   # , filename='log/{}.log'.format(datetime.strftime(datetime.now(),'%Y%m%d'))
                    )

logger = logging.getLogger("log")

class Log():

    @classmethod
    def d(cls,msg):
        logger.debug(msg)

    @classmethod
    def i(cls,msg):
        logger.info(msg)

    @classmethod
    def e(cls,msg):
        logger.error(msg)
    
    @classmethod
    def f(cls,msg):
        logger.fatal(msg)


if __name__ == "__main__":
    Log.d('tt') 
