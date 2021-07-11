import turtle as t
import random as r
from constants import *

class Ball(t.Turtle):

	def __init__(self, difficulty: str) -> None:
		super().__init__()

		self.shape(BALL_SHAPE)
		self.shapesize(stretch_wid=BALL_SIZE/STANDARD_SIZE, stretch_len=BALL_SIZE/STANDARD_SIZE)
		self.color(BALL_COLOR)
		self.speed(BALL_SPEED)
		self.penup()
		self.home()

		self.step = self.set_dificulty(difficulty)

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

	def move(self, step: int = 0) -> None:
		if step == 0:
			step = self.step 
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

	def set_dificulty(self, difficulty: str) -> int:
		if difficulty == EASY: return EASY_MODE
		elif difficulty == MEDIUM: return MEDIUM_MODE
		elif difficulty == HARD: return HARD_MODE
		else: return MEDIUM_MODE