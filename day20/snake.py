import turtle as t
import time

SNAKE_COLOR = 'white'
SEGMENT_SHAPE = 'square'
SEGMENT_SIZE = 20
STEP_SIZE = SEGMENT_SIZE
STARTING_POS = (0, 0)
STARTING_SNAKE_SIZE = 3

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600

MAX_X = (SCREEN_WIDTH-SEGMENT_SIZE)//2
MAX_Y = (SCREEN_HEIGHT-SEGMENT_SIZE)//2

COLISION_DISTANCE = SEGMENT_SIZE - 1

class Segment(t.Turtle):

	def __init__(self) -> None:
		super().__init__()
		self.shape(SEGMENT_SHAPE)
		self.penup()
		self.speed(0)
		self.color(SNAKE_COLOR)

class Snake():

	def __init__(self) -> None:
		self.snake = []
		for _ in range(STARTING_SNAKE_SIZE): self.add_segment()
		self.head: Segment = self.snake[0]

	def add_segment(self) -> None:
		segment = Segment()
		if not self.snake:
			segment.goto(STARTING_POS)
		else: 
			snakes_last_segment_position = self.snake[-1].position()
			segment.goto(snakes_last_segment_position - (SEGMENT_SIZE, 0))
		self.snake.append(segment)

	def move(self, step: int = STEP_SIZE) -> None:
		lenght = len(self.snake)
		for seg_num in range(1, lenght)[::-1]:
			self.snake[seg_num].goto(self.snake[seg_num - 1].position())
		self.head.forward(step)

	def turn(self, direction: float) -> None:
		if not (self.head.heading() - direction) % 180 == 0:
			self.head.setheading(direction)

	def colision_with_wall(self) -> bool:
		x, y = self.head.position()
		return not (abs(x) < MAX_X and abs(y) < MAX_Y)

	def colision_with_itself(self) -> bool:
		return True in [self.head.distance(segment) < COLISION_DISTANCE for segment in self.snake[1:]]