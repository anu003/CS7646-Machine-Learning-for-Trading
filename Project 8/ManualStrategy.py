"""
Implementing Manual Rule Based Strategy using all the indicators from indicators.py

@Name : Nidhi Nirmal Menon
@UserID : nmenon34

"""


import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data
from marketsimcode import compute_portvals
from indicators import *
import matplotlib.pyplot as plt

def author(self):
    """
    @summary Returning the author user ID
    """
    return 'nmenon34'

def testPolicy(symbol,sd,ed,sv):
	dates = pd.date_range(sd, ed)
	prices_all = get_data(symbol, dates)
	prices = prices_all[symbol]
	flag = 0 # flag=1: have shares, flag=0 no shares, flag=-1 shorted
	lookback=20
	sym='JPM'
	sma = getSMA(prices,lookback,symbol)
	bollinger = getBollinger(prices,symbol,lookback,sma)
	psma = priceBySMA(prices, lookback, sma, symbol)
	volatility = getVolatility(prices,lookback,symbol)
	trades = pd.DataFrame(columns=['Date', 'Symbol', 'Order', 'Shares'])
	index=0
	buydate =[]
	selldate=[]

	for i in range(0, prices.shape[0]- 1):
		if flag == 0:
			if bollinger.ix[i,sym] < 0.2 or psma.ix[i,sym] < 0.6 or volatility.ix[i,sym] < -0.1:
				trades.loc[index] = [prices.index[i].strftime('%Y-%m-%d'),'JPM','BUY',1000]
				flag = 1
				index +=1
				buydate.append(prices.index[i].date())
			elif bollinger.ix[i,sym] > 0.8 or psma.ix[i,sym] > 1.1 or volatility.ix[i,sym] > 0.1:
				trades.loc[index] = [prices.index[i].strftime('%Y-%m-%d'),'JPM','SELL',1000]
				flag=-1
				index+=1
				selldate.append(prices.index[i].date())
		elif flag == -1:
			if bollinger.ix[i,sym] < 0.1 or psma.ix[i,sym] < 0.65 or volatility.ix[i,sym] < -0.2:
				trades.loc[index] = [prices.index[i].strftime('%Y-%m-%d'),'JPM','BUY',2000]
				flag = 1
				index +=1
				buydate.append(prices.index[i].date())
			elif bollinger.ix[i,sym] < 0.2 or psma.ix[i,sym] < 0.6 or volatility.ix[i,sym] < -0.1:
				trades.loc[index] = [prices.index[i].strftime('%Y-%m-%d'),'JPM','BUY',1000]
				flag = 0
				index +=1
		elif flag == 1:
				if bollinger.ix[i,sym] > 0.9 or psma.ix[i,sym] > 1.5 or volatility.ix[i,sym] > 0.2:
					trades.loc[index] = [prices.index[i].strftime('%Y-%m-%d'),'JPM','SELL',2000]
					flag = -1
					index +=1
					selldate.append(prices.index[i].date())
				elif bollinger.ix[i,sym] > 0.8 or psma.ix[i,sym] > 1.1 or volatility.ix[i,sym]>0.1:
					trades.loc[index] = [prices.index[i].strftime('%Y-%m-%d'),'JPM','SELL',1000]
					flag = 0
					index +=1

	if flag==1:
		trades.loc[index] = [prices.index[i].strftime('%Y-%m-%d'),'JPM','SELL',1000]
	if flag == -1:
		trades.loc[index] = [prices.index[i].strftime('%Y-%m-%d'),'JPM','BUY',1000]


	return trades, buydate, selldate


if __name__ == "__main__":
	sd = dt.datetime(2010,1,1)
	ed = dt.datetime(2011, 12, 31)
	symbol = ['JPM']
	dates = dates = pd.date_range(sd, ed)
	trades,buydate,selldate = testPolicy(symbol=['JPM'], sd=sd ,ed=ed, sv=100000)
	prices_all = get_data(symbol, dates)


	bench = pd.DataFrame(columns=['Date', 'Symbol', 'Order', 'Shares'])
	bench.loc[0] = [prices_all.index[0].strftime('%Y-%m-%d'),'JPM','BUY',1000]
	bench.loc[1] = [prices_all.index[-1].strftime('%Y-%m-%d'),'JPM','SELL',1000]

	# Manual Strategy
	ms_port_val = compute_portvals(trades,100000,9.95,0.005)

	# Benchmark
	bench_port_val = compute_portvals(bench,100000,9.95,0.005)

	# Printing Portfolio statistics
	daily_returns = (ms_port_val / ms_port_val.shift(1)) - 1
	daily_returns = daily_returns[1:]
	cr = (ms_port_val.iloc[-1] / ms_port_val.iloc[0]) - 1
	adr = daily_returns.mean()
	sddr = daily_returns.std()

	print "Manual Strategy Stats"
	print "CR " + str(cr)
	print "Avg of daily returns " + str(adr)
	print "Std deviation of daily returns " + str(sddr)


	# Printing Benchmark statistics
	bench_dr = (bench_port_val / bench_port_val.shift(1)) - 1
	bench_dr = bench_dr[1:]
	cr = (bench_port_val.iloc[-1] / bench_port_val.iloc[0]) - 1
	adr = bench_dr.mean()
	sddr = bench_dr.std()

	print "\nBenchmark Stats"
	print "CR " + str(cr)
	print "Avg of daily returns " + str(adr)
	print "Std deviation of daily returns " + str(sddr)

	# Plotting charts
	ms_port_val = ms_port_val / ms_port_val[0]
	bench_port_val = bench_port_val / bench_port_val[0]
	ax = ms_port_val.plot(fontsize=12, color="black", label="Manual Strategy")
	bench_port_val.plot(ax=ax, color="blue", label='Benchmark')
	for date in buydate:
		ax.axvline(date,color="green")
	for date in selldate:
		ax.axvline(date,color="red")
	plt.title(" Manual Strategy - out sample ")
	ax.set_xlabel("Date")
	ax.set_ylabel("Portfolio Value")
	plt.legend()
	plt.show()
