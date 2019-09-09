#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
from tiingo import TiingoClient
import matplotlib.pyplot as plt

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

config = {}
config['api_key'] = "c11cafa88f76f02be5ebf0a7828035fe1413a65d"
SMIF_health_tickers = ['BMY', 'MDT', 'PFE','UNH','CNC']
SPY = ['SPY']
XLV = ['XLV']


client = TiingoClient(config)

start_date = '2018-09-01'
end_date = '2019-09-01'


# In[4]:


#download historical data and assign variables to daily returns, daily percent returns and 1 index returns 
#for SMIF health care stocks

SMIF_health_df = client.get_dataframe(SMIF_health_tickers+SPY+XLV,
                                      metric_name='adjClose',
                                      startDate=start_date,
                                      endDate=end_date)
SMIF_health_df = SMIF_health_df.dropna()

SMIF_health_dailypctRet=SMIF_health_df/SMIF_health_df.shift(-1)-1
SMIF_health_dailypctRet = SMIF_health_dailypctRet.dropna()

SMIF_health_returns = SMIF_health_df.apply(lambda x: x/ x[0])


# In[5]:


print(SMIF_health_dailypctRet.tail())
smcorr = SMIF_health_dailypctRet.drop("SPY", 1).corrwith(SMIF_health_dailypctRet.SPY)
print(smcorr)


# In[6]:


x = SMIF_health_returns.index
plt.plot(x,SMIF_health_returns['XLV'],label='XLV')
plt.plot(x,SMIF_health_returns['SPY'],label='SPY')
plt.xlabel('x label')
plt.ylabel('y label')
plt.grid(True)
plt.title("BMY vs XLV")
plt.axhline(y = 1, color = "black", lw = 2)

plt.legend()
#https://ntguardian.wordpress.com/2018/07/17/stock-data-analysis-python-v2/


# In[33]:


SMIF_health_metadata = {}

for i in range (0,len(SMIF_health_tickers)):
    ticker_metadata = client.get_ticker_metadata(SMIF_health_tickers[i])
    SMIF_health_metadata[str(SMIF_health_tickers[i])] = ticker_metadata
SMIF_health_metadata


# In[15]:


from openpyxl import load_workbook
from openpyxl import Workbook
dest_filename = 'C:\\Users\\Dell\\OneDrive - George Mason University\\MBA 797\\MBA 797 Analysis.xlsx'
wb = load_workbook(filename =dest_filename )


# In[17]:


import sec_edgar_downloader,os
from sec_edgar_downloader import Downloader

basepath = 'C:\\Users\\Dell\\OneDrive - George Mason University\\MBA 797\\Stock Data\\'
SMIF_health_tickers = ['BMY', 'MDT', 'PFE','UNH','CNC']

for i in range (0,len(SMIF_health_tickers)):
    dl = Downloader(basepath+SMIF_health_tickers[i])
    dl.get_10k_filings(SMIF_health_tickers[i],5)
    dl.get_10q_filings(SMIF_health_tickers[i],4)

for z in range (0, len(SMIF_health_tickers)):
    filelistK =os.listdir(basepath+SMIF_health_tickers[z]+"\\sec_edgar_filings\\"+SMIF_health_tickers[z]+"\\10-K\\")
    filelistQ =os.listdir(basepath+SMIF_health_tickers[z]+"\\sec_edgar_filings\\"+SMIF_health_tickers[z]+"\\10-Q\\")
    for i in range (0, len(filelistK)):
        os.rename(basepath+SMIF_health_tickers[z]+"\\sec_edgar_filings\\"+SMIF_health_tickers[z]+"\\10-K\\"+filelistK[i], 
              basepath+SMIF_health_tickers[z]+"\\sec_edgar_filings\\"+SMIF_health_tickers[z]+"\\10-K\\"+filelistK[i][:-3]+"html")
    for i in range (0, len(filelistQ)):
        os.rename(basepath+SMIF_health_tickers[z]+"\\sec_edgar_filings\\"+SMIF_health_tickers[z]+"\\10-Q\\"+filelistQ[i], 
              basepath+SMIF_health_tickers[z]+"\\sec_edgar_filings\\"+SMIF_health_tickers[z]+"\\10-Q\\"+filelistQ[i][:-3]+"html")

