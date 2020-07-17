import yfinance as yf
import numpy as np
from scipy.stats import norm
import pandas as pd
from pandasgui import show
import cvxpy as cp

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
    crossovers = high.astype(int).diff()[1:]
    return crossovers[crossovers != 0]

def profit(data, crossovers):
    total = 0
    if crossovers.iloc[0] == -1:
        total += data.loc[crossovers.index[0]] - data.iloc[0]
    for i in range(1,len(crossovers)):
        left_bound = crossovers.index[i-1]
        if crossovers.loc[left_bound] == 1:
            right_bound = crossovers.index[i]
            total += data.loc[right_bound] - data.loc[left_bound]
    if crossovers.iloc[-1] == 1:
        total += data.iloc[-1] - data.loc[crossovers.index[-1]]
    return total

def optimize(data):
    short_period = cp.Variable()
    long_period = cp.Variable()
    constraints = [short_period > 1, long_period > 1]
    obj = cp.Maximize(run_analysis(short_period, long_period, data))
    # Form and solve problem.
    prob = cp.Problem(obj, constraints)
    prob.solve()  # Returns the optimal value.
    return (short_period.value, long_period.value, prob.value, prob.status)

def run_analysis(short_period, long_period, data):
    sma = data.rolling(short_period).mean()
    lma = data.rolling(long_period).mean()
    crossovers = calc_crossovers(sma, lma)
    return profit(data['Close'], crossovers)

def main():
    tickers = 'SPY AAPL MRNA TSLA'
    data = yf.download(tickers, period='max', group_by='ticker')
    dirty = pd.DataFrame(data['TSLA'])
    frame = clean_data(dirty)
    
    

if __name__ == "__main__":
    main()