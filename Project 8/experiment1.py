"""
Experiment 1

@Name : Nidhi Nirmal Menon
@UserID : nmenon34
"""

import datetime as dt
import pandas as pd
import util as ut
import random
import numpy as np
import StrategyLearner as st
from ManualStrategy import testPolicy
from marketsimcode import compute_portvals
from util import get_data, plot_data
import matplotlib.pyplot as plt

def author(self):
    """
    @summary Returning the author user ID
    """
    return 'nmenon34'


def trades_ST(prices,symbol):
    trades = pd.DataFrame(columns=['Date', 'Symbol', 'Order', 'Shares'])
    index = 0
    for i in range(0, prices.shape[0]):
        if prices.ix[i,symbol] == 2000:
            trades.loc[index] = [prices.index[i].strftime('%Y-%m-%d'),symbol,'BUY',2000]
            index = index + 1
        elif prices.ix[i,symbol] == 1000:
            trades.loc[index] = [prices.index[i].strftime('%Y-%m-%d'),symbol,'BUY',1000]
            index = index + 1
        if prices.ix[i,symbol] == -2000:
            trades.loc[index] = [prices.index[i].strftime('%Y-%m-%d'),symbol,'SELL',2000]
            index = index + 1
        if prices.ix[i,symbol] == -1000:
            trades.loc[index] = [prices.index[i].strftime('%Y-%m-%d'),symbol,'SELL',1000]
            index = index + 1
    return trades


if __name__=="__main__":

    # setting the random seed
    np.random.seed(1234)

    # input
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009, 12, 31)
    symbol = ['JPM']
    dates = dates = pd.date_range(sd, ed)
    prices_all = ut.get_data(symbol, dates)

    # Strategy Learner
    learner = st.StrategyLearner(verbose = False, impact=0.0)
    learner.addEvidence(symbol="JPM",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    test = learner.testPolicy(symbol="JPM",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    st_trades = trades_ST(test,'JPM')
    st_port_val = compute_portvals(st_trades,sd,ed,100000,0,0)
    #trades = learner.testPolicy(symbol="JPM",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    #st_port_val = evalPolicy2("JPM",trades,100000,dt.datetime(2008,1,1),dt.datetime(2009,12,31),0,0)

    # Benchmark
    bench = pd.DataFrame(columns=['Date', 'Symbol', 'Order', 'Shares'])
    bench.loc[0] = [prices_all.index[0].strftime('%Y-%m-%d'),'JPM','BUY',1000]
    bench.loc[1] = [prices_all.index[-1].strftime('%Y-%m-%d'),'JPM','SELL',1000]
    bench_port_val = compute_portvals(bench,sd,ed,100000,0,0)

    # ManualStrategy
    trades,buydate,selldate = testPolicy(symbol=['JPM'], sd=sd ,ed=ed, sv=100000)
    ms_port_val = compute_portvals(trades,sd,ed,100000,0,0)

    # Printing Portfolio statistics
    daily_returns = (ms_port_val / ms_port_val.shift(1)) - 1
    daily_returns = daily_returns[1:]
    cr = (ms_port_val.iloc[-1] / ms_port_val.iloc[0]) - 1
    adr = daily_returns.mean()
    sddr = daily_returns.std()
    a = np.sqrt(252.0)
    sr = (a*(adr))/sddr

    '''
    print "Manual Strategy Stats"
    print "CR " + str(cr)
    print "Avg of daily returns " + str(adr)
    print "Std deviation of daily returns " + str(sddr)
    print "Sharpe Ratio " + str(sr)
    '''

    # Printing Benchmark statistics
    bench_dr = (bench_port_val / bench_port_val.shift(1)) - 1
    bench_dr = bench_dr[1:]
    cr = (bench_port_val.iloc[-1] / bench_port_val.iloc[0]) - 1
    adr = bench_dr.mean()
    sddr = bench_dr.std()
    a = np.sqrt(252.0)
    sr = (a*(adr))/sddr

    '''
    print "\nBenchmark Stats"
    print "CR " + str(cr)
    print "Avg of daily returns " + str(adr)
    print "Std deviation of daily returns " + str(sddr)
    print "Sharpe Ratio " + str(sr)
    '''

    # Printing StrategyLearner statistics
    st_dr = (st_port_val / st_port_val.shift(1)) - 1
    st_dr = st_dr[1:]
    cr = (st_port_val.iloc[-1] / st_port_val.iloc[0]) - 1
    adr = st_dr.mean()
    sddr = st_dr.std()
    a = np.sqrt(252.0)
    sr = (a*(adr))/sddr

    '''
    print "\nStrategy Learner Stats"
    print "CR " + str(cr)
    print "Avg of daily returns " + str(adr)
    print "Std deviation of daily returns " + str(sddr)
    print "Sharpe Ratio " + str(sr)
    '''

    # Plotting charts
    ms_port_val = ms_port_val / ms_port_val[0]
    bench_port_val = bench_port_val / bench_port_val[0]
    st_port_val = st_port_val / st_port_val[0]
    ax = ms_port_val.plot(fontsize=12, color="black", label="Manual Strategy")
    bench_port_val.plot(ax=ax, color="blue", label='Benchmark')
    st_port_val.plot(ax=ax, color="green", label='Strategy Learner')
    plt.title("Experiment 1")
    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio Value")
    plt.legend()
    plt.show()
