'''
Written by Josh Gregory
Last edited: 19 December 2022, Windows 11, Python 3.10
'''

import yfinance as yf

# Function to compare the market and the stock, both as given by the user.
def market_stock_comp(market_name, stock_name):
    market = yf.Ticker(market_name)
    stock = yf.Ticker(stock_name)
