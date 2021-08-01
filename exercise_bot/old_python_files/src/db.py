import requests
import datetime

from src.decorators import log

class Sheety:

	def __init__(self):

		self.endpoint = "https://api.sheety.co/3e41b69e3d7c105059981d0ca0c8a47e/exerciseBot/workouts"

	def add_data(self, data):

		date, time = self.get_date_time()

		for exercise in data:
			self.make_request(exercise=exercise, date=date, time=time)

	@log("sheety_request")
	def make_request(self, exercise, date, time):
		print({
					"workouts": {
						**exercise,
						"time": time,
						"date": date 
					}
				})
		response = requests.post(
			url=self.endpoint,
			json={
					"workout": {
						**exercise,
						"time": time,
						"date": date 
					}
				}
			)

		return response.json()

	@staticmethod
	def get_date_time():
		now = datetime.datetime.now()
		return now.strftime("%d/%m/%Y"), now.strftime("%H:%M:%S")