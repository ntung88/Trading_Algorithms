import yfinance as yf
import numpy as np
from scipy.stats import norm
import pandas as pd
from pandasgui import show
from scipy.optimize import minimize, LinearConstraint
import matplotlib.pyplot as plt

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
    trimmed = crossovers[crossovers != 0]
    return trimmed

def profit(data, crossovers):
    if len(crossovers) == 0:
        return 0
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
    cons = ({'type': 'ineq', 'fun': lambda x: x[1] - x[0]},
    {'type': 'ineq', 'fun': lambda x: x[0] - 5})
     # 'type':'eq', 'fun': lambda x : max([x[i]-int(x[i]) for i in range(len(x))]),

    short_seeds = range(5, 300, 30)
    long_seeds = range(20, 800, 40)
    # short_seeds = [100]
    # long_seeds = [750]
    minimum = float('inf')
    best_short = 0
    best_long = 0
    for short_seed in short_seeds:
        for long_seed in long_seeds:
            if long_seed > short_seed:
                res = minimize(run_analysis, [short_seed, long_seed], args=(data,), method='COBYLA', constraints=cons, options={'rhobeg': 10.0, 'catol': 0.0})
                if res.fun < minimum:
                    best_short = res.x[0]
                    best_long = res.x[1]
                    minimum = res.fun
    return (int(round(best_short)), int(round(best_long)), minimum)

def run_analysis(periods, data):
    # print(periods)
    short_period = int(round(periods[0]))
    long_period = int(round(periods[1]))
    # print(short_period, long_period)
    sma = data.rolling(short_period).mean()
    lma = data.rolling(long_period).mean()
    crossovers = calc_crossovers(sma, lma)
    result = -1 * profit(data['Close'], crossovers)
    # print(short_period, long_period, result)
    return result

def main():
    tickers = 'SPY AAPL MRNA TSLA MMM APA'
    data = yf.download(tickers, period='max', group_by='ticker')
    dirty = pd.DataFrame(data['APA'])
    frame = clean_data(dirty)
    # periods = optimize(frame)
    # visualize(data, periods[0], periods[1])
    visualize(frame, 50, 200)

def visualize(data, short_period, long_period):
    sma = data.rolling(short_period).mean()
    lma = data.rolling(long_period).mean()
    crossovers = calc_crossovers(sma, lma)
    buys = pd.DataFrame(crossovers[crossovers == 1.0])
    sells = pd.DataFrame(crossovers[crossovers == -1.0])
    plot_sells = sells * data['Close']
    # plot_sells[np.isnan(plot_sells)] = 0
    plot_buys = buys * data['Close']
    print(len(plot_sells.index), len(plot_sells['Close']))
    # plot_buys[np.isnan(plot_buys)]
    data.plot(color='black')
    plot_sells.plot(kind='scatter', x=plot_sells.index, y=plot_sells['Close'], color='red')
    plot_buys.plot(kind='scatter', x=plot_buys.index, y='Close', color='green')
    plt.show()

if __name__ == "__main__":
    main()