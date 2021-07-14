from state_data import StateData
from screen import Screen

'''CONSTANTS'''

# Data
STATES_CSV_PATH = '50_states.csv'

# Game
GAME_NAME = 'US GUESS 🤮'

class GuessGame():

	def __init__(self):
		self.screen: Screen = Screen(game_name=GAME_NAME)

		self.states: StateData = StateData(csv_path=STATES_CSV_PATH)

		self.max_score: int = self.states.get_max_score()

		self.guess_list: list = []

		self.set_actions()

		self.score: int = 0

	def play(self) -> None:

		self.screen.update_score(score=self.score)
		while True:

			guess = self.screen.get_input(
			title='Guess the state!', 
			prompt='Guess another state name.')

			if self.is_guess_correct(guess=guess) and guess not in self.guess_list:
				
				self.guess_list.append(guess)
				position = self.states.get_position(name=guess)
				self.screen.write(position=position, message=guess)
				self.score += 1
				self.screen.update_score(score=self.score)
			
			if guess is None:
				self.screen.end_screen(score=self.score, win=False)
				break
			if self.score >= self.max_score:
				self.screen.end_screen(score=self.score, win=True)
				break

		t.mainloop()

	def is_guess_correct(self, guess: str) -> bool:
		return guess.lower() in self.states.names

	def set_actions(self) -> None:
		pass

def main() -> None:
	guess_game = GuessGame()
	guess_game.play()

if __name__ == "__main__":
	main()
