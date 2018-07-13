"""
Implementing a Strategy Learner

@Name : Nidhi Nirmal Menon
@UserID : nmenon34
"""

import datetime as dt
import pandas as pd
import util as ut
import random
import RTLearner as rt
import BagLearner as bl
from indicators import *

class StrategyLearner(object):

    def author(self):
        """
        @summary Returning the author user ID
        """
        return 'nmenon34'

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.learner = bl.BagLearner(learner = rt.RTLearner, kwargs = {"leaf_size":5}, bags = 20, boost = False, verbose = False)
        self.impact = impact

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):

        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        # prices_SPY = prices_all['SPY']  # only SPY, for comparison later

        # Getting the technical indicators
        lookback = 2
	#Indicator no. 1 : SMA
        sma = getSMA(prices,lookback,syms)
        copysma = sma.copy()
	#Indicator no. 2 : Bollinger bands
        bba = getBollinger(prices,syms,lookback,copysma)
	#Indicator no. 3 : Volatility
        volatility = getVolatility(prices,lookback,syms)

        # Constructing trainX
        df1=sma.rename(columns={symbol:'SMA'})
        df2=bba.rename(columns={symbol:'BBA'})
        df3=volatility.rename(columns={symbol:'VOL'})

        indicators = pd.concat((df1,df2,df3),axis=1)
        indicators.fillna(0,inplace=True)
        indicators=indicators[:-5]
        trainX = indicators.values

        # Constructing trainY
        trainY=[]
        for i in range(prices.shape[0]-5):
            ratio = (prices.ix[i+5,symbol]-prices.ix[i,symbol])/prices.ix[i,symbol]
            if ratio > (0.02 + self.impact):
                trainY.append(1)
            elif ratio < (-0.02 - self.impact):
                trainY.append(-1)
            else:
                trainY.append(0)
        trainY=np.array(trainY)

        # Training
        self.learner.addEvidence(trainX,trainY)


    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        # prices_SPY = prices_all['SPY']  # only SPY, for comparison later


	# Getting the technical indicators
        lookback = 2
	#Indicator no. 1 : SMA
        sma = getSMA(prices,lookback,syms)
        copysma = sma.copy()
	#Indicator no. 2 : Bollinger bands
        bba = getBollinger(prices,syms,lookback,copysma)
	#Indicator no. 3 : Volatility
        volatility = getVolatility(prices,lookback,syms)


        # Constructing testX
        df1=sma.rename(columns={symbol:'SMA'})
        df2=bba.rename(columns={symbol:'BBA'})
        df3=volatility.rename(columns={symbol:'VOL'})

        indicators = pd.concat((df1,df2,df3),axis=1)
        indicators.fillna(0,inplace=True)
        testX = indicators.values

        # Querying the learner for testY
        testY=self.learner.query(testX)

        # Constructing trades DataFrame
        trades = prices_all[syms].copy()
        trades.loc[:]=0
        flag=0
        for i in range(0,prices.shape[0]-1):
            if flag==0:
                if testY[i]>0:
                    trades.values[i,:] = 1000
                    flag = 1
                elif testY[i]<0:
                    trades.values[i,:] = -1000
                    flag = -1

            elif flag==1:
                if testY[i]<0:
                    trades.values[i,:]=-2000
                    flag=-1
                elif testY[i]==0:
                    trades.values[i,:]=-1000
                    flag = 0

            else:
                if testY[i]>0:
                    trades.values[i,:]=2000
                    flag=1
                elif testY[i]==0:
                    trades.values[i,:]=1000
                    flag=0

        if flag==-1:
            trades.values[prices.shape[0]-1,:]=1000
        elif flag==1:
            trades.values[prices.shape[0]-1,:]=-1000

        return trades

if __name__=="__main__":
    print "One does not simply think up a strategy"
    st = StrategyLearner()

    st.addEvidence(symbol="AAPL",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    st.testPolicy(symbol="AAPL",sd=dt.datetime(2010,1,1),ed=dt.datetime(2011,12,31),sv=100000)
