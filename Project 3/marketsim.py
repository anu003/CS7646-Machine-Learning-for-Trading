"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    #read in data
    orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
    #sort dates
    orders_df=orders_df.sort_index()

    #scan symbols
    symbols = list(set(orders_df['Symbol'].values))
    #get date range
    orders_df.index=pd.to_datetime(orders_df.index)
    start_date=orders_df.index.values[0]
    end_date = orders_df.index.values[-1]
    dates = pd.date_range(start_date, end_date)

    #read in prices
    prices = get_data(symbols, dates)

    #add an extra column 'Cash' and initialize it to all ones
    prices['Cash'] = np.ones(prices.shape[0])

    #duplicate price df into a units df, intialize it to all zeros
    share_units=prices*0.0

    #initialize cash position with starting value
    share_units.iloc[0,-1]=start_val

    order=orders_df.iloc[0]

    #adjust share_units to show how stock units and cash are changing over time with orders

    for index2, row2 in orders_df.iterrows():
        stock_name = row2[0]
        order_price = prices[stock_name].ix[index2]
        order_units = row2[2]

	#set up signs as multipliers
        if row2[1]=="BUY":
            sign=-1
        else:
            sign=1

        #update share_units with order
        share_units.loc[index2,stock_name]+=order_units*sign*-1
        share_units.loc[index2,"Cash"]+=order_units*order_price*sign

	#deduct commission for every transaction
        share_units.loc[index2,"Cash"]-=commission

        #impact = no. of orders in transaction * price of each share * impact. deduct impact for every transaction
        my_impact=order_units*order_price*impact
        share_units.loc[index2,"Cash"]-=my_impact	

    #update share_units
    for i in range(1,share_units.shape[0]):
        for j in range (0,share_units.shape[1]):
            new_val=share_units.iloc[i,j]+share_units.iloc[i-1,j]
            share_units.iloc[i,j]=new_val

    #calculate port_vals
    port_vals=prices*share_units
    port_vals["port_val"]=port_vals.sum(axis=1)
    port_vals["daily_returns"] = (port_vals["port_val"][1:] / port_vals["port_val"][:-1].values) - 1
    port_vals["daily_returns"][0] = 0

    portvals=port_vals.iloc[:,-2:-1]
    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    #start_date = dt.datetime(2008,1,1)
    #end_date = dt.datetime(2008,6,1)
    #portvals = get_data(['IBM'], pd.date_range(start_date, end_date))
    #portvals = portvals[['IBM']]  # remove SPY

    return portvals

def author():
    return 'nmenon34' # replace tb34 with your Georgia Tech username.

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
    #cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]

    #portfolio stats calculated similar to assess_portfolio
    #rfr=0
    #sf=252
    #cum_ret=(portvals[-1]/portvals[0])-1
    #dr=(portvals/portvals.shift(1))-1
    #avg_daily_ret=dr.mean()
    #std_daily_ret=dr.std()
    #a=np.sqrt(sf)
    #sharpe_ratio=a*((dr.subtract(rfr)).mean())/std_daily_ret
    #cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

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
