import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import requests
from math import *

# URL for ESG query
url = "https://query2.finance.yahoo.com/v1/finance/esgChart"


# Create list with company tickers to be included in the index
tickers = ["aapl", "msft", "dhr"]

# Fetch stock price of each company and store in a Pandas dataframe
price_df = pd.DataFrame(columns=tickers)
print(price_df)
p = yf.download(tickers, interval="1mo", start="2020-01-01", end="2022-05-01").dropna()
print(p["Adj Close"])

# Fetch ESG score of each company and store in a Pandas dataframe
esg_df = pd.DataFrame(tickers)
#print(esg_df)
print("Start")
for i, ticker in enumerate(tickers):
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}
    response = requests.get(url, headers=headers, params={"symbol": ticker})
   
    if response.ok:
        df = pd.DataFrame(response.json()["esgChart"]["result"][0]["symbolSeries"]).fillna(method="pad")
        time = df["timestamp"]
        ar = np.array(df["esgScore"])
        #esg[:,i] = ar
print("end")



# Create an ESG weighted Pandas dataframe


# Create index from historic stock prices and ESG weights









"""

# Read in your symbols
tickers = ["aapl", "msft", "dhr"]
#tickers = ["dhr"]

# Endpoint
url = "https://query2.finance.yahoo.com/v1/finance/esgChart"

# List of dataframes (currently only ESG score, but can include separate env,
# soc, and gov scores in the future...
###  |timestamp  company1  company2 ... |
###  |14-05.01      23        24        |
###  |...                               |
esg = np.zeros([93, len(tickers)])
weights = np.zeros([93, len(tickers)])
time = []
stock = np.zeros([93, len(tickers)])


dataframes = []
#pd.set_option('display.max_rows', None)


# Get ESG data
for i, ticker in enumerate(tickers):
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}
    response = requests.get(url, headers=headers, params={"symbol": ticker})
   
    if response.ok:
        df = pd.DataFrame(response.json()["esgChart"]["result"][0]["symbolSeries"]).fillna(method="pad")
        time = df["timestamp"]
        ar = np.array(df["esgScore"])
        esg[:,i] = ar
       
       
# Update weighting
for i in range(len(esg[:,0])):
    for j in range(len(weights[0])):
        weights[i,j] = esg[i, j] / sum(esg[i,:])


# Download stock price
p = yf.download(tickers, interval="1mo", start="2020-01-01", end="2022-05-01").dropna()
print(p["Adj Close"])

# Update index price

#esg["aapl"] = pd.to_datetime(esg["aapl"], unit="s")
#print(esg)
#print(weights)
#plt.plot(time, esg)
#plt.show()
#df = pd.concat(dataframes)
#df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
#print(df[["timestamp", "esgScore"]])
"""