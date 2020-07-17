import yfinance as yf
import numpy as np
from scipy.stats import norm
import pandas as pd
from pandasgui import show
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def nw_volatility(x, data):
    '''
    Nadaraya-Watson conditional volatility estimator using the optimal bandwitch kernel (epanechnikov)
    '''
    xs = data.index
    ys = data['Close']

    num = 0
    denom = 0
    for i in range(len(data)):
        epsilon_term = (ys[i] - nw_mean(xs[i], data)) ** 2
        kernel_term = epanechnikov(xs[i] - x)
        num += kernel_term * epsilon_term
        denom += kernel_term
    return num / denom

def nw_mean(x, data):
    '''
    Nadaraya-Watson conditional mean estimator using the optimal bandwitch kernel (epanechnikov)
    '''
    xs = data.index
    ys = data['Close']

    num = 0
    denom = 0
    for i in range(len(data)):
        kernel_term = epanechnikov(xs[i] - x)
        num += kernel_term * ys[i]
        denom += kernel_term
    return num / denom

def epanechnikov(x):
    '''
    The Epanechnikov kernel, corresponding to optimal bandwith according to paper
    '''
    if abs(x) < 1:
        return 3/4 * (1 - x ** 2)
    return 0

def main():
    pass

if __name__ == "__main__":
    main()