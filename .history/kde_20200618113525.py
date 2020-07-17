import yfinance as yf
import numpy as np
from scipy.stats import norm

def main():
    tickers = 'SPY AAPL MRNA'
    data = yf.download(tickers, period='max', group_by='ticker')
    print(data['SPY'])

def kde_h(data, h):
    

if __name__ == "__main__":
    main()