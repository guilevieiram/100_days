import turtle as t
import time

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600

X_POS = 0 
Y_POS = SCREEN_HEIGHT//2 - 50

FONT_COLOR = 'white'
ALIGN = 'center'
FONT = 'courier'
FONT_SIZE = 15
FONT_TYPE = 'bold'

GAME_OVER_FONT_SIZE = 50
GAME_OVER_FONT_COLOR = 'red'

YOU_DIED_POS = (0, 0)
YOU_DIED_TIME = 1

HIGH_SCORE_FILE_NAME = 'data.txt'

class Scoreboard (t.Turtle):

	def __init__(self) -> None:
		super().__init__()
		self.score: int = 0
		self.high_score: int = self.get_high_score()
		self.hideturtle()
		self.speed(0)
		self.pencolor(FONT_COLOR)
		self.penup()
		self.write_score()

	def write_score(self) -> None:
		self.goto(x=X_POS, y=Y_POS)
		self.clear()
		self.write(
			f"HIGHT SCORE: {self.high_score}\n   SCORE: {self.score}", 
			align=ALIGN, 
			font=(FONT, FONT_SIZE, FONT_TYPE)
			)

	def increase_score(self) -> None:
		self.score += 1
		self.write_score()

	def reset(self) -> None:
		if self.score > self.high_score:
			self.high_score = self.score
			self.export_high_score()

		self.score = 0

		self.you_died_message()

		time.sleep(YOU_DIED_TIME)

		self.write_score()

	def get_high_score(self) -> int:
		with open(HIGH_SCORE_FILE_NAME, mode='r') as f:
			return int(f.read())

	def export_high_score(self) -> None:
		with open(HIGH_SCORE_FILE_NAME, mode='w') as f:
			f.write(str(self.high_score))

	def you_died_message(self) -> None:
		self.goto(YOU_DIED_POS)
		self.clear()
		self.write(
			f"YOU DIED", 
			align=ALIGN, 
			font=(FONT, FONT_SIZE, FONT_TYPE)
			)

	def game_over(self) -> None:
		self.clear()
		self.home()
		self.pencolor(GAME_OVER_FONT_COLOR)
		self.write(
			"GAME OVER", 
			align=ALIGN,
			font=(FONT, GAME_OVER_FONT_SIZE, FONT_TYPE)
			)

		self.pencolor(FONT_COLOR)
		self.setheading(-90)
		self.forward(50)
		self.write(
			f"final score: {self.score}", 
			align=ALIGN,
			font=(FONT, FONT_SIZE * 2, FONT_TYPE)
			)