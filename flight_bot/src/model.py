import requests
import datetime
import os

from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Union, Optional, Any

from src.decorators import log
from src.db import DataBase, Sheety

# Data classes
@dataclass
class FlightData:
	price: float 

	departure_date: Optional[datetime.datetime] = None
	return_date: Optional[datetime.datetime] = None

	from_city: Optional[str] = None
	to_city: Optional[str] = None 

	from_code: str = ""
	to_code: str = ""

	from_airport: str = ""
	to_airport: str = ""

	_id: int = Optional[int]

@dataclass
class FlightComparisson:
	initial: FlightData
	found: FlightData

	def is_found_better(self) -> bool:
		return self.found.price < self.initial.price


# Abstract model
class Model(ABC):

	@abstractmethod
	def __init__(self, data_base: DataBase) -> None:
		pass

	@abstractmethod
	def check_cheap_prices(self, from_code: str) -> Optional[list[FlightData]]:
		pass


# Model implementation
class PlaneModel(Model):

	def __init__(self, data_base: DataBase, months_window: int = 6, minimum_stay: int = 2, maximum_stay: int = 20) -> None:
		self.data_base: DataBase = data_base
		self.flight_search_engine = TequilaFlightApi()

		self.months_window: int = months_window
		self.minimum_stay: int = minimum_stay
		self.maximum_stay: int = maximum_stay

	def check_cheap_prices(self, from_city: str) -> list[FlightData]:
		
		from_code: str = self.flight_search_engine.get_IATA_code(from_city) 
		wanted_destinations = self.get_wanted_destinations(from_code=from_code)

		comparissons = [FlightComparisson(initial=destination, found=self.get_cheapest_flight(destination))
			for destination in wanted_destinations]

		flights_data: list[FlightData] = []
		for comparisson in comparissons:
			if comparisson.is_found_better():
				self.update_data(destination=comparisson.initial, new_price=comparisson.found.price)
				flights_data.append(comparisson.found)

		return flights_data

	def get_cheapest_flight(self, destination: FlightData) -> FlightData:
		data = self.flight_search_engine.search_flights(
			from_code=destination.from_code,
			to_code=destination.to_code,
			months_window=self.months_window,
			minimum_stay=self.minimum_stay,
			maximum_stay=self.maximum_stay
			)
		return FlightData(
			price=data["price"],
			departure_date=self.flight_search_engine.decode_dates(data["utc_departure"]),
			return_date=self.flight_search_engine.decode_dates(data["utc_departure"], day_delta = data["nightsInDest"]),
			from_city=data["cityFrom"],
			to_city=data["cityTo"],
			from_code=data["cityCodeFrom"],
			to_code=data["cityCodeTo"],
			from_airport=data["flyFrom"],
			to_airport=data["flyTo"]
			)


	def update_data(self, destination: FlightData, new_price: float) -> None:
		self.data_base.update_data(
			key=destination._id,
			key_values=[{
				"price": new_price
			}]
			)

	def get_wanted_destinations(self, from_code: str) -> list[FlightData]:
		data: list[dict] = self.data_base.get_data()
		return [
			FlightData(
				_id = point["id"],
				to_city = point["city"],
				to_code = self.flight_search_engine.get_IATA_code(point["city"]),
				price = point["price"],
				from_code = from_code
				) for point in data
		] 


# Helper API class
class TequilaFlightApi:

	endpoint: str = "https://tequila-api.kiwi.com"
	api_key: str = os.environ.get("FLIGHT_API")

	@log("flight_search")
	def search_flights(self, from_code: str, to_code: str, months_window: int, minimum_stay: int = 2, maximum_stay: int = 20) -> list[dict]:
		date_from, date_to = self.get_dates(months=months_window)
		try:
			response = requests.get(
				url=f"{self.endpoint}/v2/search",
				headers={
						"apikey": self.api_key
					},
				params={
						"fly_from": from_code,
						"fly_to": to_code,
						"dateFrom": date_from,
						"dateTo": date_to,
						"nights_in_dst_from": minimum_stay,
						"nights_in_dst_to": maximum_stay,
					}
				)
			return response.json()["data"][0]
		except Exception as e:
			print(e)
			return {
				"price": 0 ,
				"utc_departure": "1900-01-01T08:00:00.000Z",
				"nightsInDest": 0,
				"cityFrom": "none",
				"cityTo": "none",
				"flyFrom": "XXX",
				"flyTo": "XXX",
				"cityCodeFrom": "XXX",
				"cityCodeTo": "XXX"
			}

	@log("getting_IATA_codes")
	def get_IATA_code(self, city_name: str) -> str:
		try:
			response = requests.get(
				url=f"{self.endpoint}/locations/query",
				headers={
						"apikey": self.api_key
					},
				params={
						"term": city_name,
					}
				)
			return response.json()["locations"][0]["code"]
		except Exception as e:
			print(e)
			return "XXX"

	@staticmethod
	def get_dates(months: int) -> tuple[str]:
		date_from = datetime.datetime.now().strftime("%d/%m/%Y")
		date_to = (datetime.datetime.now() + datetime.timedelta(months*30)).strftime("%d/%m/%Y")
		return date_from, date_to

	@staticmethod
	def decode_dates(date: str, day_delta: int = 0) -> datetime.datetime:
		return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.000Z") + datetime.timedelta(days=day_delta)

