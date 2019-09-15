import pandas as pd
import numpy as np
from tiingo import TiingoClient
import matplotlib.pyplot as plt

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
filepath = "C:\\Users\\Dell\\OneDrive - George Mason University\\MBA 797 SMIF\\Plots\\"

API_KEY = "your API key"
config = {}
config['api_key'] = API_KEY
SMIF_tickers = ["GOOG","AMZN","BBT","BA","BMY","CBRE","CSCO","C","STZ","CVA","D","XLE","ESS","FTNT","GS","HCP","XLV","HON","JPM","KSU","LEN","MSFT","NEE","PYPL","PFE","PNC","RTN","SYF","TJX","UNH","VZ","WMT","DIS","WDC"]
SPY = ['SPY']
XLV = ['XLV']

client = TiingoClient(config)

start_date = '2018-09-01'
end_date = '2019-09-01'

#download historical data and assign variables to daily returns, daily percent returns and 1 index returns 
#for ALL SMIF stocks
#helpful guide: https://ntguardian.wordpress.com/2018/07/17/stock-data-analysis-python-v2/

SMIF_df = client.get_dataframe(SMIF_tickers+SPY,
                                      metric_name='adjClose',
                                      startDate=start_date,
                                      endDate=end_date)
SMIF_df = SMIF_df.dropna()

SMIF_dailypctRet= SMIF_df.pct_change()
SMIF_dailypctRet = SMIF_dailypctRet.dropna()
SMIF_apr = SMIF_dailypctRet * 252 *100

#for plotting time series % returns
for i in range (0, len(SMIF_tickers)):
    plt.ylim(-.12,.12)
    plt.xlabel('Time')
    plt.ylabel('Daily Returns')
    plt.title(SMIF_tickers[i])
    plt.grid(True)
    x = SMIF_dailypctRet.index
    y1 = SMIF_dailypctRet[SMIF_tickers[i]]
    plt.plot(x, y1)
    plt.savefig(filepath+'Daily Pct Returns\\'+SMIF_tickers[i]+' Timeseries.png')
    plt.close()
