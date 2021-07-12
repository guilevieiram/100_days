import turtle as t
import random as r
import sys

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 400
TURTLE_SEPARATION = 50
X_MARGIN = - SCREEN_WIDTH//2 + 30

class TurtleRace():

	def __init__(self, number_players: int = 6, shape: str = 'turtle', speed: int = 5) -> None:
		self.number_players: int = number_players
		self.colors: list = ['red', 'yellow', 'purple', 'green', 'blue', 'black', 'orange', 'brown'][:number_players]
		self.turtles: list = [t.Turtle(shape=shape) for _ in range(number_players)]
		self.screen: t.Screen = t.Screen()
		self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
		self.bet: str = self.get_bet()

		colors = self.colors
		for turtle in self.turtles:
			color = r.choice(colors)
			colors.pop(colors.index(color))
			turtle.color(color)
			turtle.pencolor(color)
			turtle.speed(speed)
			turtle.penup()

	def get_bet(self) -> str:
		title: str = "Set your bet!"
		prompt: str = f'''Which turtle will win the race?\nEnter a color from the options: {', '.join(self.colors)}:'''
		answer: str = ''
		while answer not in self.colors:
			answer = self.screen.textinput(title=title, prompt=prompt)
		return answer

	def initialize_race(self) -> None:
		fixer: float = (not self.number_players % 2) / 2 
		for count, turtle in enumerate(self.turtles, start = - (self.number_players//2)):
			turtle.goto(x = X_MARGIN, y =  (count + fixer) * TURTLE_SEPARATION)

	def run(self, lower_bound: int = 1, higher_bound: int = 10) -> None:

		while not self.game_over()['is_over']:
			for turtle in self.turtles:
				turtle.forward(r.randint(lower_bound, higher_bound))
		else:
			winner = self.game_over()['winner']
			if winner.pencolor() == self.bet:
				print("\n\nYay! you have won the race!!!\n\n")
			else:
				print(f"\n\nNot this time... The {winner.pencolor()} turtle is the winner!\n\n")

		self.screen.exitonclick()

	def game_over(self) -> dict:
		over: bool = False
		for turtle in self.turtles:
			if turtle.xcor() >= - X_MARGIN: 
				over = True
				break

		return {
			'is_over': over,
			'winner': turtle
		}


def main():
	race = TurtleRace(number_players=int(sys.argv[1]), speed=3)
	race.initialize_race()
	race.run()

if __name__ == "__main__":
	main()