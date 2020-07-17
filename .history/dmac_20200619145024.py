import yfinance as yf
import numpy as np
from scipy.stats import norm
import pandas as pd
from pandasgui import show

def main():
    tickers = 'SPY AAPL MRNA TSLA'
    data = yf.download(tickers, period='max', group_by='ticker')
    dirty = pd.DataFrame(data['TSLA'])
    frame = clean_data(dirty)
    sma = frame.rolling(100).mean()
    lma = frame.rolling(750).mean()
    crossovers = calc_crossovers(sma, lma)
    show(dirty, frame)

def clean_data(data):
    incomplete_idxs = False
    for col in data.columns:
        incomplete_idxs |= np.isnan(data[col])
    return data[~incomplete_idxs]

def calc_crossovers(sma, lma):
    #Currently using only closing prices
    sma = clean_data(sma['Close'])
    lma = clean_data(lma['Close'])
    #sma corresponds to 0
    show(sma, lma, sma > lma)
    # higher = lma
    # crossovers = (sma['Low'] - lma['Low']) * (sma['High'] - lma['High']) < 0
    # return crossovers.index[crossovers].tolist()

# def moving_averages(data):


# def kde_h(data, h):
    

if __name__ == "__main__":
    main()