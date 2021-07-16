from abc import ABC, abstractmethod
import random as rd
import string as st

class Generator(ABC):
	@abstractmethod
	def generate(self) -> str:
		pass

class DataManager(ABC):
	@abstractmethod
	def add_password(self, *atributes: str) -> None:
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
			file.write(" | ".join(atributes) + "\n")
