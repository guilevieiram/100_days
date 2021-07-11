import turtle as t
import time

from screen import Screen
from player import Player
from road import Road

'''
CONSTANTS
'''

# Playability
FPS = 20
UPDATE_TIME = 1/FPS

# Road
SPAWN_CAR_PROB = 1

class TurtleCrossing():

	def __init__(self) -> None:
		# Screen setup
		self.screen: Screen = Screen()

		# Game setup
		self.level = 0
		self.on = True
		self.update_level()

		# Player setup
		self.player: Player = Player()

		# Road setup
		self.road: Road = Road(level = self.level)

		# Time setup
		self.frame = 0

		# Actions setup
		self.set_actions()


	def run(self) -> None:

		while self.on:
			time.sleep(UPDATE_TIME)
			self.road.make_car(spawn_probability=SPAWN_CAR_PROB,
								frame=self.frame)
			self.road.move_cars()
			self.screen.update()
			self.increase_time()

	def game_over(self) -> None:
		self.screen.close()	

	def update_level(self) -> None:
		self.level += 1
		self.screen.update_score(level=self.level)

	def increase_time(self) -> None:
		self.frame += 1

	def set_actions(self) -> None:
		self.screen.action(key='space', function=self.screen.close)
		self.screen.action(key='Up', function=self.player.move)
		self.screen.action(key='c', function=self.road.move_cars)


def main() -> None:
	tc: TurtleCrossing = TurtleCrossing()
	tc.run()

if __name__=="__main__":
	main()