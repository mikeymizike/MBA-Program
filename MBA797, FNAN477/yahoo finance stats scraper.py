tickers = ["ABT","TSLA"]
def getstats(tickers):
    import requests, re, time, random
    from bs4 import BeautifulSoup as bs4
    import pandas as pd
    PS_ratios = {}
    PB_ratios = {}
    EV_revenue_ratios = {}
    PEG_ratios = {}
    trailing_PE_ratios = {}
    betas = {}
    fwd_PE_ratios = {}
    short_ratios = {}
    
    for i in range(0,len(tickers)):
        site = requests.get("https://finance.yahoo.com/quote/"+tickers[i]+"/key-statistics?p="+tickers[i]).text
        soup = bs4(site)
        stats = soup.find("div", { "id" : "mrt-node-Col1-3-KeyStatistics" }).text

        try:
            PS_ratio = re.search(r'Price/Sales \(ttm\)(\d+)\.(\d+)',stats).group(0)[len("Price/Sales (ttm)"):]
        except:
            PS_ratio = "NaN"

        try:
            PB_ratio = re.search(r'Price/Book \(mrq\)(\d+)\.(\d+)',stats).group(0)[len("Price/Book (mrq)"):]
        except:
            PB_ratio = "NaN"

        try:
            EV_revenue_ratio = re.search(r'Enterprise Value/Revenue 3(\d+)\.(\d+)',stats).group(0)[len("Enterprise Value/Revenue 3"):]
        except:
            EV_revenue_ratio = "NaN"

        try:
            PEG_ratio = re.search(r'PEG Ratio \(5 yr expected\) 1(\d+)\.(\d+)', stats).group(0)[len("PEG Ratio (5 yr expected) 1"):]
        except:
            PEG_ratio = "NaN"

        try:
            trailing_PE_ratio = re.search(r'Trailing P/E (\d+)\.(\d+)', stats).group(0)[len('Trailing P/E '):]
        except:
            trailing_PE_ratio = "NaN"

        try:
            fwd_PE_ratio = re.search(r'Forward P/E 1(\d+)\.(\d+)', stats).group(0)[len('Forward P/E 1'):]
        except:
            fwd_PE_ratio = "NaN"
        #attempts to grab beta from the stock but some betas are 3Y betas and some are 5Y. Need to write a function to
        #make either work.
        try:
            beta = re.search(r'Beta \(5Y Monthly\) (\d+)\.\d\d', stats).group(0)[len('Beta (5Y Monthly) '):]
        except:
            beta = "NaN"

        try:
            short_ratio_search = re.search(r'Short Ratio \((.*?)\) 4(\d+)\.(\d+)', stats).group(0)
            short_ratio_len = re.search(r'Short Ratio \((.*?)\) 4', stats).group(0)
            short_ratio = re.search(r'Short Ratio \((.*?)\) 4(\d+)\.(\d+)', stats).group(0)[len(short_ratio_len):]
        except:
            short_ratio = "NaN"

        trailing_PE_ratios[tickers[i]] = float(trailing_PE_ratio)
        fwd_PE_ratios[tickers[i]] = float(fwd_PE_ratio)
        betas[tickers[i]] = float(beta)
        short_ratios[tickers[i]] = float(short_ratio)
        PEG_ratios[tickers[i]] = float(PEG_ratio)
        PS_ratios[tickers[i]] = float(PS_ratio)
        EV_revenue_ratios[tickers[i]] = float(EV_revenue_ratio)
        PB_ratios[tickers[i]] = float(PB_ratio)

        output = str(tickers[i]+":\tTrailing PE Ratio:\t"+str(trailing_PE_ratios[tickers[i]])+"\t|\tForward PE Ratio:\t"+str(fwd_PE_ratios[tickers[i]])+
                     "\t|\tPEG Ratio:\t\t"+ str(PEG_ratios[tickers[i]]) +"\n\tBeta (3Y Monthly):\t"+str(betas[tickers[i]])+
                     "\t|\tShort Ratio:\t\t"+ str(short_ratios[tickers[i]]) +"\t|\tE.V. to Revenue:\t"+
                     str(EV_revenue_ratios[tickers[i]])+"\n"+"\tPrice-to-Sales Ratio:\t"+ str(PS_ratios[tickers[i]])+
                     "\t|\tPrice-to-Book Ratio:\t"+str(PB_ratios[tickers[i]]))
        print(output)
    PS_ratios_df = pd.DataFrame.from_dict(PS_ratios,orient='index',columns=["Price-to Sales"])
    PB_ratios_df = pd.DataFrame.from_dict(PB_ratios,orient='index',columns=["Price-to-Book"])
    EV_revenue_ratios_df = pd.DataFrame.from_dict(EV_revenue_ratios,orient='index',columns=["EV/Revenue"])
    PEG_ratios_df = pd.DataFrame.from_dict(PEG_ratios,orient='index',columns=["PEG"])
    trailing_PE_ratios_df = pd.DataFrame.from_dict(trailing_PE_ratios,orient='index',columns=["Trailing Price/Earnings"])
    betas_df = pd.DataFrame.from_dict(betas,orient='index',columns=["Beta"])
    fwd_PE_ratios_df = pd.DataFrame.from_dict(fwd_PE_ratios,orient='index',columns=["Forward Price/Earnings"])
    short_ratios_df = pd.DataFrame.from_dict(short_ratios,orient='index',columns=["Short Ratio"])
    all_ratios_df = pd.concat([PS_ratios_df,PB_ratios_df,EV_revenue_ratios_df,PEG_ratios_df,trailing_PE_ratios_df,betas_df,fwd_PE_ratios_df,short_ratios_df], axis=1)
    return all_ratios_df
