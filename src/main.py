import pandas as pd
import yfinance as yf
import requests


def main ():
    #update_raw_prices()
    update_esg_scores()


def update_all ():
    # update all raw data files
    ## check if last input date is today
    
    # update weight and index data files
    pass


def update_raw_prices ():
    filename = "db/historic_adjusted_stock_prices.csv"

    tickers = ["aapl", "msft", "dhr"]

    p = yf.download(tickers, start="2014-09-01").dropna()["Adj Close"]

    # Update .csv file
    p.to_csv(filename)


def update_esg_scores ():
    filename = "db/esg_scores.csv"
    pd.set_option('display.max_rows', None)
    tickers = ["aapl", "msft", "dhr"]

    # URL for ESG query
    url = "https://query2.finance.yahoo.com/v1/finance/esgChart"

    d = []
    df = pd.DataFrame()

    for ticker in tickers:
        headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}
        response = requests.get(url, headers=headers, params={"symbol": ticker})
   
        if response.ok:
            _df = pd.DataFrame(response.json()["esgChart"]["result"][0]["symbolSeries"]).fillna(method="pad")[["timestamp","esgScore"]]
            _df.symbol = ticker
            _df["timestamp"] = pd.to_datetime(_df["timestamp"], unit="s")
            _df = _df.set_index("timestamp")
            df[ticker] = _df["esgScore"]
    
    df.to_csv(filename)
    print(df)



# Create an ESG weighted Pandas dataframe


# Create index from historic stock prices and ESG weights




if __name__ == '__main__':
    main()