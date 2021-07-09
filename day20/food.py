import turtle as t
import random as r

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600

X_MARGIN = 80
Y_MARGIN = 80

FOOD_COLOR = 'green'
FOOD_SHAPE = 'circle'
FOOD_SIZE = 10
STANDARD_SIZE = 20

TARGET_SIZE = 15

class Food(t.Turtle):

	def __init__(self) -> None:
		super().__init__()
		self.penup()
		self.shape(FOOD_SHAPE)
		self.shapesize(stretch_len=FOOD_SIZE/STANDARD_SIZE, stretch_wid=FOOD_SIZE/STANDARD_SIZE)
		self.color(FOOD_COLOR)
		self.speed(0)
		self.set()

	def get_position(self) -> tuple:
		return self.position()

	def clear_food(self) -> None:
		self.clear()

	def is_eaten(self, head: t.Turtle) -> bool:
		distance: float = self.distance(head)
		return distance < TARGET_SIZE

	def set(self) -> None:
		self.goto(
			x = r.randint(-(SCREEN_WIDTH - X_MARGIN)//2 , (SCREEN_WIDTH - X_MARGIN)//2 ),
			y = r.randint(-(SCREEN_HEIGHT - Y_MARGIN)//2 , (SCREEN_HEIGHT - Y_MARGIN)//2 )
			)