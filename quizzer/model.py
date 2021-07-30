from abc import ABC, abstractmethod
import requests
import html

class Model(ABC):
	@abstractmethod
	def __init__(self, number_questions: int) -> None:
		pass

	@abstractmethod
	def get_question(self) -> str:
		pass

	@abstractmethod
	def get_answer(self, question: str) -> bool:
		pass

	@abstractmethod
	def are_questions_over(self) -> bool:
		pass

	@abstractmethod
	def get_max_number_questions(self) -> bool:
		pass

class DataBase(ABC):

	@abstractmethod
	def __init__(self, number_questions: int) -> None:
		pass

	@abstractmethod
	def get_questions(self) -> list:
		pass


class MyModel(Model):
	def __init__(self, number_questions: int):
		self.data_base: DataBase = OpenTriviaDataBase(number_questions=number_questions)
		self.questions: list = self.data_base.get_questions()
		self.question_number: int = 0
		self.max_questions: int = len(self.questions)

	def get_question(self) -> str:
		question = self.questions[self.question_number]["question"]
		self.question_number += 1
		return question

	def get_answer(self, question: str) -> bool:
		answer = next(quest for quest in self.questions if quest["question"] == question)["answer"]
		return answer

	def are_questions_over(self) -> bool:
		return self.question_number == self.max_questions

	def get_max_number_questions(self) -> bool:
		return self.max_questions


class TestDataBase(DataBase):

	def __init__(self, number_questions: int) -> None:
		pass

	def get_questions(self) -> list:
		return [
			{
				"question": "is red, .... red?",
				"answer": True
			},
			{
				"question": "what about, ..... blue? is it red?",
				"answer": False
			}
		]

class OpenTriviaDataBase(DataBase):

	def __init__(self, number_questions: int) -> None:
		self.data: dict = self.make_request(number_questions)
		self.questions: list = self.clean_data()
		self.max_questions: int = len(self.questions)

	def get_questions(self) -> list:
		return self.questions

	def make_request(self, number_questions: int) -> dict:
		response = requests.get(
			url="https://opentdb.com/api.php",
			params={
					"amount": number_questions,
					"type": "boolean"
				}
			)
		response.raise_for_status()
		return response.json()

	def clean_data(self) -> list:
		return [
			{
				"question": html.unescape(question["question"]),
				"answer": question["correct_answer"] == "True"
			} for question in self.data["results"]
		]

	def get_max_number_questions(self) -> bool:
		return self.max_questions

