"""
Experiment 2

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


    # Strategy Learner - impact = 0.0005
    learner = st.StrategyLearner(verbose = False, impact=0.0005)
    learner.addEvidence(symbol="JPM",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    test = learner.testPolicy(symbol="JPM",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    st_trades = trades_ST(test,'JPM')
    st_port_val = compute_portvals(st_trades,sd,ed,100000,0,0.0005)


    # Strategy Learner - impact = 0.005
    learner = st.StrategyLearner(verbose = False, impact=0.005)
    learner.addEvidence(symbol="JPM",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    test = learner.testPolicy(symbol="JPM",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    st_trades = trades_ST(test,'JPM')
    st_port_val2 = compute_portvals(st_trades,sd,ed,100000,0,0.005)


    # Strategy Learner - impact = 0.05
    learner = st.StrategyLearner(verbose = False, impact=0.05)
    learner.addEvidence(symbol="JPM",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    test = learner.testPolicy(symbol="JPM",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    st_trades = trades_ST(test,'JPM')
    st_port_val3 = compute_portvals(st_trades,sd,ed,100000,0,0.05)


    # Printing StrategyLearner statistics
    st_dr = (st_port_val / st_port_val.shift(1)) - 1
    st_dr = st_dr[1:]
    cr = (st_port_val.iloc[-1] / st_port_val.iloc[0]) - 1
    adr = st_dr.mean()
    sddr = st_dr.std()
    a = np.sqrt(252.0)
    sr = (a*(adr))/sddr

    '''
    print "\nStrategy Learner Stats - impact=0.0005"
    print "CR " + str(cr)
    print "Avg of daily returns " + str(adr)
    print "Std deviation of daily returns " + str(sddr)
    print "Sharpe Ratio " + str(sr)
    '''

    # Printing StrategyLearner statistics
    st_dr = (st_port_val2 / st_port_val2.shift(1)) - 1
    st_dr = st_dr[1:]
    cr = (st_port_val2.iloc[-1] / st_port_val2.iloc[0]) - 1
    adr = st_dr.mean()
    sddr = st_dr.std()
    a = np.sqrt(252.0)
    sr = (a*(adr))/sddr

    '''
    print "\nStrategy Learner Stats - impact=0.005"
    print "CR " + str(cr)
    print "Avg of daily returns " + str(adr)
    print "Std deviation of daily returns " + str(sddr)
    print "Sharpe Ratio " + str(sr)
    '''

    # Printing StrategyLearner statistics
    st_dr = (st_port_val3 / st_port_val3.shift(1)) - 1
    st_dr = st_dr[1:]
    cr = (st_port_val3.iloc[-1] / st_port_val3.iloc[0]) - 1
    adr = st_dr.mean()
    sddr = st_dr.std()
    a = np.sqrt(252.0)
    sr = (a*(adr))/sddr

    '''
    print "\nStrategy Learner Stats - impact=0.05"
    print "CR " + str(cr)
    print "Avg of daily returns " + str(adr)
    print "Std deviation of daily returns " + str(sddr)
    print "Sharpe Ratio " + str(sr)
    '''

    # Plotting charts
    st_port_val = st_port_val / st_port_val[0]
    st_port_val2 = st_port_val2 / st_port_val2[0]
    st_port_val3 = st_port_val3 / st_port_val3[0]
    ax = st_port_val.plot(fontsize=12, color="black", label="Strategy Learner - impact = 0.0005")
    st_port_val2.plot(ax=ax, color="blue", label='Strategy Learner - impact = 0.005')
    st_port_val3.plot(ax=ax, color="green", label='Strategy Learner - impact = 0.05')
    plt.title("Experiment 2")
    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio Value")
    plt.legend()
    plt.show()
