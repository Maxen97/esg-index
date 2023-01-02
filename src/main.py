import pandas as pd
import yfinance as yf
import requests


class Index:
	def __init__(self, tickers=[], start_date="2014-09-01", weighting="normal"):
		self.tickers = tickers
		self.start_date = start_date
		self.weighting = weighting

		self.prices = pd.DataFrame()
		self.esg_scores_raw = pd.DataFrame()
		self.esg_scores = pd.DataFrame()
		self.esg_weights = pd.DataFrame()
		self.index = pd.DataFrame()

		self.initialize_historic_data()


	def initialize_historic_data(self):
		self._init_historic_daily_prices_raw()
		self._init_historic_monthly_esg_scores_raw()
		self._init_historic_padded_daily_esg_scores()


	def _init_historic_daily_prices_raw(self):
		# TODO: Add try-catch
		self.prices = yf.download(self.tickers, start=self.start_date).dropna()["Adj Close"]


	def _init_historic_monthly_esg_scores_raw(self):
		# URL for ESG query
		url = "https://query2.finance.yahoo.com/v1/finance/esgChart"

		for ticker in self.tickers:
			headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}
			response = requests.get(url, headers=headers, params={"symbol": ticker})

			if response.ok:
				temp_df = pd.DataFrame(response.json()["esgChart"]["result"][0]["symbolSeries"]).fillna(method="pad")[["timestamp","esgScore"]]
				temp_df.symbol = ticker
				temp_df["timestamp"] = pd.to_datetime(temp_df["timestamp"], unit="s")
				temp_df = temp_df.set_index("timestamp")
				self.esg_scores_raw[ticker] = temp_df["esgScore"]
	
		self.esg_scores_raw.index.names = ['Date']


	def _init_historic_padded_daily_esg_scores(self):
		# Create a new dataframe with the same indices as self.prices
		self.esg_scores = pd.DataFrame(index=self.prices.index.copy())

		# Merge self.esg_scores with self.esg_scores_raw using combine_first
		self.esg_scores = self.esg_scores.combine_first(self.esg_scores_raw)

		# Forward fill any missing values
		self.esg_scores = self.esg_scores.ffill()

		# Align the indices of self.esg_scores with self.prices
		self.esg_scores = self.esg_scores.reindex(index=self.prices.index)


	def save_csv(self, path="data/"):
		self.prices.to_csv(path+"A.csv")
		self.esg_scores_raw.to_csv(path+"B.csv")
		self.esg_scores.to_csv(path+"C.csv")


if __name__ == "__main__":
	pd.set_option('display.max_rows', None)

	tickers = ["AAPL", "MSFT", "DHR"]
	index = Index(tickers=tickers)
	index.save_csv("db/")