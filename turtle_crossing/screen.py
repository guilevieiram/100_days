import turtle as t
import time

## CONSTANTS



# Screen
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500

X_MARGIN = 50
Y_MARGIN = 100

X_MAX = (SCREEN_WIDTH-X_MARGIN)//2
Y_MAX = (SCREEN_HEIGHT-Y_MARGIN)//2

SCOREBOARD_PADX = 0
SCOREBOARD_PADY = 0

SCREEN_COLOR = 'light gray'

# Text
FONT = 'courier'
FONT_SIZE = 15
FONT_COLOR = 'black'
FONT_TYPE = 'bold'
ALIGN = 'left'

GAME_OVER_FONT_SIZE = 50
GAME_OVER_FONT_COLOR = 'red'
GAME_OVER_ALIGN = 'center'

DIFFICULTY_ALIGN = 'right'
DIFFICULTY_PADX = 0
DIFFICULTY_PADY = 0

HOME_FONT_COLOR = 'green'
HOME_ALIGN = 'center'
HOME_FONT_SIZE = 50
HOME_POSITION = (0, -50)

# Road margins
ROAD_X_MARGIN = 0
ROAD_Y_MARGIN = 200
ROAD_X_MAX = (SCREEN_WIDTH - ROAD_X_MARGIN)//2
ROAD_Y_MAX = (SCREEN_HEIGHT - ROAD_Y_MARGIN)//2

MARGIN_COLOR = 'black'
MARGIN_WIDTH = 2
MARGIN_PAD = 20

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

	def update(self, level: int) -> None:
		self.clear()
		self.write(
			f"LEVEL: {level}", 
			align=ALIGN, 
			font=(FONT, FONT_SIZE, FONT_TYPE)
			)

	def hide(self) -> None:
		self.clear()

class Margin(t.Turtle):

	def __init__(self, height: tuple) -> None:
		super().__init__()
		self.hideturtle()
		self.penup()
		self.pencolor(MARGIN_COLOR)
		self.pensize(MARGIN_WIDTH)
		self.setheading(0)
		self.goto(x=-SCREEN_WIDTH/2, y=height)

	def draw(self):
		self.hideturtle()
		self.pendown()
		self.forward(SCREEN_WIDTH)

class Difficulty(t.Turtle):

	def __init__(self, difficulty: str) -> None:
		super().__init__()

		self.difficulty: str = difficulty.upper()

		self.hideturtle()
		self.penup()
		self.goto(x=(X_MAX-DIFFICULTY_PADX),
					 y=(Y_MAX-DIFFICULTY_PADX))
		self.pendown()
		self.pencolor(FONT_COLOR)

	def draw(self) -> None:		
		self.clear()
		self.write(
			f"DIFFICULTY: {self.difficulty}", 
			align=DIFFICULTY_ALIGN, 
			font=(FONT, FONT_SIZE, FONT_TYPE)
			)

	def hide(self) -> None:
		self.clear()

class Screen():

	def __init__(self, difficulty: str) -> None:
		self.screen: t.Screen = t.Screen()

		self.screen.setup(width=SCREEN_WIDTH,
						 height = SCREEN_HEIGHT)
		self.screen.bgcolor(SCREEN_COLOR)
		self.screen.title(GAME_NAME) 
		self.screen.tracer(0)
		self.screen.listen()

		self.draw_road_margins()

		self.scoreboard: Scoreboard = Scoreboard()

		self.difficulty: Difficulty = Difficulty(difficulty=difficulty)

	def close(self) -> None:
		self.screen.bye()

	def action(self, key: str, function) -> None:
		self.screen.onkeypress(key=key, fun=function)
	
	def update(self):
		self.screen.update()

	def update_score(self, level: int) -> None:
		self.scoreboard.update(level=level)

	def draw_road_margins(self) -> None:
		top_margin = Margin(height= +(ROAD_Y_MAX+MARGIN_PAD))
		bottom_margin = Margin(height= -(ROAD_Y_MAX+MARGIN_PAD))
		top_margin.draw()
		bottom_margin.draw()

	def draw_difficulty(self) -> None:
		self.difficulty.draw()

	def reset(self) -> None:
		pass

	def home_screen(self, sleep_time: float, message: str) -> None:
		home = t.Turtle()
		home.pencolor(HOME_FONT_COLOR)
		home.hideturtle()
		home.penup()
		home.goto(HOME_POSITION)
		home.pendown()
		home.write(
			message, 
			align=HOME_ALIGN, 
			font=(FONT, HOME_FONT_SIZE, FONT_TYPE)
			)

		self.update()

		time.sleep(sleep_time)

		home.clear()

	def end_screen(self, level: int):

		self.scoreboard.hide()
		self.difficulty.hide()

		end = t.Turtle()
		end.clear()
		end.home()
		end.pencolor(GAME_OVER_FONT_COLOR)
		end.write(
			"GAME OVER", 
			align=GAME_OVER_ALIGN,
			font=(FONT, GAME_OVER_FONT_SIZE, FONT_TYPE)
			)

		end.pencolor(FONT_COLOR)
		end.setheading(-90)
		end.forward(50)
		end.write(
			f"SCORE: {level}", 
			align=GAME_OVER_ALIGN,
			font=(FONT, 2 * FONT_SIZE, FONT_TYPE)
			)

		self.screen.exitonclick()
