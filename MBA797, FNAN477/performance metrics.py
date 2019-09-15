import pandas as pd
import numpy as np
from tiingo import TiingoClient
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

#download historical data from tiingo and assign variables to daily percent returns and annualized percent returns
#for SMIF stocks
#helpful guide: https://ntguardian.wordpress.com/2018/07/17/stock-data-analysis-python-v2/

SMIF_df = client.get_dataframe(SMIF_tickers+SPY,
                                      metric_name='adjClose',
                                      startDate=start_date,
                                      endDate=end_date)
SMIF_df = SMIF_df.dropna()

SMIF_dailypctRet = SMIF_df.pct_change()
SMIF_dailypctRet = SMIF_dailypctRet.dropna()
SMIF_apr = SMIF_dailypctRet * 252 * 100

smcorr = SMIF_apr.drop("SPY", 1).corrwith(SMIF_apr.SPY)
#print(smcorr)

#Three month t-bill 09/03/19 
#https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/textview.aspx?data=yield
rrf = 1.98

sy = SMIF_apr.drop("SPY",1).std()
sx = SMIF_apr.SPY.std()

ybar = SMIF_apr.drop("SPY",1).mean()
xbar = SMIF_apr.SPY.mean()

beta = smcorr * sy / sx
alpha = ybar - beta * xbar
sharpe = (ybar - rrf)/sy
treynor = (ybar-rrf)/beta 
