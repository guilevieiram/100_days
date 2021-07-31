from src.messager import Messager
from src.stock import Stocks
from src.news import News


class Bot:

	def __init__(self, companies: list[dict[str]], telephone: str, fluctuation_treshold: float, number_news: int, stocks: Stocks, messager: Messager, news: News) -> None:

		self.stocks: Stocks = stocks
		self.news: News = news
		self.messager: Messager =  messager

		self.companies: list[dict[str]] = companies
		self.telephone: str = telephone
		self.treshold: float = fluctuation_treshold
		self.number_news: int = number_news

	def run(self) -> None:

		message = ""

		for company in self.companies:

			stock = company["stock"]
			name = company["name"]

			self.stocks.fetch_info(stock=stock)

			if self.stocks.high_fluctuation(stock=stock, treshold=self.treshold):
				
				news = self.news.fetch_news(key_word=name, number_news=self.number_news)

				fluctuation = self.stocks.get_fluctuation(stock=stock)

				message += self.format_message(news=news, stock=stock, fluctuation=fluctuation)
				
		self.messager.send_message(
			telephone=self.telephone,
			message=message
			)

	def format_message(self, news: list[dict[str]], stock: str, fluctuation: float) -> str:
		return "".join([f"""
{stock}: {"🔺" if fluctuation > 0 else "🔻"} {int(abs(fluctuation*100))}%
-------------------------------------------------------
Headline: {article["headline"]}
Source: {article["source"]}
Link: {article["link"]}

{article["description"]}

"""for article in news])