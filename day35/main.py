import requests
import json
import os
from twilio.rest import Client
from abc import ABC, abstractmethod

# Defining decorator
def log(name: str):

	def logger(function):

		def wrapper(*args, **kwargs):

			with open(f"{name}.json", "w") as log_file:
				result = function(*args, **kwargs)	
				log_file.write(function.__name__ + "\n\n")
				log_file.write(json.dumps(result, indent=4))
			return result
			
		return wrapper

	return logger

# Abstract methods
class Messager(ABC):

	@abstractmethod
	def send_message(self, telephone: str, message: str) -> None:
		pass


class Forecast:

	def __init__(self) -> None:
		self.url = "http://api.openweathermap.org/data/2.5/"
		self.key = os.environ.get("WEATHER_KEY")

	def make_request(self, channel: str, parameters: dict) -> dict:
		url = self.url + channel
		response = requests.get(url=url, params=parameters)
		response.raise_for_status()
		return response.json()

	def onecall(self, latitude: float, longitude: float) -> None:
		data = self.make_request(
			channel="onecall",
			parameters={
					"appid": self.key,
					"lat": latitude,
					"lon": longitude,
					"exclude": "current,minutely,daily,alerts"
				}
			)
		return data

	def weather(self, city) -> None:
		data = self.make_request(
			channel="weather",
			parameters={
					"appid": self.key,
					"q": city,
				}
			)
		return data

	@log("next_48h")
	def next_48h(self, latitude: float, longitude: float) -> None:
		data = self.onecall(latitude=latitude, longitude=longitude)
		return [
			{
				"hour": hour + 1,
				"id": int(weather["weather"][0]["id"]),
				"temperature": self.kelvin_to_celsius(weather["temp"]),
				"feels like": self.kelvin_to_celsius(weather["feels_like"]),
				"weather": weather["weather"][0]["main"]
			}	for hour, weather in enumerate(data["hourly"])
		]

	# Miscellaneous methods
	@staticmethod
	def kelvin_to_celsius(temperature: float, round_num: int = 3) -> float:
		return round(temperature - 273.15, round_num)


class Predictor:

	def will_rain_today(self, data: list) -> bool:
		next_12h_data = data[:12]
		ids_list = [hour_data["id"] for hour_data in next_12h_data]
		return any(self.is_rain(idx) for idx in ids_list)

	@staticmethod
	def is_rain(identification: int) -> bool:
		return identification < 700


class TestMessager(Messager):

	def send_message(self, telephone: str, message: str) -> None:
		print(f"message to {telephone}\n{message}")


class TwilioMessager(Messager):

	def __init__(self) -> None:
		self.sid = "ACb62737daa2ca8914b38d013ac3946891"
		self.token = os.environ.get("TWILIO_TOKEN")
		self.number = "+13868663463"
		self.client = Client(self.sid, self.token)

	@log("message")
	def send_message(self, telephone: str, message: str) -> None:
		twilio_message = self.client.messages.create(
			body=message,
			from_=self.number,
			to=telephone
			)

		print(twilio_message.sid)
		return twilio_message.sid


class RainBot:

	def __init__(self, telephone: str, latitude: float, longitude: float) -> None:

		self.predictor = Predictor()
		self.forecast = Forecast()
		self.messager = TwilioMessager()

		self.telephone = telephone
		self.latitude = latitude
		self.longitude = longitude

	def run(self) -> None:

		weather_data = self.forecast.next_48h(
			latitude=self.latitude,
			longitude=self.longitude
			)

		if self.predictor.will_rain_today(data=weather_data):
			self.messager.send_message(
				telephone=self.telephone,
				message="Rain alert! Bring an umbrella ☂️" 
				)


def main() -> None:

	RainBot(
			telephone = "+5531998524668",
			latitude=51.507351,
			longitude=-0.127758
		).run()

if __name__ == "__main__":
	main()

 