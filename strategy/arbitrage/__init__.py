# 转债套利工具

from trader.util import quotation


def get_info(stock_code, bond_code, convert_price):
    """
    计算溢价率: 转债价格 / 转股价值  - 1 
    """

    stock = quotation(stock_code)
    bond = quotation(bond_code)
    overflow = float(bond['ask1']) / (100 / convert_price * float(stock['bid1'])) - 1
    return overflow, bond['ask1'] , stock['bid1'] 


if __name__ == "__main__":
    print(get_info('sz002002','sz128085',3.92))

