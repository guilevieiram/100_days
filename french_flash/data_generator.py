from googletrans import Translator
import pandas as pd

# Frequency words retrieved from https://github.com/hermitdave/FrequencyWords

class DataGenerator:
	def __init__(self, original_data_path: str, source_language: str, size: int = 10) -> None:
		self.source = source_language
		self.translator = Translator()
		self.data = pd.read_csv(original_data_path, sep=' ', header=None)[:size]
		self.clean_data()

	def clean_data(self) -> None:
		self.data.columns = [self.source, 'frequency']
		self.data.drop(columns='frequency', inplace=True)
		self.data.dropna()

	def translate(self, target_language: str) -> None:
		self.target = target_language
		self.data[self.target] = self.data[self.source].map(
			lambda word: self.translator.translate(str(word), src=self.source, dest=self.target
				).text
			)

	def print_data(self) -> None:
		print(self.data.head())

	def export_data(self, export_path: str) -> None:
		self.data.to_csv(export_path, index=False)

def main() -> None:
	gen = DataGenerator(
		original_data_path='fr.csv',
		source_language='fr',
		)
	gen.translate(target_language='en')
	gen.export_data("data.csv")

if __name__=="__main__":
	main()