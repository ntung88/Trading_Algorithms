import yfinance as yf
import numpy as np
import pandas as pd
from pandasgui import show
from scipy.optimize import minimize
import matplotlib.pyplot as plt

'''
A library for running Dual Moving Average Crossover trading strategy, with backtesting, 
period optimization, and vizualization tools.
'''
#Period of time (in years) that we look back when optimizing in return calculation
HINDSIGHT = 2

def clean_data(data):
    ''' 
    Removes row (days) with no data from dataframe or series 
    '''
    incomplete_idxs = False
    if isinstance(data, pd.DataFrame):
        for col in data.columns:
            incomplete_idxs |= np.isnan(data[col])
    else:
        incomplete_idxs |= np.isnan(data)
    return data[~incomplete_idxs]

def calc_crossovers(sma, lma):
    ''' 
    Returns a dataframe containing only the rows where a crossover of the sma and lma
    is detected. 1 indicates a buy point (sma moving above lma), -1 a sell point
    '''
    num_points = len(clean_data(lma))
    high = (sma > lma)[-num_points:]
    print(high)
    crossovers = high.astype(int).diff()[1:]
    print(crossovers)
    trimmed = crossovers[crossovers != 0]
    print(trimmed)
    return trimmed

def profit(data, crossovers):
    '''
    Calculates profit assuming data covers a continuous time period with the given crossovers
    '''
    if len(crossovers) == 0:
        return 0
    total = 0
    # If first crossover is a sell point assume implicit buy point at very start of data
    print(crossovers.iloc[0])
    if crossovers.iloc[0] == -1:
        total += data.loc[crossovers.index[0]] - data.iloc[0]
    # Add the difference between value at sell points and value at buy points to our profit
    for i in range(1,len(crossovers)):
        left_bound = crossovers.index[i-1]
        if crossovers.loc[left_bound] == 1:
            right_bound = crossovers.index[i]
            total += data.loc[right_bound] - data.loc[left_bound]
    # If last crossover is a buy point assume implicit sell point at end of data (include 
    # profit we have made on current holding)
    if crossovers.iloc[-1] == 1:
        total += data.iloc[-1] - data.loc[crossovers.index[-1]]
    return total

def optimize(data):
    '''
    Uses scipy's convex minimization library to find optimal short period and long period
    for moving averages. Because the profit certainly isn't a truly convex function I use a
    wide range of seeds as initial guesses in hopes of detecting all the local minimums
    and comparing them to get a good guess of the global min
    '''
    cons = ({'type': 'ineq', 'fun': lambda x: x[1] - x[0]},
    {'type': 'ineq', 'fun': lambda x: x[0] - 5})

    # Ranges of initial guesses for short and long periods
    #30 and 40 step size for max accuracy, larger for faster runtime
    short_seeds = range(5, 300, 50)
    long_seeds = range(20, 800, 70)
    # short_seeds = [100]
    # long_seeds = [750]
    minimum = float('inf')
    best_short = 0
    best_long = 0
    for short_seed in short_seeds:
        for long_seed in long_seeds:
            # Use all combinations of ranges where long_seed > short_seed as initial guesses
            if long_seed > short_seed:
                res = minimize(run_analysis, [short_seed, long_seed], args=(data,), method='COBYLA', constraints=cons, options={'rhobeg': 10.0, 'catol': 0.0})
                if res.fun < minimum:
                    best_short = res.x[0]
                    best_long = res.x[1]
                    minimum = res.fun
    return (int(round(best_short)), int(round(best_long)), minimum)

def run_analysis(periods, data):
    '''
    Objective function for minimization, runs profit calculation with given periods and data
    Returns negative profit for minimization (maximization of profit)
    '''
    short_period = int(round(periods[0]))
    long_period = int(round(periods[1]))
    sma = data.rolling(short_period).mean()
    lma = data.rolling(long_period).mean()
    print(sma, lma)
    crossovers = calc_crossovers(sma, lma)
    return -1 * profit(data, crossovers)

def visualize(data, short_period, long_period):
    '''
    Useful for visualizing the algorithm's decisions. Plots the stock price with colored
    vertical bars at buy and sell points
    '''
    sma = data.rolling(short_period).mean()
    lma = data.rolling(long_period).mean()
    crossovers = calc_crossovers(sma, lma)
    buys = pd.DataFrame(crossovers[crossovers == 1.0])
    sells = pd.DataFrame(crossovers[crossovers == -1.0])
    data.plot(color='black')
    for buy in buys.index:
        plt.axvline(buy, color="green")
    for sell in sells.index:
        plt.axvline(sell, color="red")
    plt.show()

def split_year(data):
    '''
    Split dataframe into a list of dataframes, each corresponding to the data for each year
    '''
    years = np.unique(data.index.year)
    split = []
    for year in years:
        split.append(data[data.index.year == year])
    return split

def calc_returns(split_data):
    '''
    Calculate annual returns for periods optimized over slices (of size HINDSIGHT) of past data. Gives an idea of what kind of results to realistically expect
    '''
    annual_returns = []
    max_return = float('-inf')
    min_return = float('inf')
    for i in range(2, len(split_data)):
        test_year = split_data[i]
        optimize_period = pd.DataFrame(np.concatenate(split_data[i-HINDSIGHT:i]))
        print('optimize period:')
        print(optimize_period)
        periods = optimize(optimize_period)
        print('periods:')
        print(periods)
        profit = run_analysis(periods, test_year)
        annual_returns.append(profit)
        if profit > max_return: max_return = profit
        if profit < min_return: min_return = profit
    return annual_returns, max_return, min_return

def main():
    '''
    Main's current functionality: Find optimal windows for TSLA and print them, along with profit since 6/29/2010
    '''
    ticker = yf.Ticker('MRNA')
    # data = yf.download(tickers, period='max', group_by='ticker')
    data = ticker.history(period="max")[:-4]
    dirty = pd.DataFrame(data)
    #Currently using only closing prices
    frame = clean_data(dirty)['Close']
    # periods = optimize(frame)
    # short = frame.rolling(periods[0]).mean()[-1]
    # long = frame.rolling(periods[1]).mean()[-2]
    # print('short ' + str(short) + 'long ' + str(long))
    periods = calc_returns(split_year(frame))
    print(periods)



    # visualize(frame, periods[0], periods[1])

if __name__ == "__main__":
    main()

'''
how to quantify number of shares you want to buy (steepness of trend, volatility, top 20 stocks?)
'''