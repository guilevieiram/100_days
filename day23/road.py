import turtle as t
import random as r

'''
CONSTANTS
'''

from screen import SCREEN_WIDTH, SCREEN_HEIGHT

# Turtle defaults
STANDARD_SIZE = 20

# Positions
X_MARGIN = 0
Y_MARGIN = 200

X_MAX = (SCREEN_WIDTH - X_MARGIN)/2
Y_MAX = (SCREEN_HEIGHT - Y_MARGIN)/2


UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

# Car
CAR_WIDTH = 30
CAR_HEIGHT = 20
CAR_SHAPE = 'square'

# Road
INITIAL_NUMBER_CARS = 10
DEFAULT_STEP = 5
STEP_INCREMET = 5

# Spawn 
SPAWN = True
NO_SPAWN = False
SPAWN_FRAME = 10

class Car (t.Turtle):

	def __init__(self, step: int, color: tuple, random: bool = False) -> None:
		super().__init__()
		
		self.step: int = step

		self.shapesize(stretch_wid=CAR_HEIGHT/STANDARD_SIZE, stretch_len=CAR_WIDTH/STANDARD_SIZE)
		self.shape(CAR_SHAPE)
		self.color(color)
		self.setheading(LEFT)
		self.penup()
		if random:
			self.set_random_position()
		else:
			self.set_position()

	def move(self) -> None:
		if self.xcor() > - (X_MAX + CAR_WIDTH):
			self.forward(self.step)

	def out_of_bounds(self) -> bool:
		return self.xcor() < - (X_MAX + CAR_WIDTH)

	def set_position(self) -> None:
		x = X_MAX + CAR_WIDTH/2
		y = r.randint(-Y_MAX, +Y_MAX)
		self.goto(x=x, y=y)

	def set_random_position(self) -> None:
		x = r.randint(-X_MAX, +X_MAX)
		y = r.randint(-Y_MAX, +Y_MAX)
		self.goto(x=x, y=y)


class Road():

	def __init__(self, level = int) -> None:
		self.cars: list = []
		self.step = DEFAULT_STEP
		self.fill_road()

	def make_car(self, spawn_probability: float, frame: int) -> None:
		if r.choices(
			population=[SPAWN, NO_SPAWN],
			weights=[spawn_probability, 1-spawn_probability]
			) and not frame % SPAWN_FRAME:
			self.cars.append(Car(step=self.step, color=self.random_color()))

	def delete_car(self, car: Car) -> None:
		self.cars.pop(self.cars.index(car))

	def random_color(self) -> tuple:
		return (
			r.random(),
			r.random(),
			r.random()
			)

	def move_cars(self) -> None:
		for car in self.cars_out_of_bound():
			self.delete_car(car)
		for car in self.cars:
			car.move()

	def cars_out_of_bound(self) -> list:
		return [car for car in self.cars if car.out_of_bounds()]

	def increase_level(self) -> None:
		self.level += 1
		self.step += STEP_INCREMET

	def fill_road(self) -> None:
		for _ in range(INITIAL_NUMBER_CARS):
			self.cars.append(Car(step=self.step, color=self.random_color(), random = True))

