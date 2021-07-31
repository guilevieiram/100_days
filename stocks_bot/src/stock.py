from abc import ABC, abstractmethod
import os
import requests
import datetime

from src.decorators import log
from src.dates import Date


class Stocks(ABC):

	@abstractmethod
	def fetch_info(self, stock: str) -> None:
		pass

	@abstractmethod
	def get_fluctuation(self, stock: str) -> float:
		pass

	@abstractmethod
	def high_fluctuation(self, stock: str, treshold: float) -> bool:
		pass


class TestStocks(Stocks):

	def fetch_info(self, stock: str) -> None:
		print(f"Fetching prices for {stock}")

	def get_fluctuation(self, stock: str) -> float:
		print("Returning fluctuations")
		return 1.0

	def high_fluctuation(self, stock: str, treshold: float) -> bool:
		print(f"Evaluating fluctuations for {stock}")
		return True


class AVStocks(Stocks):

	def __init__(self) -> None:
		self.endpoint: str = "https://www.alphavantage.co/query"
		self.api_key: str = os.environ.get("ALPHA_VANTAGE_KEY")
		self.prices: dict = {}

	def fetch_info(self, stock: str) -> None:
		self.prices[stock] = self.make_request(stock=stock)["Time Series (Daily)"]


	def high_fluctuation(self, stock: str, treshold: float) -> bool:
		fluctuation = self.get_fluctuation(stock=stock)
		return abs(fluctuation) >= treshold

	def get_fluctuation(self, stock: str) -> float:

		today: str = Date().get("today")
		yesterday: str = Date().get("yesterday")

		price_today: float = float(self.prices[stock][today]["5. adjusted close"])
		price_yesterday: float = float(self.prices[stock][yesterday]["5. adjusted close"])

		price_delta: float = price_today - price_yesterday

		return price_delta / price_today

	@log("prices")
	def make_request(self, stock: str) -> dict:

		response = requests.get(
			url=self.endpoint,
			params={
				"function": "TIME_SERIES_DAILY_ADJUSTED",
				"symbol": stock,
				"outputsize": "compact",
				"apikey": self.api_key
				}
			)
			
		response.raise_for_status()

		return response.json()

