from src.text_interpreter import Nutritionix
from src.db import Sheety
from src.decorators import log

class ExerciseBot:
	def __init__(self, gender: str, weight: float, height: float, age: int) -> None:

		self.nutr = Nutritionix()
		self.db = Sheety()

		self.gender = gender
		self.weight = weight
		self.height = height
		self.age = age

	def add_exercise(self, sentence: str) -> None:
		data = self.get_exercise_info(sentence=sentence)
		self.db.add_data(data=data)

	@log("nut_info")
	def get_exercise_info(self, sentence: str) -> list[dict]:
		return self.nutr.get_exercise_info(
			sentence=sentence,
			gender=self.gender,
			weight=self.weight,
			height=self.height,
			age=self.age
			)

def main() -> None:
	bot = ExerciseBot(
		gender="male",
		weight=80.5,
		height=179.0,
		age=20
		)

	sentence = input("Describe your execise: ")

	bot.add_exercise(sentence=sentence)

	

if __name__ == "__main__":
	main()