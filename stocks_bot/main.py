from src.messager import Messager, TerminalMessager, FileMessager
from src.stock import Stocks, TestStocks, AVStocks
from src.news import News, TestNews, ApiNews
from src.bot import Bot

def main() -> None:

	companies=[
			{
				"stock": "TSLA",
				"name": "Tesla"
			},
			{
				"stock": "GOGL",
				"name": "Google"
			},
			{
				"stock": "AAPL",
				"name": "Apple"
			},
			{
				"stock": "MSFT",
				"name": "Microsoft"
			},
			{
				"stock": "AMZN",
				"name": "Amazon"
			},

		]

	Bot(
		companies=companies,
		telephone="+5531998524668",
		fluctuation_treshold=0.01,
		number_news=2,
		
		stocks=AVStocks(),
		news=ApiNews(),
		messager=FileMessager()
		).run()

if __name__ == "__main__":
	main()