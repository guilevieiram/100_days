import turtle as t
import time
import os
from snake import Snake
from food import Food
from scoreboard import Scoreboard

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600
SCREEN_COLOR = 'black'
GAME_NAME = 'Snake Game'

FRAME_RATE = 10
UPDATE_TIME = 1/FRAME_RATE

UP = 90
DOWN = -90
LEFT = 180
RIGHT = 0

class SnakeGame():

	def __init__(self) -> None:
		'''Setup game screen'''
		self.screen: t.Screen = t.Screen()
		self.screen.setup(width=SCREEN_WIDTH, height = SCREEN_HEIGHT)
		self.screen.bgcolor(SCREEN_COLOR)
		self.screen.title(GAME_NAME)
		self.screen.tracer(0)
		self.screen.listen()

		'''Setup Snake'''
		self.snake: Snake = Snake()
		self.screen.update()

		'''Food Settings'''
		self.food: Food = Food()

		'''Scoreboard settings'''
		self.scoreboard: Scoreboard = Scoreboard()

		'''Game settings'''
		self.game_on: bool = True
		self.points: int = 0

	def run(self) -> None:
		while self.game_on:

			'''Checking collisions with wall and tail'''
			if self.snake.colision_with_wall() or self.snake.colision_with_itself():
				self.end_game()

			'''Food dynamic'''
			if self.food.is_eaten(self.snake.head):
				self.points += 1
				self.snake.add_segment()
				self.scoreboard.increase_score()
				self.food.clear()
				self.food.set()

			'''Quit game action'''
			self.screen.onkey(key='space', fun=lambda : self.end_game())

			'''Moving actions'''
			self.screen.onkey(key='Up', fun=lambda : self.snake.turn(UP))
			self.screen.onkey(key='Down', fun=lambda : self.snake.turn(DOWN))
			self.screen.onkey(key='Left', fun=lambda : self.snake.turn(LEFT))
			self.screen.onkey(key='Right', fun=lambda : self.snake.turn(RIGHT))
			self.screen.onkey(key='p', fun=lambda : self.snake.add_segment()) #dev purposes only

			'''Moving'''
			self.snake.move()
			self.screen.update()
			time.sleep(UPDATE_TIME)

	def end_game(self) -> None:
		self.scoreboard.game_over()
		self.game_on = False
		self.screen.exitonclick()

def main() -> None:
	sg: SnakeGame = SnakeGame()
	sg.run()
	try:
		os.system("cls")
	except:
		pass
	try:
		os.system("clear")
	except:
		pass

if __name__ == "__main__":
	main()