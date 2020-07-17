'''
Script for running dmac on current data. Outputs decision for paper trading since I don't have the resources
to trade electronically :(((
'''
import dmac
import yfinance as yf
import numpy as np
import sys

def main():
    args = sys.argv[1:]
    tickers = ' '.join(args)
    data = yf.download(tickers, period='max', group_by='ticker')
    for ticker in args
        dirty = pd.DataFrame(data[ticker])
        #Currently using only closing prices
        frame = clean_data(dirty)['Close']
        periods = optimize(frame)
        short_window = periods.x[0]
        long_window = periods.x[1]
        current_data = frame[-long_window]
        sma = current_data.rolling(short_window).mean()
        lma = current_data.rolling(long_window).mean()
        crossovers = 



if __name__ == "__main__":
    main(_