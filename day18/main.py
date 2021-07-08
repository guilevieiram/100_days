import turtle as t
import random as r
# import colorgram

class MyTurtle(t.Turtle):

	def __init__(self, turtle_color: str = 'blue', pencolor: str = 'red', shape: str = 'turtle', pensize: int = 1, speed: int = 1):
		super().__init__()
		self.shape(shape)
		self.color(turtle_color)
		self.pensize(pensize)
		self.pencolor(pencolor)
		self.speed(speed)
		self.TURTLE_SIZE = 20

	def draw_square(self, lenght: int = 100) -> None:
		for _ in range(4):
			self.forward(lenght)
			self.right(90)

	def draw_dashed_line(self, dash_lenght: int = 10, total_lenght: int = 100) -> None:
		num_dashes = total_lenght//(dash_lenght * 2)
		for _ in range(num_dashes):
			self.forward(dash_lenght)
			self.penup()
			self.forward(dash_lenght)
			self.pendown()

	def draw_polygon(self, number_of_sides: int, side_lenght: int = 100) -> None:
		turning_angle = 360/number_of_sides
		for _ in range(number_of_sides):
			self.forward(side_lenght)
			self.right(turning_angle)

	def draw_polygons(self, max_number_of_sides: int, side_lenght: int = 100) -> None:
		for number_of_sides in range(3, max_number_of_sides):
			self.pencolor(self.get_random_color())
			self.draw_polygon(number_of_sides, side_lenght=side_lenght)

	def draw_random_walk(self, step_lenght: int = 10, number_of_steps: int = 50, 
		angle_choices: list = [90, -90, 0, 180]) -> None:
		for _ in range(number_of_steps):
			self.pencolor(self.get_random_color())
			self.right(r.choice(angle_choices))
			self.forward(step_lenght)

	def draw_spyrograph(self, radius: int = 100, number_of_steps: int = 100) -> None:
		turning_angle: float = 360/number_of_steps
		for _ in range(number_of_steps):
			self.pencolor(self.get_random_color())
			self.circle(radius)
			self.right(turning_angle)

	def herst_painting(self, painting_path: str, step_size: int = 100, number_of_colors: int = 10):
		# self.colors: list = colorgram.extract(painting_path, number_of_colors) 
		self.colors = [self.get_random_color() for _ in range(number_of_colors)]
		
		screen = t.Screen()
		width = screen.window_width()//2 - self.TURTLE_SIZE
		height = screen.window_height()//2 - self.TURTLE_SIZE

		self.penup()
		for x in range(-width, width, step_size):
			for y in range(-height, height, step_size):
				self.pencolor(r.choice(self.colors))
				self.goto(x,y)
				self.dot()

	def show(self):
		screen = t.Screen()
		screen.exitonclick()

	def get_random_color(self) -> str:
		red = r.randint(0,255)
		green = r.randint(0,255)
		blue = r.randint(0,255)
		return (red, green, blue)


def main() -> None:

	t.colormode(255)

	joana = MyTurtle(turtle_color='blue', speed=0, pensize=10)
	joana.herst_painting('spot_painting.jpg', number_of_colors=30, step_size=50)
	joana.show()

if __name__=='__main__':
	main()