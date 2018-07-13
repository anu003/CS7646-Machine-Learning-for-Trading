import pandas as pd
import numpy as np
import datetime as dt
import util as ut
import matplotlib.pyplot as plt

def get_indicators(df_prices, sym):
    prices=df_prices[sym]
    prices=prices/prices[0]
    
    df_indicators = pd.DataFrame(index=prices.index)
    
    #1] SMA
    df_indicators['price'] = prices
    df_indicators['rolling mean'] = prices.rolling(window=10,center=False).mean()
    
    #2] bollinger bands
    rm = prices.rolling(window=10,center=False).mean()
    sd = prices.rolling(window=10,center=False).std()
    upband = rm + (2*sd)
    dnband = rm - (2*sd)    
    df_indicators['upper band'] = upband
    df_indicators['lower band'] = dnband
    #BB value
    bb_value = (prices - rm)/(25 * sd)
    df_indicators['bb value'] = bb_value

    #3] Commodity channel index
    cci = (prices-rm)/(2.5 * prices.std())
    df_indicators['Commodity Channel Index'] = cci
    
    #4] Volatility
    volatility = prices.rolling(window=7,center=False).std()
    df_indicators['Volatility'] = volatility*3.5
    
    return df_indicators.dropna()

def author():
    return 'nmenon34'

def test_code():
    dev_sd=dt.datetime(2008,1,1)
    dev_ed=dt.datetime(2009,12,31)
    test_sd=dt.datetime(2010,1,1)
    test_ed=dt.datetime(2011,12,31)
    
    symbol='JPM'
    
    dates = pd.date_range(dev_sd, dev_ed)
    prices_all = ut.get_data([symbol], dates)
    
    #SMA
    get_indicators(prices_all, symbol)[['price', 'rolling mean']].plot(figsize=(20, 7))
    plt.show()
    
    #Bollinger
    get_indicators(prices_all, symbol)[['upper band', 'lower band', 'bb value', 'rolling mean']].plot(figsize=(20, 7))
    plt.show()
    
    #CCI
    get_indicators(prices_all, symbol)[['Commodity Channel Index']].plot(figsize=(20, 7))
    plt.show()
    
    #Volatility
    get_indicators(prices_all, symbol)[['Volatility']].plot(figsize=(20, 7))
    plt.show()

    plt.axhline(y=0, linestyle=':')
    plt.axhline(y=0.04, linestyle='--')
    plt.axhline(y=-0.04, linestyle='--')

if __name__ == "__main__":
    test_code()