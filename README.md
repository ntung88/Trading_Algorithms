# Trading_Algorithms
A collection of trading strategies implemented in Python

- dmac.py implements the Dual Moving Average Crossover strategy, which buys shares when the Short Moving Average moves above the Long Moving Average,
and sells when the reverse happens. dmac.py includes methods for optimizing the short and long window (in number of days) based on past data, profit
calculation, and vizualization to see decisions the algorithm is making. Background information from a Duke Paper on DMAC (DMAC.pdf)

- kde.py will implement kernel regression/density estimation to predict future stock prices

Results:

dmac.py:
Achieves very high profits on past data, but this is obviously not very indicative of future profits. Short and long window sizes are chosen as those that maximize profit over all available data (if the strategy were in use since the beginning of the data with the optimal parameters). 

For example, I have a calculated profit of $1287.42 per share of TSLA since 6/29/2010 using the optimal windows I found (10 days for short and 20 days for long). These optimal windows were calculated using the data since 6/29/2010, so they were found with "future" knowledge that we wouldn't have realistically had back in June of 2010. 

I am testing out some other ways of optimizing these windows (maybe taking slices of past data and testing on the rest, like a train-test split/cross validation, or intelligently choosing a slice to optimize over based on metrics like volatility or total stock price) as I'm not convinced using the entirety of past data is the best thing.
