"""
Implementing Technical Indicators
	1. Volatility
	2. Bollinger Bands
	3. Simple Moving Average

@Name : Nidhi Nirmal Menon
@UserID : nmenon34

"""
import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime
import os
from util import get_data, plot_data
import matplotlib.pyplot as plt
import math

def author(self):
    """
    @summary Returning the author user ID
    """
    return 'nmenon34'

# Calculating the Simple Moving Average
def getSMA(prices,lookback, symbols):
	price = prices[symbols]
	sma = price.rolling(window=lookback, center=False).mean()
	return sma


def getBollinger(prices, symbols, lookback, sma):
	price = prices[symbols]
	bollinger = price.copy()
	avg = price.rolling(window=lookback, center=False).mean()
	std = price.rolling(window=lookback, center=False).std()
	bollinger = (price - avg)/(2*std)
	return bollinger


def getVolatility(prices, lookback, symbols):
	price = prices[symbols]
	volatility = price.rolling(window=lookback, center=False).std()
	return volatility


# Calculating Price/SMA
def priceBySMA(prices, lookback, sma, symbols):
	for day in range(lookback,prices.shape[0]):
		for sym in symbols:
			sma.ix[day,sym]=prices.ix[day,sym]/sma.ix[day,sym]
	return sma




