"""MC1-P2: Optimize a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import scipy.optimize as spo
from util import get_data, plot_data

def f(allocs,normed,sv):
    #normed=prices/prices.values[0]
    alloced=normed.multiply(allocs)
    pos_vals=alloced.multiply(sv)
    port_val=pos_vals.sum(axis=1)
    dr=(port_val/port_val.shift(1))-1
    std_dev=dr.std()
    return std_dev

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    sv=1000000
    rfr=0.0
    sf=252.0

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY

    prices_all.fillna(method="ffill",inplace=True)
    prices_all.fillna(method="bfill",inplace=True)

    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    # allocs = np.asarray([0.2, 0.2, 0.3, 0.3]) # add code here to find the allocations

    n=len(syms)
    guess = 1.0/n
    
    #Generate array allocs for
    a_list=[guess]*n
    allocs=np.asarray(a_list)
    #print 'Allocs:',allocs
    normed=prices/prices.values[0]

    my_bounds=[(0.0,1.0) for i in normed.columns]
    #print "Bounds:", my_bounds

    my_constraints = ({ 'type': 'eq', 'fun': lambda inputs: 1.0 - np.sum(inputs) })

    my_result=spo.minimize(f,allocs,args=(normed,sv,), method='SLSQP', constraints=my_constraints, bounds=my_bounds, options={'disp':True})
    opt_allocs=my_result.x
    opt_sddr=my_result.fun
    #normed=prices/prices.values[0]
    alloced=normed.multiply(opt_allocs)
    pos_vals=alloced.multiply(sv)
    port_val=pos_vals.sum(axis=1)

    cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats
    dr=(port_val/port_val.shift(1))-1
    cr=(port_val[-1]/port_val[0])-1
    adr=dr.mean()
    sddr=opt_sddr
    a=np.sqrt(sf)
    sr=a*((dr.subtract(rfr)).mean())/sddr

    # Get daily portfolio value
    # port_val = prices_SPY # add code here to compute daily portfolio values
    

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
	port_val = port_val/port_val[0]
	prices_SPY = prices_SPY/prices_SPY[0]
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
	plot_data(df_temp, title="Daily portfolio value and SPY")
        pass

    return opt_allocs, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008,6,1)
    end_date = dt.datetime(2009,6,1)
    symbols = ['IBM', 'X', 'GLD']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = False)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
