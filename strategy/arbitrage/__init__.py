# 转债套利工具

from trader.util import quotation


def get_info(stock_code, bond_code, convert_price):
    """
    计算溢价率(实时): 转债价格 / 转股价值  - 1 
    计算溢价率1(卖股买债): 转债价格卖3价 / 转股价值  - 1 
    计算溢价率1(卖债买股): 转债价格买3价 / 转股价值  - 1 

    """

    stock = quotation(stock_code)
    bond = quotation(bond_code)
    overflow = float(bond['price']) / (100 / convert_price * float(stock['price'])) - 1
    overflow_1 = float(bond['ask3']) / (100 / convert_price * float(stock['bid3'])) - 1
    overflow_2 = float(bond['bid3']) / (100 / convert_price * float(stock['ask3'])) - 1
    return overflow, overflow_1, stock['bid3'], bond['ask3'] , overflow_2, bond['bid3'], stock['ask3']


if __name__ == "__main__":
    print(get_info('sz002002','sz128085',3.92))

