from data import question_data
from question_model import Question
from quiz_brain import QuizBrain

'''Initialize the question bank'''
question_bank = [Question(question['text'], question['answer']) 
	for question in question_data]

'''Initialize the quiz brain '''
quiz = QuizBrain(question_bank)

'''Main action loop'''
while quiz.still_has_questions():
	quiz.next_question()
else:
	quiz.end_quiz()