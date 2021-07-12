import turtle as t

class SketchApp(t.Turtle):

	def __init__(self, turtle_color: str = 'blue', pencolor: str = 'red', 
		shape: str = 'turtle', pensize: int = 1, speed: int = 1,
		step: int = 10, angular_step: float = 5) -> None:

		super().__init__()
		self.shape(shape)
		self.color(turtle_color)
		self.pensize(pensize)
		self.pencolor(pencolor)
		self.speed(speed)
		self.step = step
		self.angular_step = angular_step

	def run(self) -> None:
		screen = t.Screen()
		self.event_loop(screen)
		screen.exitonclick()

	def event_loop(self, screen: t.Screen) -> None:
		def clear() -> None:
			self.home()
			self.clear()

		screen.listen()
		screen.onkeypress(key='w', fun=lambda : self.forward(self.step))
		screen.onkeypress(key='s', fun=lambda : self.backward(self.step))
		screen.onkeypress(key='a', fun=lambda : self.left(self.angular_step))
		screen.onkeypress(key='d', fun=lambda : self.right(self.angular_step))
		screen.onkeypress(key='space', fun=lambda : screen.bye())
		screen.onkeypress(key='c', fun=clear)



def main() -> None:
	skapp = SketchApp(turtle_color='green', pencolor='black', speed = 0)
	skapp.run()

if __name__ == "__main__":
	main()