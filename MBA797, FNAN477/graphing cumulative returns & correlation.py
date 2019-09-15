import pandas as pd
import numpy as np
from tiingo import TiingoClient #pip install tiingo
import matplotlib.pyplot as plt

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

API_KEY = "your api key here"
config = {}
config['api_key'] = API_KEY
SMIF_tickers = ["GOOG","AMZN","BBT","BA","BMY","CBRE","CSCO","C","STZ","CVA","D","XLE","ESS","FTNT","GS","HCP","XLV","HON","JPM","KSU","LEN","MSFT","NEE","PYPL","PFE","PNC","RTN","SYF","TJX","UNH","VZ","WMT","DIS","WDC"]
SPY = ['SPY']
XLV = ['XLV']

client = TiingoClient(config)

start_date = '2018-09-01'
end_date = '2019-09-01'

#download historical data from tiingo and assign variables to cumulative returns for SMIF stocks
#helpful guide: https://ntguardian.wordpress.com/2018/07/17/stock-data-analysis-python-v2/

SMIF_df = client.get_dataframe(SMIF_tickers+SPY,
                                      metric_name='adjClose',
                                      startDate=start_date,
                                      endDate=end_date)
SMIF_df = SMIF_df.dropna()

SMIF_CumReturns = SMIF_df.apply(lambda x: x/ x[0])-1
SMIF_CumReturns = SMIF_CumReturns.dropna()


#for plotting cumulative returns
for i in range (0, len(SMIF_tickers)):
    x = SMIF_CumReturns.index
    plt.plot(x,SMIF_CumReturns['SPY'],label='SPY')
    plt.plot(x,SMIF_CumReturns[SMIF_tickers[i]],label=str(SMIF_tickers[i]))
    plt.xlabel('Time')
    plt.ylabel('Cumulative Percent Return')
    plt.grid(True)
    plt.title("SPY vs "+SMIF_tickers[i])
    plt.axhline(y = 0, color = "black", lw = 2)
    plt.legend(["SPY",SMIF_tickers[i]], title="Correlation: "+str(smcorr[i])[:4])
    plt.savefig(filepath+'Cumulative Correlation\\'+SMIF_tickers[i]+' Timeseries - Cumulative Correlation.png')
    plt.close()
