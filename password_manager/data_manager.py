from abc import ABC, abstractmethod
import random as rd
import string as st
import json

"""CONSTANTS"""
# Txt
SEPARATOR = " | "

class Generator(ABC):
	@abstractmethod
	def generate(self) -> str:
		pass

class DataManager(ABC):
	@abstractmethod
	def add_password(self, *atributes: str) -> None:
		pass
	@abstractmethod
	def retrieve_password(self, website: str) -> dict:
		pass

class PasswordGenerator(Generator):

	def __init__(self, password_size: int = 10) -> None:
		self.password_size: int = password_size
		self.char_bank: str = st.ascii_letters + st.digits + st.punctuation

	def generate(self) -> str:
		return ''.join([rd.choice(self.char_bank) for _ in range(self.password_size)])
		

class LocalDataManager(DataManager):
	def __init__(self, storage_file: str) -> None:
		self.storage_file = storage_file

	def add_password(self, *atributes: str) -> None:
		with open(self.storage_file, "a") as file:
			file.write(SEPARATOR.join(atributes) + "\n")

	def retrieve_password(self, website: str) -> dict:
		with open(self.storage_file, "r") as file:
			data = file.readlines()

		print(data)
		filtered_data = [line for line in data if website in line]
		print(filtered_data	)
		filtered_data = filtered_data[0].replace("\n","").split(SEPARATOR)

		return {
		'username': filtered_data[1],
		'password': filtered_data[2]
		}

class JSONLocalDataManager(DataManager):
	def __init__(self, storage_file: str) -> None:
		self.storage_file = storage_file

	def add_password(self, *atributes: str) -> None:
		new_data = {
		atributes[0]: {
			'username': atributes[1],
			'password': atributes[2]
			}
		}

		try:
			with open(self.storage_file, "r") as file:
				data = json.load(file)
				data.update(new_data)
		except:
			with open(self.storage_file, "w") as file:
				json.dump(new_data, file, indent=4)
		else:
			with open(self.storage_file, "w") as file:
				json.dump(data, file, indent=4)



	def retrieve_password(self, website: str) -> dict:
		with open(self.storage_file, "r") as file:
			data = json.load(file)
		return data[website]