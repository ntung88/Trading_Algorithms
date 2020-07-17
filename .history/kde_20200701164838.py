import yfinance as yf
import numpy as np
from scipy.stats import norm
import pandas as pd
from pandasgui import show
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def epanechnikov(x):
    if abs(x) < 1:
        return 3/4 * (1 - x ** 2)
    return 0

def main():
    pass

if __name__ == "__main__":
    main()