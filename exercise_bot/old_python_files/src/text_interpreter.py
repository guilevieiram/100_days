import requests

class Nutritionix:

	def __init__(self):

		self.endpoint = "https://trackapi.nutritionix.com"
		self.app_id = "0ebd65b5"
		self.key =  "f87172445b512b8923974b5e9ce09da8"

	def get_exercise_info(self, sentence, gender, weight, height, age):

		self.sentence = sentence
		self.gender = gender
		self.weight = str(weight)
		self.height = str(height)
		self.age = str(age)

		self.data_raw = self.make_request()

		return self.process_data(data=self.data_raw)

	def make_request(self):
		response = requests.post(
			url=f"{self.endpoint}/v2/natural/exercise",
			json={	
					"query": self.sentence,
					"gender": self.gender,
					"weight_kg": self.weight,
					"height_cm": self.height,
					"age": self.age
				},
			headers={
					"x-app-id": self.app_id,
					"x-app-key": self.key,
					"Content-Type": "application/json"
				}
			)	
		return response.json()

	@staticmethod
	def process_data(data):
		return [
			{	
				"exercise": exercise["name"],
				"duration": str(exercise["duration_min"]),
				"calories": str(exercise["nf_calories"])
			}	for exercise in data["exercises"]
		]