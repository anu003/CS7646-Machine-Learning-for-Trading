"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data


def author():
    return 'nmenon34'

def compute_portvals(order, start_val = 1000000, commission=0.00, impact=0.00):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    print
    #order = pd.read_csv(orders_file, index_col='Date',parse_dates=True, na_values=['nan'])
    order = order.sort_index()
    Symbol_list = list(set(order['Symbol'].tolist()))
    symbol_list = order['Symbol'].tolist()
    symbols = list(set(symbol_list))
    #print order

    #order['Date'] = pd.to_datetime(order['Date']).dt.date
    #order = order.set_index('Date')
    #order.index = pd.to_datetime(order.index)
    #order['Date'] = order['Date'].dt.date
    #order.index = (order.index).normalize()

    start_date = order.index[0]
    print start_date
    end_date = order.index[-1]
    dates_range = pd.date_range(start_date, end_date)

    sym = list(set(order['Symbol'].values))
    prices = get_data(sym, dates_range)
    prices['Cash'] = 1.00


    trade = pd.DataFrame(index = prices.index, columns = prices.columns)
    trade = trade.fillna(0)
    trade['Cash'] = 0.00

    holdings = pd.DataFrame(index=prices.index, columns=prices.columns)
    holdings = holdings.fillna(0)
    holdings['Cash'] = 0.00


    value = 0.0
    share_amt = 0.0
    no_of_shares = 0
    hold_value = start_val
    share_gain_loss = 0

    action = 0

    for index, o in order.iterrows():
        #print index
        #index = pd.DatetimeIndex(index).normalize()
        
        if o['Order'] == 'BUY':
            action = -1
        elif o['Order'] == 'SELL':
            action = 1

        no_of_shares = o['Shares']
        symbol = o['Symbol']
        date = index
        
        
        
        
        share_amt = prices.ix[date,symbol]

        value = action * no_of_shares * share_amt
        share_gain_loss = action * no_of_shares * -1

        trade.ix[index,symbol] += share_gain_loss
        trade.ix[index,'Cash'] += value
        trade.ix[index,'Cash'] -= commission
        imp = impact * no_of_shares * share_amt
        trade.ix[index,'Cash'] -=imp

    holdings.ix[0,:] = trade.ix[0,:]
    holdings['Cash'][0] += start_val

    df_values = pd.DataFrame(index=prices.index, columns=prices.columns)
    df_values = df_values.fillna(0)
    df_values['Cash'] = 1.00



    for i in range(1,len(prices.index)):
        holdings.ix[i,:] = holdings.ix[i-1,:] + trade.ix[i,:]






    df_values = prices * holdings


    portvals = df_values.sum(axis=1)


    sf = 252
    rfr = 0
    cum_ret = (portvals[-1] / portvals[0]) - 1
    dr = (portvals / portvals.shift(1)) - 1
    #
    avg_daily_ret = dr.mean()
    std_daily_ret = dr.std()
    #
    sharpe_ratio = np.sqrt(sf) * ((dr.subtract(rfr)).mean() / (dr.std()))
    
    #print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
   
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

    return portvals

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders2.csv"
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

    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2, 0.01, 0.02, 1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2, 0.01, 0.02, 1.5]

    # sf = 252
    # rfr = 0
    # cum_ret = (portvals[-1] / portvals[0]) - 1
    # dr = (portvals / portvals.shift(1)) - 1
    #
    # avg_daily_ret = dr.mean()
    # std_daily_ret = dr.std()
    #
    # sharpe_ratio = np.sqrt(sf) * ((dr.subtract(rfr)).mean() / (dr.std()))






    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    #print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
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
    #print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
