import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

'''
Written by Josh Gregory
Last edited: 19 December 2022, Windows 11, Python 3.10
Takes in a list of stock tickers and computes only percent change relative to market
Source: https://www.kaggle.com/code/asimislam/stock-performance-with-yahoo-finance-yfinance
'''

# Reading in all of the tickers (reading in the entire S&P500)
sp_500 = pd.read_csv('sp_500.csv')

ticker = sp_500.Symbol.tolist()

# Set market indexes to compare equities with

market_index = ['^DJI', '^IXIC', '^GSPC']  # Dow Jones, Nasdaq and S&P500

#  Time period and interval
yf_period   = "10y"   # 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
yf_interval = "1d"    # 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo


def main(tickers, market_index, yf_period, yf_interval):
    symbol_calc = symbols(market_index=market_index, ticker=tickers)

    fin_info_calc = fin_info(symbols=symbol_calc)

    pct_calc = pct_return(symbols=symbol_calc, yf_period=yf_period, yf_interval=yf_interval)

    clean_returns = clean_return(pct_calc)

    perf_yr, perf_mh, perf_wk, perf_dy = perf_anal(yf_returns=clean_returns)

    # plot performance for the past 10 years:
    plotPerformance(perf_yr.tail(10))  # past 10 years


    # plot performance for the past 24 months:
    plotPerformance(perf_mh.tail(24))  # past 24 months

    # plot performance for the past 26 weeks (6 months)
    plotPerformance(perf_wk.tail(26))  # past 26 weeks

    # plot the daily performance for the past 31 days (1 month) 
    plotPerformance(perf_dy.tail(31))  # past 31 days

    return print("\n\n\nProgram executed")



# Function to get all of the symbols given the market indexes and the tickers
def symbols(market_index, ticker):
    #  1.  uppercase and sort ticker
    ticker = [x.upper() for x in ticker]
    ticker.sort()

    #  2.  remove markets from ticker for plots, returns
    for market in market_index:
        if market in ticker:
            ticker.remove(market)

    #  3.  symbols = market_indexes + ticker
    symbols = []   # initialize list
    symbols = ticker + market_index

    return symbols

# Function to get the financial info of each of the equities
def fin_info(symbols):
    #  set parameters to download
    fin_info = ["shortName", "sector", "industry", "quoteType", "exchange", "totalAssets",
                "marketCap", "beta", "trailingPE", "volume", "averageVolume", "fiftyTwoWeekLow", 
                "fiftyTwoWeekHigh", "dividendRate", "phone"]

    #  Create DataFrame
    yf_info = pd.DataFrame(index = fin_info, columns = symbols)

    for i in symbols:
        l = []             # initialize
        x = yf.Ticker(i)   # get ticker info
        for j in fin_info:
            if 'date' in j.lower():
                d = pd.to_datetime(x.info[j])
                if d is not None:
                    l.append(d.strftime("%Y-%m-%d"))  # format date
            else:
                try:      # some parameters error
                    l.append(x.info[j])
                except:   # ignore error and continue
                    l.append("")
        yf_info[i] = l
        print('{}\t- financial information downloaded'.format(i))

    return yf_info


def pct_return(symbols, yf_period, yf_interval):
    #  1.  Create DataFrame yf_price with yf.download
    yf_returns = yf.download(
            tickers = symbols,       # tickers list or string as well
            period = yf_period,      # optional, default is '1mo'
            interval = yf_interval,  # fetch data by interval
            group_by = 'ticker',     # group by ticker
            auto_adjust = True,      # adjust all OHLC (open-high-low-close)
            prepost = True,          # download market hours data
            threads = True,          # threads for mass downloading
            proxy = None)            # proxy


    #  2.  Select 'Close' (price at market close) column only
    yf_returns = yf_returns.iloc[:, yf_returns.columns.get_level_values(1)=='Close']


    #  3.  Remove the DataFrame multi-index
    yf_returns.columns = yf_returns.columns.droplevel(1)  # multi-index

    #  4.  calculate percentage changes with "pct_change()"
    #  multiply by 100 to get percentage value
    #  round off the percentages to 2 decimal points
    yf_returns = round(yf_returns.pct_change()*100, 2)

    return yf_returns

# Clean up the yf_return DataFrame
def clean_return(yf_returns):
    #  1. re-order columns
    col_order = []

    for i in market_index:
        col_order.append(i)  # add markets

    for i in ticker:
        col_order.append(i)  # add tickers

    yf_returns = yf_returns[col_order]   # reorder columns


    #  2. rename market index columns
    yf_returns.rename(columns = {'^DJI':'DowJones', '^GSPC':'S&P500', '^IXIC':'Nasdaq'}, inplace = True)


    #  3. update 'market_index' with market names
    market_index = sorted(['DowJones', 'S&P500', 'Nasdaq'])


    #  4. update `symbols` list with market names
    symbols[symbols.index('^DJI')]  = 'DowJones'
    symbols[symbols.index('^GSPC')] = 'S&P500'
    symbols[symbols.index('^IXIC')] = 'Nasdaq'

    return yf_returns

# Create performance DataFrames
def perf_anal(yf_returns):

    #  create YEAR, MONTH, WEEK columns in perf_dy
    perf_dy = yf_returns
    perf_dy['YEAR']  = perf_dy.index.strftime("%Y")     # YEAR
    perf_dy['MONTH'] = perf_dy.index.strftime("%Y-%m")  # YEAR-MONTH
    perf_dy['WEEK']  = perf_dy.index.strftime("%Y-%U")  # YEAR-WEEK


    #  create time dataframes using GROUPBY
    perf_yr = perf_dy.groupby('YEAR').sum()
    perf_mh = perf_dy.groupby('MONTH').sum()
    perf_wk = perf_dy.groupby('WEEK').sum()
    
    return perf_yr, perf_mh, perf_wk, perf_dy

# Create function to plot the performance
def plotPerformance(arg):
    df = arg
    
    plt.figure(figsize=(10,8))

    #  subplot #1
    plt.subplot(221)
    df[market_index].boxplot()
    plt.title('market indexes')
    plt.ylabel('percent change')
    plt.xticks(rotation = 90)
    plt.grid(False)

    #  subplot #2
    plt.subplot(222)
    plt.plot(df[market_index])
    plt.title('market indexes')
    plt.legend(df[market_index], loc="upper left", bbox_to_anchor=(1,1))
    plt.xticks(rotation = 90)
    
    plt.show()  # plot subplots
    
    #  plot #3
    plt.figure(figsize=(10,6))
    df[ticker].boxplot()
    plt.title('SYMBOLS', fontsize = 14)
    plt.ylabel('percent change', fontsize = 14)
    plt.xticks(rotation = 90)
    plt.grid(False)
    plt.show()
    
    #  plot #4
    plt.figure(figsize=(10,6))
    plt.plot(df[ticker])
    plt.title('SYMBOLS', fontsize = 14)
    plt.ylabel('percent change', fontsize = 14)
    plt.legend(df[ticker], loc="upper left", bbox_to_anchor=(1,1))
    plt.xticks(rotation = 90)
    plt.show()
    

    #  print returns
    print('\nRETURNS FROM {} TO {}:'.format(df.index[0], df.index[-1]))
    for i in market_index + ticker:
        print('{:>10}{:>10.2f}%'.format(i,df[i].sum()))

    return
'''
plot performance for the past 10 years:
plotPerformance(perf_yr.tail(10))  # past 10 years


plot performance for the past 24 months:
plotPerformance(perf_mh.tail(24))  # past 24 months

plot performance for the past 26 weeks (6 months)
plotPerformance(perf_wk.tail(26))  # past 26 weeks

plot the daily performance for the past 31 days (1 month) 
plotPerformance(perf_dy.tail(31))  # past 31 days
'''

main(tickers=ticker, market_index=market_index, yf_period=yf_period, yf_interval=yf_interval)
