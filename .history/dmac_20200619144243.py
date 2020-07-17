import yfinance as yf
import numpy as np
from scipy.stats import norm
import pandas as pd
from pandasgui import show

def main():
    tickers = 'SPY AAPL MRNA TSLA'
    data = yf.download(tickers, period='max', group_by='ticker')
    frame = clean_data(pd.DataFrame(data['TSLA']))
    sma = frame.rolling(100).mean()
    lma = frame.rolling(750).mean()
    crossovers = calc_crossovers(sma, lma)
    show(sma, lma, crossovers)

def clean_data(data):
    data = data[~(np.isnan(data['Open']) | 
    np.isnan(data['High']) |
    np.isnan(data['Low']) |
    np.isnan(data['Close']) |
    np.isnan(data['Adj Close']) |
    np.isnan(data['Volume']))]
    return data

def calc_crossovers(sma, lma):
    #Currently using only closing prices
    sma = sma['Close']
    lma = lma['Close']
    #sma corresponds to 0
    show(sma, lma, sma > lma)
    higher = lma
    # crossovers = (sma['Low'] - lma['Low']) * (sma['High'] - lma['High']) < 0
    # return crossovers.index[crossovers].tolist()

# def moving_averages(data):


# def kde_h(data, h):
    

if __name__ == "__main__":
    main()