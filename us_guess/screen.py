import turtle as t
import time

## CONSTANTS

# Screen

BACKGROUND_IMAGE = 'blank_states_img.gif'
BACKGROUND_IMAGE_SIZE = (725, 491)

SCREEN_WIDTH, SCREEN_HEIGHT = BACKGROUND_IMAGE_SIZE

X_MARGIN = 100
Y_MARGIN = 40

X_MAX = (SCREEN_WIDTH-X_MARGIN)//2
Y_MAX = (SCREEN_HEIGHT-Y_MARGIN)//2

SCOREBOARD_PADX = 80
SCOREBOARD_PADY = 0


# Text
FONT = 'courier'
FONT_SIZE = 10
FONT_COLOR = 'black'
FONT_TYPE = 'normal'
ALIGN = 'center'

SCOREBOARD_FONT_SIZE = 24
SCOREBOARD_FONT_TYPE = 'bold'
SCOREBOARD_ALIGN = 'center'

GAME_OVER_POSITION = (0,0)
GAME_OVER_FONT = FONT
GAME_OVER_FONT_SIZE = 50
GAME_OVER_FONT_COLOR = 'red'
GAME_OVER_FONT_TYPE = 'bold'
GAME_OVER_ALIGN = 'center'

GAME_OVER_WIN_TEXT = 'YOU WIN!!'
GAME_OVER_WIN_COLOR = 'green'
GAME_OVER_LOOSE_TEXT = 'YOU LOST'
GAME_OVER_LOOSE_COLOR = 'red'

FINAL_SCORE_POS = (0, -50)
FINAL_SCORE_FONT_SIZE = 30

HOME_FONT_COLOR = 'green'
HOME_ALIGN = 'center'
HOME_FONT_SIZE = 50
HOME_POSITION = (0, 0)



class Text(t.Turtle):

	def __init__(self):
		super().__init__()
		self.hideturtle()

	def write_message(self, position: tuple, message: str,
					font=FONT, font_size=FONT_SIZE, font_type=FONT_TYPE,
					font_color=FONT_COLOR, align=ALIGN) -> None:
		self.pencolor(font_color)
		self.penup()
		self.goto(position)
		self.write(
			message, 
			align=align, 
			font=(font, font_size, font_type)
			)

class Image():

	def __init__(self, path: str, name: str, size: tuple):
		self.path: str = path
		self.name: str = name
		self.size: tuple = size

	def get_size(self) -> tuple:
		return self.size

class Scoreboard(t.Turtle):

	def __init__(self) -> None:
		super().__init__()

		self.hideturtle()
		self.penup()
		self.goto(x=(X_MAX-SCOREBOARD_PADX),
					 y=(Y_MAX-SCOREBOARD_PADX))
		self.pendown()
		self.pencolor(FONT_COLOR)

	def update(self, score: int) -> None:
		self.clear()
		self.write(
			f"Points: {score}", 
			align=SCOREBOARD_ALIGN, 
			font=(FONT, SCOREBOARD_FONT_SIZE, SCOREBOARD_FONT_TYPE)
			)

	def hide(self) -> None:
		self.clear()

class Screen():

	def __init__(self, game_name: str) -> None:
		self.screen: t.Screen = t.Screen()

		self.image: Image = Image(BACKGROUND_IMAGE, 'us_states', size=BACKGROUND_IMAGE_SIZE)

		self.screen.setup(width=self.image.get_size()[0], height=self.image.get_size()[1])
		self.screen.title(game_name) 
		self.screen.tracer(0)
		self.screen.listen()

		self.text = Text()

		self.set_background_image()

		self.scoreboard: Scoreboard = Scoreboard()

		self.home_screen(sleep_time=2, message=game_name)


	def close(self) -> None:
		self.screen.bye()

	def action(self, key: str, function) -> None:
		self.screen.onkeypress(key=key, fun=function)
	
	def update(self):
		self.screen.update()

	def update_score(self, score: int) -> None:
		self.scoreboard.update(score=score)

	def reset(self) -> None:
		pass

	def set_background_image(self) -> None:
		self.screen.bgpic(self.image.path)

	def home_screen(self, sleep_time: float, message: str) -> None:

		self.text.write_message(
			message=message,
			position=HOME_POSITION,
			font_color=HOME_FONT_COLOR,
			align=HOME_ALIGN, 
			font_size=HOME_FONT_SIZE
			)

		self.update()

		time.sleep(sleep_time)

		self.text.clear()

	def end_screen(self, score: int, win: bool):

		self.scoreboard.hide()

		if win:
			message = GAME_OVER_WIN_TEXT
			font_color = GAME_OVER_WIN_COLOR
		if not win:
			message = GAME_OVER_LOOSE_TEXT
			font_color = GAME_OVER_LOOSE_COLOR

		self.text.write_message(
			position=GAME_OVER_POSITION,
			message=message,
			font=GAME_OVER_FONT,
			font_size=GAME_OVER_FONT_SIZE,
			font_type=GAME_OVER_FONT_TYPE,
			font_color=font_color,
			align=GAME_OVER_ALIGN
			)

		message = f"SCORE: {score}"
		position = FINAL_SCORE_POS

		self.text.write_message(
			position=position,
			message=message,
			font_size=FINAL_SCORE_FONT_SIZE,
			)

		self.screen.exitonclick()

	def get_input(self, title: str, prompt: str) -> str:
		return self.screen.textinput(
			title=title, prompt=prompt
			)

	def write(self, position: tuple, message: str) -> None:
		self.text.write_message(position=position, message=message)
