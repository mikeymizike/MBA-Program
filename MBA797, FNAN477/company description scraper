#Simple web scraper function for grabbing company description from yahoo finance
tickers = ["TMO","ILMN"]

def getdes(tickers): #pass any list of tickers into the function
    import requests
    from bs4 import BeautifulSoup as bs4
    url1 = "https://finance.yahoo.com/quote/"
    pages = ["profile", "key-statistics"] #page names by 
    for i in range(0,len(tickers)):
        des_page_source = requests.get(url1+tickers[i]+"/"+pages[0]+"?p="+tickers[i]) #requests website
        des_soup = bs4(des_page_source.text, 'html.parser') #parses HTML into plaintext
        print(des_soup.h1.text+"\n"+des_soup.find("p", {"class" : "Mt(15px) Lh(1.6)"}).text+"\n") #isolates and prints the descriscription element by class
getdes(tickers)
