import turtle as t

'''
CONSTANTS
'''
from screen import X_MAX, Y_MAX

# Player shape
PLAYER_COLOR = 'green'
PLAYER_SHAPE = 'turtle'
PLAYER_WIDTH = 20 
PLAYER_HEIGHT = 20

# Player mechanics
STEP = 15
SPEED = 0

# Turtle defaults
STANDARD_SIZE = 20

# Directions
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

class Player(t.Turtle):

	def __init__(self) -> None:
		super().__init__()

		self.color(PLAYER_COLOR)
		self.shape(PLAYER_SHAPE)
		self.shapesize(stretch_wid=PLAYER_WIDTH/STANDARD_SIZE, stretch_len=PLAYER_HEIGHT/STANDARD_SIZE)
		self.speed(SPEED)
		self.penup()
		self.setheading(UP)
		self.goto(x=0, y=-Y_MAX)

	def move(self, step: int = STEP) -> None:
		if self.ycor() < Y_MAX:
			self.forward(step)

	def reset(self) -> None:
		self.goto(x=0, y=-Y_MAX)

	def crossed_road(self) -> bool:
		return self.ycor() >= Y_MAX
