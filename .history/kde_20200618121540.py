import yfinance as yf
import numpy as np
from scipy.stats import norm
import pandas as pd
from pandasgui import show

def main():
    tickers = 'SPY AAPL MRNA'
    data = yf.download(tickers, period='max', group_by='ticker')
    frame = pd.DataFrame(data['SPY'])
    averages = frame.rolling(4).mean()
    show(frame, averages, nonblocking=True)

# def moving_averages(data):


# def kde_h(data, h):
    

if __name__ == "__main__":
    main()