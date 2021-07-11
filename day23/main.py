import turtle as t
import time
from argparse import ArgumentParser


from screen import Screen
from player import Player
from road import Road

'''
CONSTANTS
'''

# Playability
FPS = 20
UPDATE_TIME = 1/FPS
TIME_BETWEEN_LEVELS = 1

# Difficulty
EASY = 'easy'
MEDIUM = 'medium'
HARD = 'hard'
DEFAULT = EASY

# Road
SPAWN_CAR_PROB = 1

# Home message
HOME_MESSAGE_TIME = 2
HOME_MESSAGE = '''TURTLE CROSSING
       \U0001F422'''

class TurtleCrossing():

	def __init__(self, difficulty: str, random_color: bool) -> None:
		# Screen setup
		self.screen: Screen = Screen(difficulty=difficulty)
		self.screen.home_screen(sleep_time=HOME_MESSAGE_TIME, message=HOME_MESSAGE)
		self.screen.draw_difficulty()

		# Game setup
		self.level = 0
		self.on = True
		self.increase_level()

		# Player setup
		self.player: Player = Player()

		# Road setup
		self.road: Road = Road(difficulty=difficulty, random_color=random_color)

		# Time setup
		self.frame = 0

		# Actions setup
		self.set_actions()

	def run(self) -> None:

		while self.on:

			time.sleep(UPDATE_TIME)
			self.road.move_cars()
			self.screen.update()
			self.increase_frame()

			if self.road.ran_over_player(player_position=self.player.position()):
				self.game_over()

			if self.player.crossed_road():
				self.reset()
				self.increase_level()
				self.screen.update()
				time.sleep(TIME_BETWEEN_LEVELS)


			self.road.make_car(spawn_probability=SPAWN_CAR_PROB,
								frame=self.frame)


	def game_over(self) -> None:
		self.screen.end_screen(level=self.level)	

	def increase_level(self) -> None:
		self.level += 1
		self.screen.update_score(level=self.level)

	def increase_frame(self) -> None:
		self.frame += 1

	def set_actions(self) -> None:
		self.screen.action(key='space', function=self.screen.close)
		self.screen.action(key='Up', function=self.player.move)

	def reset(self) -> None:
		self.screen.reset()
		self.player.reset()
		self.road.reset()

def setup_parser() -> ArgumentParser:
	parser = ArgumentParser()
	parser.add_argument('--difficulty', '-d', default=DEFAULT,
		type=str, help='set game difficulty (easy, medium, hard).\ndefault = medium')
	parser.add_argument('--randomColor', '-rc', default=False,
		action='store_true',
		help='Generates cars with random colors from the whole spectrum.')
	return parser

def main() -> None:

	parser = setup_parser()
	arguments = vars(parser.parse_args())

	tc: TurtleCrossing = TurtleCrossing(difficulty=arguments['difficulty'],
						random_color=arguments['randomColor'])
	
	try:
		tc.run()
	except:
		print('Game ended')

if __name__=="__main__":
	main()