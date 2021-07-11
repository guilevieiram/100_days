import turtle as t
import random as r
from constants import *

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
