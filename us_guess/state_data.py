import pandas as pd

class StateData():

	def __init__(self, csv_path: str):
		self.data: pd.DataFrame
		self.read_data(csv_path=csv_path)
		self.names = [element.lower() for element in list(self.data['state'])]

	def read_data(self, csv_path: str) -> None:
		if not csv_path.endswith(".csv"):
			raise TypeError("not a csv file as expected")
		self.data = pd.read_csv(csv_path)

	def get_position(self, name: str) -> tuple:
		if name not in self.names:
			raise ValueError("Not a valid input.")

		data_frame_row = self.data[self.data['state'].str.lower() == name.lower()]
		data_frame_row = data_frame_row[['x', 'y']]
		return tuple(list(data_frame_row.itertuples(index=False))[0])

	def get_max_score(self) -> int:
		return self.data.shape[0]

	def __str__(self) -> str:
		return str(self.data)