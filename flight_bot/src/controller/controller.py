import requests
import datetime

from abc import ABC, abstractmethod

from src.decorators import log
from src.model import db, flight_model, user_model
from src.view import messager, ui
from src.controller import controller

from src.model.flight_model import Flight
from src.model.user_model import User


class Controller(ABC):
	"""Controller abstract class to control the main flow of the aplication"""

	@abstractmethod
	def __init__(self,	
		user_interface: ui.UserInterface,
		messager: messager.Messager,
		flight_model: flight_model.FlightModel,
		user_model: user_model.UserModel
		) -> None:
		"""Initializes the controller with all the components it needs."""
		pass

	@abstractmethod
	def send_cheapest_flights(self) -> None:
		"""For every user in the user_model, find the cheap flight prices using the flight_model.
		Then, send that flight information to the user."""
		pass

	@abstractmethod
	def load_ui(self) -> None:
		"""Load the main ui screen via user_interface."""
		pass

	@abstractmethod
	def get_user(self) -> None:
		"""Get a new user info via the ui and passes that info to user_model via the User dataclass."""
		pass

	@abstractmethod
	def contact_user(self, user: User, flight: Flight) -> None:
		"""Sends the message with flight information to the user via messager."""
		pass


class FlightBotController(Controller):
	"""Implementation for the Controller abstract class. More info on that class."""

	def __init__(self,	
		user_interface: ui.UserInterface,
		messager: messager.Messager,
		flight_model: flight_model.FlightModel,
		user_model: user_model.UserModel
		) -> None:

		self.user_interface = user_interface
		self.messager = messager
		self.flight_model = flight_model
		self.user_model=user_model

	def send_cheapest_flights(self) -> None:
		all_users: list[User] = self.user_model.get_all_users()

		for user in all_users:		
			cheap_flights = self.flight_model.check_cheap_prices(from_city=user.city)
			if cheap_flights:
				self.contact_user(user=user, flights=cheap_flights)

		print("getting cheapest flights")

	def load_ui(self) -> None:
		self.user_interface.start()

	def get_user(self) -> None:
		user_atributes: list[str] = list(User().__dict__.keys())
		user_data: dict = self.user_interface.accquire_user(information_needed=user_atributes)
		self.user_model.add_user(user=User().set(user_data))

	def contact_user(self, user: User, flights: list[Flight]) -> None:
		print("contacting user")
		message = ""
		for flight in flights:
			message += 	f"\nFlight found from {flight.from_city}-{flight.from_airport} to {flight.to_city}-{flight.to_airport} "
			message += 	f"leaving on {flight.departure_date.strftime('%d/%m/%y')} "
			message += 	f"and returning on {flight.return_date.strftime('%d/%m/%y')}\n"
			message += 	f"Only {flight.price} euros!!!!!\n"

		self.messager.send_message(
			destination=user.e_mail,
			subject="Cheap Flight Alert!!!",
			message=message
			)
