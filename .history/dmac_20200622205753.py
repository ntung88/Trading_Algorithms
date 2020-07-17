import yfinance as yf
import numpy as np
from scipy.stats import norm
import pandas as pd
from pandasgui import show
from scipy.optimize import minimize, LinearConstraint

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
    # short_period = cp.Variable(integer=True, nonneg=True)
    # long_period = cp.Variable(integer=True, nonneg=True)
    # constraints = [short_period >= 1, long_period >= short_period]
    # obj = cp.Maximize(run_analysis(short_period, long_period, data))
    # # Form and solve problem.
    # prob = cp.Problem(obj, constraints)
    # prob.solve()  # Returns the optimal value.
    # return (short_period.value, long_period.value, prob.value, prob.status)

    cons = {'type': 'ineq', 'fun': lambda x: x[1] - x[0],
    'type':'eq', 'fun': lambda x : max([x[i]-int(x[i]) for i in range(len(x))]),
    'type': 'ineq', 'fun': lambda x: x[0] - 1}

    short_seeds = range(0, 200, 60)
    long_seeds = range(0, 800, 100)
    minimum = float('inf')
    best_short = 0
    best_long = 0
    for short_seed in short_seeds:
        for long_seed in long_seeds:
            if long_seed > short_seed:
                res = minimize(run_analysis, [short_seed, long_seed], args=data, method='COBYLA', constraints=cons, options={'rhobeg': 10.0})
                if res.fun < minimum:
                    best_short = res.x[0]
                    best_long = res.x[1]
                    minimum = res.fun
    return (best_short, best_long, minimum)

def run_analysis(periods, data):
    short_period = int(round(periods[0]))
    long_period = int(round(periods[1]))
    sma = data.rolling(short_period).mean()
    lma = data.rolling(long_period).mean()
    crossovers = calc_crossovers(sma, lma)
    result = -1 * profit(data['Close'], crossovers)
    # print(short_period, long_period, result)
    return result

def main():
    tickers = 'SPY AAPL MRNA TSLA'
    data = yf.download(tickers, period='max', group_by='ticker')
    dirty = pd.DataFrame(data['TSLA'])
    frame = clean_data(dirty)
    print(optimize(frame))
    
    

if __name__ == "__main__":
    main()