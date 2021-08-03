from src.decorators import log
from src.db import DataBase, Sheety, PandasDB
from src.model import Model, PlaneModel
from src.view import Messager, TerminalMessager, EmailMessager
from src.controller import Controller, PlaneBotController

def main() -> None:

	data_base: DataBase = PandasDB
	messager: Messager = EmailMessager
	model: Model = PlaneModel
	controller: Controller = PlaneBotController

	controller(

		from_city="Paris",
		message_destination="guilhermevmanhaes@gmail.com",

		messager=messager(),

		model=model(
			data_base=data_base(
					project = "flightBot",
					table = "flights"
				),
			minimum_stay=7,
			months_window=3,
			)

		).get_cheapest()

	controller(

		from_city="London",
		message_destination="bruna.patrus@gmail.com",

		messager=messager(),

		model=model(
			data_base=data_base(
					project = "flightBot",
					table = "buFlights"
				),
			minimum_stay=7,
			months_window=3,
			)

		).get_cheapest()

if __name__ == "__main__":
	main()