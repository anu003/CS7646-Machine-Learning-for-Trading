import pandas as pd
import numpy as np
import datetime as dt
import util as ut
import matplotlib.pyplot as plt
from marketsimcode import *

def testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
    dates = pd.date_range(sd,ed)
    df_prices = ut.get_data([symbol], dates)
    prices=df_prices[symbol]
    prices=prices/prices[0]
   
    df1=pd.DataFrame()
    df2=pd.DataFrame()
    df1['ORDER'] = prices < prices.shift(-1)

    df1['ORDER'].replace(True, 'BUY', inplace=True)
    df1['ORDER'].replace(False, 'SELL', inplace=True)

    df2['ORDER'] = df1['ORDER'].append(
    df1['ORDER'].shift(1).replace('BUY', 'TMP').replace('SELL', 'BUY').replace('TMP', 'SELL').dropna())

    df2['SYMBOL'] = 'JPM'
    df2['SHARES'] = 1000

    df2.sort_index(inplace=True)
    
    return df2

def author():
    return 'nmenon34'

def test_code():
    dev_sd=dt.datetime(2008,1,1)
    dev_ed=dt.datetime(2009,12,31)
    test_sd=dt.datetime(2010,1,1)
    test_ed=dt.datetime(2011,12,31)
    
    symbol='JPM'
    dates = pd.date_range(dev_sd, dev_ed)
    prices_all = ut.get_data([symbol], dates)
    
    prices=prices_all[symbol]
    prices=prices/prices[0]
    
    sv = 100000
    
    df3=testPolicy(symbol = "JPM", sd=dev_sd, ed=dev_ed, sv = 100000)
    port_vals = compute_portvals(df3, sv, 0, 0)
    #port_vals
    
    df3=pd.DataFrame(index=prices.index, columns=['ORDER','SYMBOL','SHARES'])
    df3['ORDER'] = 'BUY'
    df3['SYMBOL'] = 'JPM'
    df3['SHARES'] = 1000
    df4 = df3[:1]
    #df4
    df5 = df3.copy().tail(1)
    df5['ORDER'] = 'BUY'
    df5['SYMBOL'] = 'JPM'
    df5['SHARES'] = 0
    df4 = df4.append(df5)
    #df4
    bench_vals = compute_portvals(df4, sv, 0, 0)
    #bench_vals
    
    plt.figure(figsize=(20,7))
    plt.gca().set_color_cycle(['black', 'blue'])
    port, = plt.plot(port_vals)
    bench, = plt.plot(bench_vals)
    plt.legend([port, bench], ['Portfolio', 'Benchmark'])
    plt.title("Portfolio vs Benchmark")
    plt.show()

if __name__ == "__main__":
    test_code()
    