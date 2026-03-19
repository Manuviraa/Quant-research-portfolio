# Library to store the different functions I will need for my project portfolio in Quantitative research
import pandas as pd
import numpy as np
import yfinance as yf

def yf_data(ticker, start_date, end_date, interval):
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval, multi_level_index=False)
    return data

def log_returns(data, column):
    """
    Inputs a financial time series and outputs a new column with the computed log returns
    """
    data = np.log(data[column]/data[column].shift(1))
    return data