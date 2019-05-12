import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import skewnorm
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

filepath = "[FILEPATH]"
filename = "ETFs.xlsx"
sheetname = "Sheet1"

excelfile = filepath+filename
destpath = "[FILEPATH]"
etfs = ["XLB Material","XLE Energy","XLF Financials","XLI Industrials","XLK Technology","XLV Healthcare","XLP Consumer Staples","XLY Consumer Discretionary","IYZ Telecommunications","Risk free Rate"]
shortetfs = ["XLB","XLE","XLF","XLI","XLK","XLV","XLP","XLY","IYZ","Rfr"]


#data import of raw monthly total return index from Bloomberg and cleaning
df = pd.read_excel(excelfile, sheet_name = sheetname, usecols="A:J", skiprows=0, nrows=102)
df = df.set_index('Date')
df.columns = etfs[0:9]
df = df.dropna()
df.tail()

#shifting and finding monthly return percentages
df1=df/df.shift(-1)-1
df1 = df1.dropna()
print(df1.tail(2))
df1.describe(percentiles=[.25, .5, .75,.95,.10,.99])

#for plotting time series % returns
for i in range (0, len(etfs)-1):
    plt.ylim(-.20,.20)
    plt.xlabel('Time')
    plt.ylabel('Monthly Returns')
    plt.title(etfs[i])
    plt.grid(True)

    x = df1.index
    y1 = df1[etfs[i]]
    
    plt.plot(x, y1)
    
    plt.savefig(filepath+'plots\\'+etfs[i]+' Timeseries.png')
    plt.close()

#for plotting all frequency histograms on one chart
for i in range(0, len(etfs)-1):
    plt.hist(df1[etfs[i]], bins=15)
    plt.xlabel('Monthly Returns')
    plt.ylabel('Frequency')
    plt.title("All ETFs Histogram")
    plt.grid(True)
    plt.savefig(filepath+'All ETFS Histogram.png')

#for plotting frequency histograms on individual charts with normal distribution overlay

for i in range (0, len(etfs)-1):
    data = df1[etfs[i]].sort_values()
    plt.grid(True)
    plt.hist(data, 15, alpha=1, density=True)
    
    mean = data.mean()
    sigma = data.std()
    a = data.skew()

    plt.ylim(0,17)
    plt.xlim(-.2,.2)
    plt.xlabel('Monthly Returns')
    plt.ylabel('Frequency')
    plt.title(etfs[i])

    
    x = np.linspace(-.2,.2)

    pdf = norm.pdf(x, mean, sigma)
    
    plt.plot(x, pdf)
    
    plt.savefig(filepath+'plots\\'+etfs[i]+' Histogram.png')
    plt.close()

#for plotting individual ETFs by Sharpe ratio

for i in range (0, len(etfs)-1):
    plt.scatter(df1[etfs[i]].std() , df1[etfs[i]].mean())
    plt.xlabel('σ of Monthly Returns')
    plt.ylabel('µ of Monthly Returns')
    plt.grid(True)

    plt.annotate(shortetfs[i],(float(df1[etfs[i]].std())+.0005,  float(df1[etfs[i]].mean())+.0005))
    plt.title('Return vs. Risk')
    plt.ylim(0,.017)
    plt.xlim(.0,.06)
plt.rcParams["figure.figsize"] = [16,9]
plt.savefig(filepath+'plots\\'+'all etf scatter')
plt.close()

#for plotting indifference curves on top of individual ETFs by Sharpe ratio
for i in range (0, len(etfs)-1):
    
    plt.scatter(df1[etfs[i]].std() , df1[etfs[i]].mean())
    plt.xlabel('σ of Monthly Returns')
    plt.ylabel('µ of Monthly Returns')
    plt.grid(True)

    plt.annotate(shortetfs[i],(float(df1[etfs[i]].std())+.0005,  float(df1[etfs[i]].mean())+.0005))
    plt.title('Return vs. Risk')
    plt.ylim(0,.017)
    plt.xlim(.0,.06)


x = np.linspace(0.0,.06,1000)
y6 = 0.00917 + .5*6*x**2
A6 = plt.plot(x, y6, label="IC A=6")

y3 = 0.01115 + .5*3*x**2
A3 = plt.plot(x, y3, label="IC A=3")

y1 = 0.01268 + .5*1*x**2
A1 = plt.plot(x, y1, label="IC A=1")

plt.legend(loc='lower left')

plt.rcParams["figure.figsize"] = [16,9]
plt.savefig(filepath+'plots\\'+'all etf scatter with indifference')
plt.close()

