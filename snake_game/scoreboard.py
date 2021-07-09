import turtle as t

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600

X_POS = 0 
Y_POS = SCREEN_HEIGHT//2 - 30

FONT_COLOR = 'white'
ALIGN = 'center'
FONT = 'arial'
FONT_SIZE = 15
FONT_TYPE = 'bold'

GAME_OVER_FONT_SIZE = 50
GAME_OVER_FONT_COLOR = 'red'

class Scoreboard (t.Turtle):

	def __init__(self) -> None:
		super().__init__()
		self.score: int = 0
		self.hideturtle()
		self.speed(0)
		self.pencolor(FONT_COLOR)
		self.penup()
		self.goto(x=X_POS, y=Y_POS)
		self.write_score()

	def write_score(self) -> None:
		self.clear()
		self.write(
			f"SCORE: {self.score}", 
			align=ALIGN, 
			font=(FONT, FONT_SIZE, FONT_TYPE)
			)

	def increase_score(self) -> None:
		self.score += 1
		self.write_score()

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