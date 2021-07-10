'''
How to make the pong game:
1. make the screen OKEY
2. make the pads OKEY
3. make the ball OKEY
4. implement the player class from pads OKEY
5. implement bouncing action (from wall and from paddle)
6. implement out of bounds 
7. make scoreboard
'''

import turtle as t
import random as r

'''Screen constants'''
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
X_MARGIN = 20
Y_MARGIN = 20
X_MAX = (SCREEN_WIDTH - X_MARGIN)//2 
Y_MAX = (SCREEN_HEIGHT - Y_MARGIN)//2 
SCREEN_COLOR = 'black'

ELEMENTS_COLOR = 'white'
ELEMENTS_WIDTH = 5
DASHES_LENGHT = 10

'''Game constants'''
GAME_NAME = 'Guile Pong'

'''Pad constants'''
PAD_HEIGHT = 50
PAD_WIDTH = 10
RIGHT_PAD_POS = ((SCREEN_HEIGHT-X_MARGIN)/2,0)
LEFT_PAD_POS = (-(SCREEN_HEIGHT-X_MARGIN)/2,0)

PAD_COLOR = 'white'
PAD_SPEED = 6
PAD_SHAPE = 'square'

PAD_STEP = 5

'''Ball constants'''
BALL_SIZE = 10
BALL_SHAPE = 'square'
BALL_COLOR = 'white'
BALL_SPEED = 1
MAX_DISTANCE = 10 * SCREEN_WIDTH

'''Turtle constants'''
STANDARD_SIZE = 20

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

	def colision(self, ball_position: tuple) -> bool:
		return self.pad.colision(ball_position)

class Ball(t.Turtle):

	def __init__(self) -> None:
		super().__init__()

		self.shape(BALL_SHAPE)
		self.shapesize(stretch_wid=BALL_SIZE/STANDARD_SIZE, stretch_len=BALL_SIZE/STANDARD_SIZE)
		self.color(BALL_COLOR)
		self.speed(BALL_SPEED)
		self.penup()
		self.home()

	def start_moving(self) -> None:
		theta: int = r.random() * 360
		self.setheading(theta)
		self.forward(MAX_DISTANCE)
		

	def bounce_on_pad(self) -> None:
		direction: tuple = self.heading()
		print(direction)

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
		self.forward(PAD_STEP)

	def down(self) -> None:
		self.backward(PAD_STEP)

	def colision(self, ball_position: tuple) -> bool:
		x_ball, y_ball = ball_position
		x_pad, y_pad = self.position()
		return abs(x_ball-x_pad) < PAD_WIDTH or abs(y_ball-y_pad) < PAD_HEIGHT

class Screen():

	def __init__(self) -> None:
		self.screen: t.Screen = t.Screen()
		self.screen.setup(width=SCREEN_WIDTH, height = SCREEN_HEIGHT)
		self.screen.bgcolor(SCREEN_COLOR)
		self.screen.title(GAME_NAME) 
		self.screen.tracer(0)
		self.draw_dashed_line()
		self.screen.listen()

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

class Pong:

	def __init__(self) -> None:

		# Screen setup
		self.screen: Screen = Screen()

		# Pad setup
		self.player_1: Player = Player(LEFT_PAD_POS)
		self.player_2: Player = Player(RIGHT_PAD_POS)

		# Ball setup
		self.ball: Ball = Ball() 

		# Actions setup
		self.set_actions()

		# Game state setup
		self.on = True

	def run(self) -> None:

		self.screen.enable_movement()

		self.ball.start_moving()

		while self.on:

			if self.player_1.colision(self.ball.position()) or self.player_2.colision(self.ball.position()):
				self.ball.bounce_on_pad()
				print('colision')

			self.screen.update()

	def game_over(self) -> None:
		self.screen.update()
		self.screen.close()

	def set_actions(self) -> None:
		# Moving actions
		self.screen.action(key='w', function=self.player_1.move_up)
		self.screen.action(key='s', function=self.player_1.move_down)
		self.screen.action(key='Up', function=self.player_2.move_up)
		self.screen.action(key='Down', function=self.player_2.move_down)

		# Kill app
		self.screen.action(key='space', function=self.game_over)


if __name__ == '__main__':
	pong: Pong = Pong()
	pong.run()
