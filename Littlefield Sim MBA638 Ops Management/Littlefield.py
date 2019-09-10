from selenium import webdriver
from bs4 import BeautifulSoup
import openpyxl, re, os
import pandas as pd
import numpy as np


browser = webdriver.Chrome()

teamid = "teamid"
password = "password"

urls = ["JOBIN","S1UTIL","S1Q","S2UTIL","S2Q","S3UTIL","S3Q","CASH"]
column_letter = ["A","B","C","D","E","F","G","H","I"]

multiurls = ["JOBT","JOBOUT","JOBREV"]
column_letter2 = ["J","M","P","K","N","Q","L","O","R"]
allmultiurls = ["JOBT1","JOBOUT1","JOBREV1","JOBT2","JOBOUT2","JOBREV2","JOBT3","JOBOUT3","JOBREV3"]
allurls = ["JOBIN","S1UTIL","S1Q","S2UTIL","S2Q","S3UTIL","S3Q","INV","CASH","JOBT1","JOBOUT1","JOBREV1","JOBT2","JOBOUT2","JOBREV2","JOBT3","JOBOUT3","JOBREV3"]

entry = "http://op.responsive.net/lt/gmu2/entry.html"
main = "http://op.responsive.net/Littlefield/CheckAccess"

tracker = "C:\\Users\\Dell\\Desktop\\littlefield.xlsx"
datadict = {}
invdict = {}


#login to littlefield simulation
browser.get(entry)
browser.find_element_by_name("id").send_keys(teamid)
browser.find_element_by_name("password").send_keys(password)
browser.find_element_by_xpath("/html/body/center/form/p/font/input[2]").click()
browser.switch_to_alert().accept()


#for single-point data 
for x in range(0, len(urls)):
    browser.get("http://op.responsive.net/Littlefield/Plot?data=" + str(urls[x]) + "&x=all") #opens the browser iterating thru urls variable
    html = browser.page_source #converts the browser.get into html for BS4 parsing
    soup = BeautifulSoup(html) # Parses the html into a BS4 object
    soup = soup.find_all('td')[1] #isolates the data output table
    data = [] #sets an empty list for data points
    for i in range(0,len(soup)): #sets for loop to create list of data points
        data.append(soup.find_all('span')[i].contents) #adds data points to list
    data = str(data) #converts data list into a string
    data = [float(s) for s in re.findall(r'-?\d+\.?\d*', data)] #finds all floats in the data string. [Source: Dharmkar, R. (2017, December 12). How to extract numbers from a string in Python. Retrieved December 16, 2018, from https://www.tutorialspoint.com/How-to-extract-numbers-from-a-string-in-Python]
    datadict[str(urls[x])] = data
    wb = openpyxl.load_workbook(tracker) #opens the excel tracker
    sheet = wb['Data'] # selects the Data sheet within the excel tracker
    for i in range(0,len(data)): #sets for loop for adding data from list to rows in excel tracker
        sheet[str(column_letter[x]) + str(i+2)] = data[i] #selects column x and iterates through data list
    wb.save(tracker) #saves the tracker

#for multipoint data
for n in range(1,4):
    for x in range(0, len(multiurls)):
        browser.get("http://op.responsive.net/Littlefield/Plot?data=" + str(multiurls[x]) + "&x=all") #opens the browser iterating thru urls variable
        html = browser.page_source #converts the browser.get into html for BS4 parsing
        soup = BeautifulSoup(html) # Parses the html into a BS4 object
        soup = soup.find_all('td')[n] #isolates the data output table
        data = [] #sets an empty list for data points
        for i in range(0,len(soup)): #sets for loop to create list of data points
            data.append(soup.find_all('span')[i].contents) #adds data points to list
        data = str(data) #converts data list into a string
        data = [float(s) for s in re.findall(r'-?\d+\.?\d*', data)] #finds all floats in the data string. [Source: Dharmkar, R. (2017, December 12). How to extract numbers from a string in Python. Retrieved December 16, 2018, from https://www.tutorialspoint.com/How-to-extract-numbers-from-a-string-in-Python]
        datadict[str(allmultiurls[x+((n-1)*3)])] = data
        for i in range(0,len(data)): #sets for loop for adding data from list to rows in excel tracker
            sheet[str(column_letter2[x+((n-1)*3)]) + str(i+2)] = data[i] #selects column x and iterates through data list
        wb.save(tracker) #saves the tracker

#For inventory (partial days)
browser.get("http://op.responsive.net/Littlefield/Plot?data=INV&x=all")
html = browser.page_source #converts the browser.get into html for BS4 parsing
soup = BeautifulSoup(html) # Parses the html into a BS4 object
days = soup.find_all('td')[0] #isolates the days
data = soup.find_all('td')[1] #isolates the data output
dayslist = []
datalist = []
for i in range(0,len(data)): #sets for loop to create list of data points
     datalist.append(data.find_all('span')[i].contents) #adds data points to list
for i in range(0,len(days)): #sets for loop to create list of data points
    dayslist.append(days.find_all('span')[i].contents) #adds data points to list
dayslist = str(dayslist) #converts data list into a string
dayslist = [float(s) for s in re.findall(r'-?\d+\.?\d*', dayslist)]
invdict['Days'] = dayslist
    
datalist = str(datalist) #converts data list into a string
datalist = [float(s) for s in re.findall(r'-?\d+\.?\d*', datalist)] #finds all floats in the data string. [Source: Dharmkar, R. (2017, December 12). How to extract numbers from a string in Python. Retrieved December 16, 2018, from https://www.tutorialspoint.com/How-to-extract-numbers-from-a-string-in-Python]
invdict['Inventory'] = datalist


#wb = openpyxl.load_workbook(tracker) #opens the excel tracker
#sheet = wb['Inventory']
#for i in range(0,len(datalist)): #sets for loop for adding data from list to rows in excel tracker
#    sheet['A'+ str(i+2)] = dayslist[i] #selects column x and iterates through data list
#for i in range(0,len(datalist)): #sets for loop for adding data from list to rows in excel tracker
#    sheet['B'+ str(i+2)] = datalist[i] #selects column x and iterates through data list
#wb.save(tracker)
#os.startfile(tracker) #opens the tracker


#converts dictionary data to pandas dataframe
df = pd.DataFrame.from_dict(datadict)
df.index = np.arange(1, len(df) + 1)
df.index.name = "Day"
df.tail()

invdf = pd.DataFrame.from_dict(invdict).set_index('Days')
invdf.tail()


get_ipython().run_line_magic('matplotlib', '')
df[["JOBIN"]].plot()
df[["JOBOUT1","JOBOUT3","JOBOUT3"]].plot()


# #References
# #Dharmkar, R. (2017, December 12). How to extract numbers from a string in Python. Retrieved December 16, 2018, from https://www.tutorialspoint.com/How-to-extract-numbers-from-a-string-in-Python
# #Lewis, G. (2017, March 14). Scraping the Littlefield Simulation with Python. Retrieved December 16, 2018, from https://medium.com/@gregdlewis/scraping-the-littlefield-simulation-with-python-a6bf618c6833
# #Sweigart, A. (2017). Automate the Boring Stuff With Python: Practical Programming for Total Beginners. Retrieved December 16, 2018, from https://automatetheboringstuff.com/
# 




