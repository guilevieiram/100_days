import turtle as t

## CONSTANTS

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

X_MARGIN = 50
Y_MARGIN = 100

X_MAX = (SCREEN_WIDTH-X_MARGIN)/2
Y_MAX = (SCREEN_HEIGHT-Y_MARGIN)/2

SCOREBOARD_PADX = 0
SCOREBOARD_PADY = 0

SCREEN_COLOR = 'white'

# Text
FONT = 'courier'
FONT_SIZE = 12
FONT_COLOR = 'black'
FONT_TYPE = 'bold'
ALIGN = 'left'
GAME_OVER_FONT_SIZE = 50

# Game
GAME_NAME = 'Turtle crossing'

class Scoreboard(t.Turtle):

	def __init__(self) -> None:
		super().__init__()

		self.hideturtle()
		self.penup()
		self.goto(x=-(X_MAX-SCOREBOARD_PADX),
					 y=(Y_MAX-SCOREBOARD_PADX))
		self.pendown()
		self.pencolor(FONT_COLOR)

	def update(self, level: int):
		self.clear()
		self.write(
			f"LEVEL: {level}", 
			align=ALIGN, 
			font=(FONT, FONT_SIZE, FONT_TYPE)
			)

class Screen():

	def __init__(self) -> None:
		self.screen: t.Screen = t.Screen()

		self.screen.setup(width=SCREEN_WIDTH,
						 height = SCREEN_HEIGHT)
		self.screen.bgcolor(SCREEN_COLOR)
		self.screen.title(GAME_NAME) 
		self.screen.tracer(0)
		self.screen.listen()

		self.scoreboard: Scoreboard = Scoreboard()

	def close(self) -> None:
		self.screen.bye()

	def action(self, key: str, function) -> None:
		self.screen.onkeypress(key=key, fun=function)
	
	def update(self):
		self.screen.update()

	def update_score(self, level: int) -> None:
		self.scoreboard.update(level=level)

	def end_screen(self, level: int):
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
			f"Score: {level}", 
			align=ALIGN,
			font=(FONT, FONT_SIZE, FONT_TYPE)
			)

		self.screen.exitonclick()
