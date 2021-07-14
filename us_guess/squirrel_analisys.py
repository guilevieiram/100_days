import pandas as pd
"primary fur column"

class SquirrelAnalysis():

	def __init__(self):
		self.data: pd.DataFrame
		self.column: str
		self.feature_count: pd.Series

	def load_data(self, path_to_csv: str) -> None:
		self.data = pd.read_csv(path_to_csv)

	def count_feature(self, feature: str) -> pd.Series:
		if not feature in list(self.data.columns):
			raise ValueError("Not a column of the loaded data...")

		self.feature_count = self.data[feature].value_counts()

	def column_values(self) -> str:
		return str(list(self.data.columns))

	def export_feature_count(self, path: str) -> None:
		self.feature_count.to_csv(path)

	def __str__(self) -> str:
		return f"Primary fur color count:\n{self.feature_count}"

if __name__=='__main__':
	analysis = SquirrelAnalysis()

	analysis.load_data("squirrel_data.csv")
	analysis.count_feature("Primary Fur Color")
	analysis.export_feature_count("fur_color.csv")


	print(analysis)
