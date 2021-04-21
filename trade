#!/usr/bin/env python3
from trader import client 
import sys
import getopt


if __name__ == "__main__":
    try:
        option, args = getopt.getopt(sys.argv[1:], 'hc:p:n:')
    except:
        print("error params")

    for opt, value in option:
        if '-h' == opt:
            print("""
            trade cli:
                -c code
                -p price
                -n num
                -h show this
            """)
            exit()
        elif '-c' == opt:
            code = value
        elif '-p' == opt:
            price = value
        elif '-n' == opt:
            num = value


    df = client.position['position']
    market = df.loc[df['stock_code'] == code]['market'].values[0]
    name = df.loc[df['stock_code'] == code]['stock_name'].values[0]
    if int(num) > 0:
        if code[0] in [1]:
            client.buy_bond(name, code, market, price, num)
        else:
            client.buy_stock(name, code, market, price, num)
    else:
        if code[0] in [1]:
            client.sell_bond(name, code, market, price, 0 - int(num))
        else:
            client.sell_stock(name, code, market, price, 0 - int(num))
