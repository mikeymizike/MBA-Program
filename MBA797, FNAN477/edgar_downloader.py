#this script downloads 10-K and 10-Q reports for specified tickers from EDGAR using the sec_edgar_downloader package 
#and renames them so they resolve correctly as html files.
import sec_edgar_downloader,os
from sec_edgar_downloader import Downloader

basepath = 'C:\\Users\\Dell\\OneDrive - George Mason University\\MBA 797\\Stock Data\\'
SMIF_health_tickers = ['BMY', 'PFE','UNH','CNC']

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
