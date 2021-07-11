import time
import sys
import random as r
from argparse import ArgumentParser

from constants import *
from screen import Screen
from player import Player
from ball import Ball

class Pong:

	def __init__(self, max_score_number: int, difficulty: str = DEFAULT) -> None:

		# Screen setup
		self.screen: Screen = Screen()

		# Pad setup
		self.player_1: Player = Player(LEFT_PAD_POS)
		self.player_2: Player = Player(RIGHT_PAD_POS)

		# Ball setup
		self.ball: Ball = Ball(difficulty) 

		# Actions setup
		self.set_actions()

		# Game setup
		self.on: bool = True
		self.max_score_number: int = max_score_number
		
	def run(self) -> None:

		# self.screen.enable_movement()

		self.screen.update_score(self.player_1.score, self.player_2.score)

		self.ball.set_direction(r.choice([LEFT, RIGHT]))

		while self.on:

			# Moves ball and updates screen
			self.ball.move()
			self.screen.update()
			time.sleep(UPDATE_TIME)

			# Checking game over

			if self.player_1.score >= self.max_score_number:
				self.game_over(player_number=1)

			if self.player_2.score >= self.max_score_number:
				self.game_over(player_number=2)

			# Checking collisions with pad or wall

			if (self.ball.colision_with_pad(self.player_1.position()) or
			 self.ball.colision_with_pad(self.player_2.position()) ):
				self.ball.bounce_on_pad()

			if self.ball.colision_with_wall():
				self.ball.bounce_on_wall()

			# Checking ball out of bounds (scores a point)

			out_of_bounds: str = self.ball.out_of_bounds()
			if out_of_bounds == LEFT:
				self.player_1.increase_score()

			if out_of_bounds == RIGHT:
				self.player_2.increase_score()

			if out_of_bounds == LEFT or out_of_bounds == RIGHT:
				self.screen.update_score(self.player_1.score, self.player_2.score)
				self.player_1.reset(LEFT_PAD_POS)
				self.player_2.reset(RIGHT_PAD_POS)
				self.next_match()
				self.screen.update()
				time.sleep(TIME_BETWEEN_MATCHES)

	def game_over(self, player_number: int = 0) -> None:
		self.ball.hide()
		if not player_number == 0:
			self.screen.end_screen(player_number)
		else:
			self.screen.close()

	def next_match(self) -> None:
		self.ball.restart()

	def set_actions(self) -> None:
		# Moving actions
		self.screen.action(key='w', function=self.player_1.move_up)
		self.screen.action(key='s', function=self.player_1.move_down)
		self.screen.action(key='Up', function=self.player_2.move_up)
		self.screen.action(key='Down', function=self.player_2.move_down)

		# Kill app
		self.screen.action(key='space', function=self.game_over)

def setup_parser() -> ArgumentParser:
	parser = ArgumentParser()
	parser.add_argument('--difficulty', '-d', default=DEFAULT,
		type=str, help='set game difficulty (easy, medium, hard).\ndefault = medium')
	parser.add_argument('--matches', '-m', type=int, default=DEFAULT_MATCHES,
	 	help='set number of matches for a win.\ndefault = 5')
	return parser

def main() -> None:

	parser = setup_parser()
	arguments = vars(parser.parse_args())

	pong: Pong = Pong(max_score_number=arguments['matches'],
	 					difficulty=arguments['difficulty'])
	try:
		pong.run()
	except:
		pass

if __name__ == '__main__':
	main()