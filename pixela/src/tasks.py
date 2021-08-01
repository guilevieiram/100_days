import requests
from abc import ABC, abstractmethod

from src.decorators import log

class Tasks(ABC):

	@abstractmethod
	def create_task(self, task: str) -> None:
		pass

	@abstractmethod
	def increase_task_counter(self, task: str, count_number: int) -> None:
		pass


class Pixela(Tasks):

	def __init__(self) -> None:

		self.endpoint: str = "https://pixe.la/v1"
		self.username: str = "guilhermevieira"
		self.token: str = "qwertyuiopasdfghjklzxcvbnm"

		self.graph_id: str = "guilegraph1"

	def create_task(self, task: str) -> None:
		pass

	def increase_task_counter(self, task: str, count_number: int) -> None:
		pass

	@log("pixela_create")
	def create_user(self) -> str:
		response = requests.post(
			url=f"{self.endpoint}/users",
			json={
				"token": self.token,
				"username": self.username,
				"agreeTermsOfService": "yes",
				"notMinor": "yes"
				}
			)
		return response.text

	@log("pixela_graph")
	def create_graph(self, name: str, unit: str, data_type: str) -> str:
		response = requests.post(
			url=f"{self.endpoint}/users/{self.username}",
			json={
					"id": self.graph_id,
					"name": name,
					"unit": unit,
					"type": data_type,
					"color": "sora"
				},
			headers={
					"X-USER-TOKEN": self.token
				}
			)
		return response.text		

