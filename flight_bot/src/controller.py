import requests
import datetime

from abc import ABC, abstractmethod

from src.model import Model, FlightData
from src.view import Messager


class Controller(ABC):

	@abstractmethod
	def __init__(self, from_city: str, model: Model, messager: Messager) -> None:
		pass

	@abstractmethod
	def get_cheapest(self) -> None:
		pass


class PlaneBotController(Controller):

	def __init__(self, from_city: str, message_destination: str, model: Model, messager: Messager) -> None:

		self.from_city: str = from_city
		self.message_destination: str = message_destination

		self.model: Model = model
		self.messager: Messager = messager

	def get_cheapest(self) -> None:
		cheap_flights = self.model.check_cheap_prices(from_city=self.from_city)
		if cheap_flights:
			self.anounce_flights(flights=cheap_flights)

	def anounce_flights(self, flights: list[FlightData]) -> None:
		for flight in flights:
			if not flight.price == 0:
				message = 	f"Flight found from {flight.from_city}-{flight.from_airport} to {flight.to_city}-{flight.to_airport} " + \
							f"leaving on {flight.departure_date.strftime('%d/%m/%y')} " + \
							f"and returning on {flight.return_date.strftime('%d/%m/%y')}\n" + \
							f"Only {flight.price} euros!!!!!"

				self.messager.send_message(
					destination=self.message_destination,
					subject="Cheap Flight Alert!!!",
					message=message
					)
