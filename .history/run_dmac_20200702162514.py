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
    tickers = 'TSLA SPY'
    data = yf.download(tickers, period='max', group_by='ticker')
    dirty = pd.DataFrame(data['TSLA'])
    #Currently using only closing prices
    frame = clean_data(dirty)['Close']

    periods = optimize(frame)
    print(periods)


if __name__ == "__main__":
    main(_