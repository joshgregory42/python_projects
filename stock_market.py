'''
Written by Josh Gregory
Last edited: 19 December 2022, Windows 11, Python 3.10

Investment rules:
* Want to find companies that are undervalued relative to the market.
* Want to allow the user to specify a market/industry to measure everything relative to (i.e. )

'''

import yfinance as yf

# Function to compare the market and the stock, both as given by the user.
def market_stock_comp(market_name, stock_name, start_date, end_date):
    market = yf.Ticker(market_name)
    stock = yf.Ticker(stock_name)


    # Get history for the market and stock over the same time frame
    market_hist = market.history(start=start_date, end=end_date)
    stock_hist = stock.history(start=start_date, end=end_date)

    

