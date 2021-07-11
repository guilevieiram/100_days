import turtle as t
import random as r

'''
CONSTANTS
'''

from screen import ROAD_X_MAX, ROAD_Y_MAX
from player import PLAYER_WIDTH, PLAYER_HEIGHT

# Turtle defaults
STANDARD_SIZE = 20

# Positions
X_MAX = ROAD_X_MAX
Y_MAX = ROAD_Y_MAX

UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

# Colors
COLORS = ['black', 'green', 'blue', 'yellow', 'red',
			'orange', 'purple']

# Car
CAR_WIDTH = 50
CAR_HEIGHT = 30
CAR_SHAPE = 'square'

# Road
INITIAL_NUMBER_CARS = 5

# Difficulty settings
DEFAULT_STEP = 5
DEFAULT_SPAWN_FRAME = 20

EASY_STEP = 5
EASY_SPAWN_FRAME = 25

MEDIUM_STEP = 10
MEDIUM_SPAWN_FRAME = 15

HARD_STEP = 15
HARD_SPAWN_FRAME = 10

STEP_INCREMET = 2
SPAWN_FRAME_REDUCTION_FACTOR = 1.3

# Spawn 
SPAWN = True
NO_SPAWN = False

# Difficulty
EASY = 'easy'
MEDIUM = 'medium'
HARD = 'hard'
DEFAULT = MEDIUM


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

	def hit(self, player_position: tuple) -> bool:
		hit = False

		x_player, y_player = player_position

		if (abs(self.xcor() - x_player) < (CAR_WIDTH+PLAYER_WIDTH)/2 and
			abs(self.ycor() - y_player) < (CAR_HEIGHT+PLAYER_HEIGHT)/2):
				hit = True

		return hit

	def update_step(self, step: int) -> None:
		self.step: int = step

class Road():

	def __init__(self, difficulty: str, random_color: bool) -> None:
		step, spawn_frame = self.set_difficulty(difficulty)

		self.random_color: bool = random_color

		self.cars: list = []
		self.step: int = step
		self.spawn_frame: int = spawn_frame 
		self.fill_road()
		self.top_margin = +Y_MAX
		self.bottom_margin = -Y_MAX

	def make_car(self, spawn_probability: float, frame: int) -> None:

		if r.choices(
			population=[SPAWN, NO_SPAWN],
			weights=[spawn_probability, 1-spawn_probability]
			) and not frame % int(self.spawn_frame):
			self.cars.append(Car(step=self.step, color=self.get_color()))

	def delete_car(self, car: Car) -> None:
		self.cars.pop(self.cars.index(car))

	def get_color(self) -> tuple:
		if self.random_color:
			color = (r.random(), r.random(), r.random())
		else:
			color = r.choice(COLORS)
		return color

	def move_cars(self) -> None:
		self.delete_cars_out_of_bound()

		for car in self.cars:
			car.move()

	def delete_cars_out_of_bound(self) -> list:
		for car in self.cars:
			if car.xcor() < - (X_MAX + CAR_WIDTH):
				self.delete_car(car)

	def increase_level(self) -> None:
		self.step += STEP_INCREMET
		self.spawn_frame = self.spawn_frame//SPAWN_FRAME_REDUCTION_FACTOR

	def fill_road(self) -> None:
		for _ in range(INITIAL_NUMBER_CARS):
			self.cars.append(Car(step=self.step, color=self.get_color(), random = True))

	def ran_over_player(self, player_position: tuple) -> bool:
		ran_over = False
		for car in self.cars:
			if car.hit(player_position):
				ran_over = True
				break
		return ran_over

	def reset(self) -> None:
		self.increase_level()
		for car in self.cars:
			car.update_step(step=self.step)

	def set_difficulty(self, difficulty: str) -> tuple:
		step: int
		spawn_frame: int

		if difficulty == EASY:
			step = EASY_STEP
			spawn_frame = EASY_SPAWN_FRAME
		elif difficulty == MEDIUM:
			step = MEDIUM_STEP
			spawn_frame = MEDIUM_SPAWN_FRAME
		elif difficulty == HARD:
			step = HARD_STEP
			spawn_frame = HARD_SPAWN_FRAME
		else:
			step = DEFAULT_STEP
			spawn_frame = DEFAULT_SPAWN_FRAME

		return step, spawn_frame