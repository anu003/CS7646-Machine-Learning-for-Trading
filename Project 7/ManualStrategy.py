import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
import matplotlib.pyplot as plt
#import marketsimcode as ms
import marketsimcode as mm
from BestPossibleStrategy import *
from indicators import *

def author():
	return 'nmenon34'

def testPolicy(symbol = ['JPM'], sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000):
    orders = []
    lookback = 10
    
    holdings={sym:0 for sym in symbol}
  
    dates = pd.date_range(sd,ed)
    prices_1 = get_data(['JPM'],dates)
    price = prices_1['JPM']
    #prices = prices/prices[0]
    
    
    df_i = get_indicators(price)
    
    sma = df_i['SMA']
    
    
    bbp = df_i['bb_value']
    vol = df_i['volatility']
    moment = df_i['momentum']
    cci = df_i['CCI']
    
    
    sym = 'JPM'
    orders.append([sd,'JPM','HOLD',0])
    for day in range(lookback+1,df_i.shape[0]):
        
            if (sma.ix[day]<0.5) and (bbp.ix[day]<0.9) and (moment.ix[day]<0):
		
                if holdings[sym]<1000:
                    holdings[sym] += 1000
                    orders.append([price.index[day].date(),sym,'BUY',1000])
            
            
            elif (sma.ix[day]>2) and (bbp.ix[day]>1) and (moment.ix[day]<0):
		
                if holdings[sym]>0:
                    holdings[sym] -= 2000
                    orders.append([price.index[day].date(),sym,'SELL',2000])
                    
            elif (holdings[sym]<=0) and (holdings[sym] >= -1000):
                holdings[sym] -= 1000
                orders.append([price.index[day].date(),sym,'SELL',1000])
                
            elif (sma.ix[day]>1) and (sma.ix[day-1]<1) and (holdings[sym]>0):
                holdings[sym]=0
                orders.append([price.index[day].date(),sym,'SELL',1000])
            
            elif (sma.ix[day]<=1) and (sma.ix[day-1]>1) and (holdings[sym]<0):
                holdings[sym]=0
                orders.append([price.index[day].date(),sym,'BUY',1000])
        
    orders.append([ed,sym,'HOLD',0])
    
    
    
    res=pd.DataFrame(orders)
    res.columns=['Date','Symbol','Order','Shares']
    #res['Date'] = pd.to_datetime(res['Date']) 
    #res['Date'] = res['Date'].dt.date
    #res = res.set_index('Date')
    
    
    #print res
    p = compute_portvals(res)
    my_colors = ['black', 'blue']
    start_val = 100000
    ben = benchmark_trades('JPM')
    p3 = mm.compute_portvals(ben,start_val)
    
    plt.figure(figsize=(20,10))
    plt.gca().set_color_cycle(['black','blue'])
    plt.legend(loc="upper left")
    p = p/p[0]
    p3 = p3/p3[0]
    pp, = plt.plot(p)
    pb, = plt.plot(p3)
    plt.legend([pp,pb],['Manual','Benchmark'])

    plt.xlabel('Dates')
    plt.ylabel('Prices(normalized)')
    
	
	
    
            
    
    
    plt.show()	
    
    
    
    
    #print port
    return port
    
    
    
def compute_portvals(orderss, start_val = 100000, commission=0.00, impact=0.00):
    
    syms=orderss.Symbol.unique()
  
    orderss = orderss.sort_values(['Date'])

    sd=orderss['Date'].iloc[0]
    
    ed=orderss['Date'].iloc[-1]
    
    pricess=get_data(list(syms),pd.date_range(sd, ed))
    #FWD FILL

    pricess.fillna(method='ffill',inplace=True)
    pricess.fillna(method='bfill',inplace=True)
    pricess['Cash']= 1.0
   
    #COPY
    trades=pricess.copy()
    trades[:]=0.0
   
    for index,order in orderss.iterrows():
        action=order['Order']
	sym=order['Symbol']
	date=order['Date']
	if action=='SELL':
		trades[sym].loc[date] += -1*order['Shares']
		trades['Cash'].loc[date] += (order['Shares']*(pricess[sym].loc[date]-(impact*pricess[sym].loc[date])) - commission)
	elif action=='BUY':
		trades[sym].loc[date] += order['Shares']
		trades['Cash'].loc[date] += (-1*order['Shares']*(pricess[sym].loc[date]+(impact*pricess[sym].loc[date])) - commission)
		
    
    holding=trades.copy()
    
    holding['Cash'].iloc[0] += start_val
  
    
    for i in range(1,len(holding['Cash'])):
	   holding.iloc[i] += holding.iloc[i-1]
    
    df_value = holding.copy()
    df_value = df_value*pricess
    
    portvals = df_value.sum(axis=1)
    
    
    sf = 252
    rfr = 0
    cum_ret = (portvals[-1] / portvals[0]) - 1
    dr = (portvals / portvals.shift(1)) - 1
    #
    avg_daily_ret = dr.mean()
    std_daily_ret = dr.std()
    #
    sharpe_ratio = np.sqrt(sf) * ((dr.subtract(rfr)).mean() / (dr.std()))
    
    
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
   
    print
    #print "Final Portfolio Value: {}".format(portvals[-1])
    

    return portvals






def main():
    testPolicy()
    
    
    pass


if __name__ == "__main__": main()
