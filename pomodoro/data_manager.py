from abc import ABC, abstractmethod
import pandas as pd

class Generator(ABC):
	@abstractmethod
	def generate(self) -> str:
		pass

class DataManager(ABC):
	@abstractmethod
	def add_password(self, username: str, password: str, website: str) -> None:
		pass

class PasswordGenerator(Generator):
	pass

class LocalDataManager(DataManager):
	pass