import yfinance as yf
import numpy as np
from scipy.stats import norm
import pandas as pd
from pandasgui import show
import cvxpy as cp

def main():
    tickers = 'SPY AAPL MRNA TSLA'
    data = yf.download(tickers, period='max', group_by='ticker')
    dirty = pd.DataFrame(data['TSLA'])
    frame = clean_data(dirty)
    sma = frame.rolling(10).mean()
    lma = frame.rolling(30).mean()
    crossovers = calc_crossovers(sma, lma)
    show(dirty, frame)

def clean_data(data):
    incomplete_idxs = False
    for col in data.columns:
        incomplete_idxs |= np.isnan(data[col])
    return data[~incomplete_idxs]

def calc_crossovers(sma, lma):
    num_points = len(clean_data(lma))
    #Currently using only closing prices
    sma = sma['Close']
    lma = lma['Close']
    high = (sma > lma)[-num_points:]
    crossovers = high.astype(int).diff()
    crossovers = crossovers[crossovers != 0]
    show(sma, lma, high, crossovers)

def profit(data, crossovers):
    total = 0
    if crossovers[0] == -1:
        total += data[crossovers.index[0]] - data[0]
    for i in range(1,len(crossovers)):
        left_bound = crossovers.index[i-1]
        if crossovers[left_bound] == 1:
            right_bound = crossovers.index[i]
            total += data[right_bound] - data[left_bound]
    if crossovers[-1] == 1:
        total += data[-1] - data[crossovers[-1]]


# def moving_averages(data):


# def kde_h(data, h):
    

if __name__ == "__main__":
    main()