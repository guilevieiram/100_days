class QuizBrain():
	def __init__(self, questions_list: list):
		self.questions_list: list = questions_list
		self.question_number: int = 0
		self.score: int = 0

	def next_question(self) -> None:
		question = self.questions_list[self.question_number]
		answer = input(
			f"Q. {self.question_number + 1}: {question.text} (True/False): "
			)
		self.check_answer(answer)
		self.question_number += 1


	def still_has_questions(self) -> bool:
		return len(self.questions_list) > self.question_number

	def check_answer(self, answer: str) -> None:
		if answer.lower() == self.questions_list[self.question_number].answer.lower():
			self.score += 1
			print("You got it!")
		else: 
			print("Not quite there...")

		print(f"The answer was {self.questions_list[self.question_number].answer}")
		print(f"Your current score is {self.score}/{self.question_number + 1}\n\n")

	def end_quiz(self) -> None:
		print(
			f'''You've completed the quizz!
			Your final score is {self.score}/{self.question_number + 1}'''
			)