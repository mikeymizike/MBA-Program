import pandas as pd
from tiingo import TiingoClient
import matplotlib.pyplot as plt

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

API_KEY = "your api key here"
config = {}
config['api_key'] = API_KEY
SMIF_health_tickers = ['BMY','PFE','UNH']
SPY = ['SPY']
XLV = ['XLV']

client = TiingoClient(config)

start_date = '2018-09-01'
end_date = '2019-09-01'

#download historical data and assign variables to daily returns, daily percent returns and 1 index returns 
#for SMIF health care stocks
#helpful guide: https://ntguardian.wordpress.com/2018/07/17/stock-data-analysis-python-v2/

SMIF_health_df = client.get_dataframe(SMIF_health_tickers+SPY+XLV,
                                      metric_name='adjClose',
                                      startDate=start_date,
                                      endDate=end_date)
SMIF_health_df = SMIF_health_df.dropna()

SMIF_health_dailypctRet=SMIF_health_df/SMIF_health_df.shift(-1)-1
SMIF_health_dailypctRet = SMIF_health_dailypctRet.dropna()

SMIF_health_returns = SMIF_health_df.apply(lambda x: x/ x[0])

print(SMIF_health_dailypctRet.tail())
smcorr = SMIF_health_dailypctRet.drop("SPY", 1).corrwith(SMIF_health_dailypctRet.SPY)
print(smcorr)

#Graph specified ticker returns against another
x = SMIF_health_returns.index
plt.plot(x,SMIF_health_returns['XLV'],label='XLV')
plt.plot(x,SMIF_health_returns['SPY'],label='SPY')
plt.xlabel('x label')
plt.ylabel('y label')
plt.grid(True)
plt.title("SPY vs XLV")
plt.axhline(y = 1, color = "black", lw = 2)

plt.legend()
