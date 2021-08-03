"""
TODO:

- refactor CMV architecture ok
- refactor table management to acquire users ok
- build ui for getting users ok

- extend data structure to handle multiple cities
-COMMENT THE CODE FOR GODS SAKE

"""

"""
BUGS:
- phone getting saved as float not string
- same good flight not going to all users
"""


from src.decorators import log
from src.model import db, flight_model, user_model
from src.view import messager, ui
from src.controller import controller

def main(
	user_interface: ui.UserInterface,
	messager: messager.Messager,

	controller: controller.Controller,

	flight_model: flight_model.FlightModel,
	user_model: user_model.UserModel,
	data_base: db.DataBase
	) -> None:

	bot = controller(
		user_interface=user_interface(),
		messager=messager(),
		flight_model=flight_model(
			data_base=data_base(
				table="flights"
				)
			),
		user_model=user_model(
			data_base=data_base(
				table="users"
				)
			),
		)

	bot.load_ui()

	bot.get_user()
	bot.send_cheapest_flights()



if __name__ == "__main__":
	main(
		controller=controller.FlightBotController,
		user_interface=ui.TerminalUserInteface,
		messager=messager.TerminalMessager,
		flight_model=flight_model.TequilaFlightModel,
		user_model=user_model.TerminalUserModel,
		data_base=db.CSVDB
		)