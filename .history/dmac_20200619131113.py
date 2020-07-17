import yfinance as yf
import numpy as np
from scipy.stats import norm
import pandas as pd
from pandasgui import show

def main():
    tickers = 'SPY AAPL MRNA'
    data = yf.download(tickers, period='max', group_by='ticker')
    frame = clean_data(pd.DataFrame(data['SPY']))
    sma = frame.rolling(100).mean()
    lma = frame.rolling(750).mean()
    show(sma, lma)

def clean_data(data):
    data = data[~(np.isnan(data['Open']) | 
    np.isnan(data['High']) |
    np.isnan(data['Low']) |
    np.isnan(data['Close']) |
    np.isnan(data['Adj Close']) |
    np.isnan(data['Volume']))]
    return data

# def moving_averages(data):


# def kde_h(data, h):
    

if __name__ == "__main__":
    main()