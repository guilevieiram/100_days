import turtle as t
import random as r
import time
import sys

'''Screen constants'''
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
X_MARGIN = 60
Y_MARGIN = 20
X_MAX = (SCREEN_WIDTH - X_MARGIN)//2 
Y_MAX = (SCREEN_HEIGHT - Y_MARGIN)//2 
SCREEN_COLOR = 'black'

ELEMENTS_COLOR = 'white'
ELEMENTS_WIDTH = 5
DASHES_LENGHT = 5

'''Game constants'''
GAME_NAME = 'Guile Pong'
TIME_BETWEEN_MATCHES = 1

'''Pad constants'''
PAD_HEIGHT = 60
PAD_WIDTH = 10
RIGHT_PAD_POS = ((SCREEN_WIDTH-X_MARGIN)//2,0)
LEFT_PAD_POS = (-(SCREEN_WIDTH-X_MARGIN)//2,0)

PAD_COLOR = 'white'
PAD_SPEED = 0
PAD_SHAPE = 'square'

PAD_STEP = 10

'''String constants'''
LEFT = 'left'
RIGHT = 'right'
NONE = ''

EASY = 'easy'
MEDIUM = 'medium'
HARD = 'hard'
DEFAULT = MEDIUM

'''Ball constants'''
BALL_SIZE = 10
BALL_SHAPE = 'circle'
BALL_COLOR = 'white'
BALL_SPEED = 0
BALL_STEP = 5

MIN_ANGLE = 20

'''Scoreboard constants'''
FONT_COLOR = 'white'
ALIGN = 'center'
FONT = 'courier'
FONT_SIZE = 30
FONT_TYPE = 'bold'

GAME_OVER_FONT_SIZE = 50
GAME_OVER_FONT_COLOR = 'red'

SCOREBOARD_PADY = 50

'''Turtle constants'''
STANDARD_SIZE = 20

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

class Player():
	def __init__(self, position: tuple) -> None:
		self.pad: Pad = Pad(position)
		self.score: int = 0

	def move_up(self) -> None:
		self.pad.up()

	def move_down(self) -> None:
		self.pad.down()

	def increase_score(self) -> None:
		self.score += 1

	def position(self) -> tuple:
		return self.pad.position()

	def reset(self, position_tuple) -> None:
		self.pad.reset(position_tuple)

class Ball(t.Turtle):

	def __init__(self) -> None:
		super().__init__()

		self.shape(BALL_SHAPE)
		self.shapesize(stretch_wid=BALL_SIZE/STANDARD_SIZE, stretch_len=BALL_SIZE/STANDARD_SIZE)
		self.color(BALL_COLOR)
		self.speed(BALL_SPEED)
		self.penup()
		self.home()

	def restart (self) -> None:
		self.home()
		self.set_direction(r.choice([LEFT, RIGHT]))
		self.move()

	def set_direction(self, side: str) -> None:

		angle_opening: float = (180 - 2 * MIN_ANGLE)
		direction: float = r.random() * angle_opening - angle_opening/2

		if side == LEFT:
			direction = direction - 180

		self.setheading(direction)
		

	def bounce_on_pad(self) -> None:
		direction: float = self.heading()

		if direction > 90 and direction < 270 :
			self.set_direction(side = RIGHT)
		else: # ball heading left
			self.set_direction(side = LEFT)

		self.move(step=PAD_WIDTH)

	def bounce_on_wall(self) -> None:
		direction: float = self.heading()
		direction = - direction
		self.setheading(direction)
		self.move()

	def move(self, step: int = BALL_STEP) -> None:
		self.forward(step)

	def colision_with_wall(self) -> bool:
		x_ball, y_ball = self.position()
		return abs(y_ball) >= Y_MAX 

	def colision_with_pad(self, pad_position: tuple) -> bool:
		x_ball, y_ball = self.position()
		x_pad, y_pad = pad_position
		return abs(x_ball-x_pad) < PAD_WIDTH/2 and abs(y_ball-y_pad) < PAD_HEIGHT/2

	def out_of_bounds(self) -> str:
		x_ball, y_ball = self.position()

		if x_ball >= +X_MAX:
			return LEFT
		elif x_ball <= -X_MAX:
			return RIGHT
		else:
			return NONE 

	def hide(self) -> None:
		self.hideturtle()

class Pad(t.Turtle):
	
	def __init__(self, position: tuple) -> None:
		super().__init__()
		
		self.penup()
		self.color(PAD_COLOR)
		self.speed(PAD_SPEED)	
		self.shape(PAD_SHAPE)
		self.setheading(90)
		self.shapesize(stretch_wid=PAD_WIDTH/STANDARD_SIZE, stretch_len=PAD_HEIGHT/STANDARD_SIZE)
		self.goto(position)

	def up(self) -> None:
		if self.ycor() < +(Y_MAX - PAD_HEIGHT/2):
			self.forward(PAD_STEP)

	def down(self) -> None:
		if self.ycor() > -(Y_MAX - PAD_HEIGHT/2):
			self.backward(PAD_STEP)

	def reset(self, position: tuple) -> None:
		self.goto(position)

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

class Pong:

	def __init__(self, max_score_number: int, difficulty: str = DEFAULT) -> None:

		# Screen setup
		self.screen: Screen = Screen()

		# Pad setup
		self.player_1: Player = Player(LEFT_PAD_POS)
		self.player_2: Player = Player(RIGHT_PAD_POS)

		# Ball setup
		self.ball: Ball = Ball() 

		# Actions setup
		self.set_actions()

		# Game setup
		self.on: bool = True
		self.max_score_number: int = max_score_number
		self.FPS = self.set_fps(difficulty)
		self.UPDATE_TIME = 1/self.FPS

	def run(self) -> None:

		# self.screen.enable_movement()

		self.screen.update_score(self.player_1.score, self.player_2.score)

		self.ball.set_direction(r.choice([LEFT, RIGHT]))

		while self.on:

			# Moves ball and updates screen
			self.ball.move()
			self.screen.update()
			time.sleep(self.UPDATE_TIME)

			# Checking game over

			if self.player_1.score >= self.max_score_number:
				self.game_over(player_number=1)

			if self.player_2.score >= self.max_score_number:
				self.game_over(player_number=2)

			# Checking collisions with pad or wall

			if (self.ball.colision_with_pad(self.player_1.position()) or
			 self.ball.colision_with_pad(self.player_2.position()) ):
				self.ball.bounce_on_pad()

			if self.ball.colision_with_wall():
				self.ball.bounce_on_wall()

			# Checking ball out of bounds (scores a point)

			out_of_bounds: str = self.ball.out_of_bounds()
			if out_of_bounds == LEFT:
				self.player_1.increase_score()

			if out_of_bounds == RIGHT:
				self.player_2.increase_score()

			if out_of_bounds == LEFT or out_of_bounds == RIGHT:
				self.screen.update_score(self.player_1.score, self.player_2.score)
				self.player_1.reset(LEFT_PAD_POS)
				self.player_2.reset(RIGHT_PAD_POS)
				self.next_match()
				self.screen.update()
				time.sleep(TIME_BETWEEN_MATCHES)

	def game_over(self, player_number: int = 0) -> None:
		self.ball.hide()
		if not player_number == 0:
			self.screen.end_screen(player_number)
		else:
			self.screen.close()

	def next_match(self) -> None:
		self.ball.restart()

	def set_fps(self, difficulty: str) -> int:
		if difficulty == EASY: return 50
		if difficulty == MEDIUM: return 70
		if difficulty == HARD: return 90

	def set_actions(self) -> None:
		# Moving actions
		self.screen.action(key='w', function=self.player_1.move_up)
		self.screen.action(key='s', function=self.player_1.move_down)
		self.screen.action(key='Up', function=self.player_2.move_up)
		self.screen.action(key='Down', function=self.player_2.move_down)

		# Kill app
		self.screen.action(key='space', function=self.game_over)

def main() -> None:
	max_score_number = int(sys.argv[1])
	difficulty = sys.argv[2].lower()

	pong: Pong = Pong(max_score_number=max_score_number, difficulty=difficulty)

	try:
		pong.run()
	except:
		pass

if __name__ == '__main__':
	main()