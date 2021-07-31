from src.decorators import log
from src.messager import Messager, TerminalMessager
from src.stock import Stocks, TestStocks, AVStocks
from src.news import News, TestNews, ApiNews

def test() -> None:
	n = ApiNews()

	n.fetch_news(key_word="IBM")

	n.get_best_news(number_news=3)


if __name__ == "__main__":
	test()