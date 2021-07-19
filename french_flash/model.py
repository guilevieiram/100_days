from abc import ABC, abstractmethod
import pandas as pd

"""CONSTANTS"""
# Data
CSV_PATH = 'data/french_words.csv'
TO_LEARN_CSV_PATH = 'data/words_to_learn.csv'

class Model(ABC):
	@abstractmethod
	def remove_data(self, data) -> None:
		pass
	@abstractmethod
	def generate_data(self) -> None:
		pass
	@abstractmethod
	def get_current_data(self) -> dict:
		pass

class MyModel(Model):
	def __init__(self) -> None:
		self.data: pd.DataFrame = pd.read_csv(CSV_PATH)
		
		try:
			self.data_to_learn = pd.read_csv(TO_LEARN_CSV_PATH)
		except FileNotFoundError:
			self.data_to_learn = self.data

		self.current_data: dict = {"French": '', "English": ''}

	def remove_data(self, data) -> None:
		self.data_to_learn = self.data_to_learn[self.data_to_learn["French"] != data["French"]]
		self.save()

	def save(self) -> None:
		self.data_to_learn.to_csv(TO_LEARN_CSV_PATH, index=False)

	def generate_data(self) -> dict:
		self.current_data = self.data.sample(n=1, axis='rows').to_dict(orient='records')[0]

	def get_current_data(self) -> dict:
		return self.current_data

if __name__=="__main__":
	model = MyModel()
	print(model.get_data())