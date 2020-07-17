import yfinance as yf
import numpy as np
from scipy.stats import norm
import pandas as pd
from pandasgui import show

def main():
    tickers = 'SPY AAPL MRNA'
    data = yf.download(tickers, period='max', group_by='ticker')
    frame = pd.DataFrame(data['SPY'])
    averages = frame.rolling(4).mean()
    show(clean_data(frame))

def clean_data(data):
    data = data[~(np.isnan(data['Open']) or 
    np.isnan(data['High']) or 
    np.isnan(data['Low']) or 
    np.isnan(data['Close']) or 
    np.isnan(data['Adj Close']) or 
    np.isnan(data['Volume']))]
    return data

# def moving_averages(data):


# def kde_h(data, h):
    

if __name__ == "__main__":
    main()