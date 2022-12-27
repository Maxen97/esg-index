import pandas as pd
import yfinance as yf
import requests


def init_historic_raw_daily_prices():
    filename = "db/historic_raw_daily_prices.csv"
    tickers = ["aapl", "msft", "dhr"]
    start_date = "2014-09-01"
    end_date = "2022-09-01"

    p = yf.download(tickers, start=start_date).dropna()["Adj Close"]

    p.to_csv(filename)
    

def init_historic_raw_monethly_esg_scores():
    filename = "db/historic_raw_monthly_esg_scores.csv"

    tickers = ["aapl", "msft", "dhr"]

    # URL for ESG query
    url = "https://query2.finance.yahoo.com/v1/finance/esgChart"

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


def init_historic_padded_daily_esg_scores():
    filename = "db/historic_padded_daily_esg_scores.csv"

    tickers = ["aapl", "msft", "dhr"]

    price = pd.read_csv("db/historic_raw_daily_prices.csv", index_col="Date")
    esg = pd.read_csv("db/historic_raw_monthly_esg_scores.csv", index_col="timestamp")

    # Create pandas DataFrame with exact same rows as daily_prices dataframe
    df = pd.DataFrame(index=price.index.copy())

    # Fill with esg scores from monthly raw dataframe
    for ticker in list(esg.columns):
        pass
    print(esg.loc[:,"msft"])

    # Add padding
    df.to_csv(filename)


if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
    #init_historic_raw_daily_prices()
    #init_historic_raw_monethly_esg_scores()
    init_historic_padded_daily_esg_scores()
    
    