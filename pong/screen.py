import turtle as t
from constants import *

class Scoreboard(t.Turtle):

	def __init__(self) -> None:
		super().__init__()

		self.hideturtle()
		self.penup()
		self.goto(x=0, y=Y_MAX-SCOREBOARD_PADY)
		self.pendown()
		self.pencolor(FONT_COLOR)

	def update(self, player_1_score: int, player_2_score: int):
		self.clear()
		self.write(
			f"{player_1_score}  {player_2_score}", 
			align=ALIGN, 
			font=(FONT, FONT_SIZE, FONT_TYPE)
			)

class Screen():

	def __init__(self) -> None:
		self.screen: t.Screen = t.Screen()

		self.screen.setup(width=SCREEN_WIDTH, height = SCREEN_HEIGHT)
		self.screen.bgcolor(SCREEN_COLOR)
		self.screen.title(GAME_NAME) 
		self.screen.tracer(0)
		self.draw_dashed_line()
		self.screen.listen()

		self.scoreboard: Scoreboard = Scoreboard()

	def close(self) -> None:
		self.screen.bye()

	def action(self, key: str, function) -> None:
		self.screen.onkeypress(key=key, fun=function)

	def enable_movement(self) -> None:
		self.screen.tracer(1)

	def draw_dashed_line(self):
		dashed = t.Turtle()
		dashed.hideturtle()
		dashed.pencolor(ELEMENTS_COLOR)
		dashed.speed(0)
		dashed.setheading(90)
		dashed.penup()
		dashed.goto(0, Y_MAX)

		for _ in range(Y_MAX//DASHES_LENGHT):
			dashed.pendown()
			dashed.backward(DASHES_LENGHT)
			dashed.penup()
			dashed.backward(DASHES_LENGHT)
	
	def update(self):
		self.screen.update()

	def update_score(self, player_1_score: int, player_2_score: int) -> None:
		self.scoreboard.update(player_1_score=player_1_score, player_2_score=player_2_score)

	def end_screen(self, player_number: int):
		self.update()

		end = t.Turtle()
		end.clear()
		end.home()
		end.pencolor(GAME_OVER_FONT_COLOR)
		end.write(
			"GAME OVER", 
			align=ALIGN,
			font=(FONT, GAME_OVER_FONT_SIZE, FONT_TYPE)
			)

		end.pencolor(FONT_COLOR)
		end.setheading(-90)
		end.forward(50)
		end.write(
			f"Player {player_number} won", 
			align=ALIGN,
			font=(FONT, FONT_SIZE, FONT_TYPE)
			)

		self.screen.exitonclick()
