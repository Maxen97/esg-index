import pandas as pd
import yfinance as yf
import requests


def main():
    init_historic_esg_scores()
    

def init_historic_esg_scores ():
    filename = "db/test.csv"

    tickers = ["aapl", "msft", "dhr"]
    tickers = ["aapl"]

    p = yf.download(tickers, start="2014-09-01").dropna()["Adj Close"]

    print(p)

    # Update .csv file
    p.to_csv(filename)


if __name__ == "__main__":
    main()