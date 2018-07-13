"""
Marketsim code modified to handle a pandas dataframe as input.
Code taken from the marketsim assignment and slightly modified.

@Name : Nidhi Nirmal Menon
@UserID : nmenon34

"""

import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime
import os
from util import get_data, plot_data

def author(self):
    """
    @summary Returning the author user ID
    """
    return 'nmenon34'

def compute_portvals(df, sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    #df = pd.read_csv(orders_file, index_col='Date', parse_dates=True)
    # df = pd.read_csv(orders_file, parse_dates=True)
    # print df
    # df = df.sort_values(by='Date',ascending=True)
    # print "Sorted"
    # print df

    # Building the prices data frame
    start_date = datetime.strptime(df['Date'].min(),'%Y-%m-%d')
    #end_date = datetime.strptime(df['Date'].max(),'%Y-%m-%d')
    end_date = ed
    dates = pd.date_range(start_date, end_date)
    syms = df['Symbol'].unique().tolist()
    prices_all = get_data(syms, dates)
    prices_all.fillna(method="ffill",inplace=True)
    prices_all.fillna(method="bfill",inplace=True)
    prices = prices_all[syms]
    prices['Cash'] = 1

    # Building the trades data frame
    trades = prices.copy()
    trades[:] = 0

    # Populating the trades DataFrame
    nrow = df.shape[0]
    for k in range(0,nrow):
        i = datetime.strptime(df.ix[k,'Date'],'%Y-%m-%d')

        if i not in prices.index:
            continue

        j = df.ix[k,'Symbol']
        if df.ix[k,'Order'] == 'BUY':
            trades.ix[i,j] += df.ix[k,'Shares']
            trades.ix[i,'Cash'] += (-1*df.ix[k,'Shares']*prices.ix[i,j]*(1+impact))
        elif df.ix[k,'Order'] == 'SELL':
            trades.ix[i,j] -= df.ix[k,'Shares']
            trades.ix[i,'Cash'] += (1*df.ix[k,'Shares']*prices.ix[i,j]*(1-impact))
        trades.ix[i,'Cash'] -= commission

    # Building the initial holdings
    holdings = trades.copy()
    holdings.ix[0,'Cash'] += start_val

    # Populating holdings
    nrow = holdings.shape[0]
    for i in range(1,nrow):
        holdings.ix[i,:] += holdings.ix[i-1,:]

    # Populating values
    values = pd.DataFrame(prices.values*holdings.values, columns=prices.columns, index=prices.index)

    # Populating portvals
    portvals = values.sum(axis=1)

    return portvals


def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-02.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
