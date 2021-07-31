from abc import ABC, abstractmethod
import os
import requests

from src.decorators import log
from src.dates import Date

class News(ABC):

	@abstractmethod
	def fetch_news(self, key_word: str, number_news: int = 3) -> list[dict[str]]:
		return [			
			{
				"headline": ...,
				"description": ...,
				"source": ...,
				"link": ...
			},
			...
		]

class TestNews(News):

	def fetch_news(self, key_word: str, number_news: int = 3) -> list[dict[str]]:
		return [
			{
			"headline": "You wont believe what jesus did today",
			"description": "Jesus turned water into wine",
			"source": "me",
			"link": "bible.com"
			}
		]

class ApiNews(News):

	def __init__(self) -> None:
		self.endpoint: str = "https://newsapi.org/v2/everything"
		self.key: str = os.environ.get("NEWS_API_KEY")

	def fetch_news(self, key_word: str, number_news: int = 3) -> list[dict[str]]:
		self.news = self.make_request(key_word=key_word)
		return self.get_best_news(number_news=number_news)

	def make_request(self, key_word: str) -> dict:

		response = requests.get(
			url=self.endpoint,
			params={
				"q": key_word,
				"from": Date().get(day="today"),
				"sortBy": "popularity",
				"apiKey": self.key
				}
			)
			
		response.raise_for_status()

		return response.json()

	@log("news")
	def get_best_news(self, number_news: int) -> list[dict]:
		article_list = self.news["articles"][:number_news]
		return [self.format_article(article=article) for article in article_list]


	def format_article(self, article: dict) -> dict:
		return {
			"headline": article["title"],
			"description": article["description"],
			"source": article["source"]["name"],
			"link": article["url"]
		}