from data_manager import DataManager, LocalDataManager
from data_manager import Generator, PasswordGenerator
from screen import Screen, TkScreen

"""CONSTANTS"""
# Data
STORAGE_FILE = "data.txt"

class PasswordManager():

	def __init__(self) -> None:
		
		self.password_generator: PasswordGenerator = PasswordGenerator(
			password_size=20
			)

		self.screen: Screen = TkScreen(
			add_password_button_function=self.add_password_button_function,
			generate_random_password_function=self.generate_random_password_function
			)

		self.data_manager: DataManager = LocalDataManager(
			storage_file=STORAGE_FILE
			)

	def run(self) -> None:
		self.screen.make()

	def add_password_button_function(self) -> None:
		
		if not self.screen.field_empty() and self.screen.confirm_user_entry():

			username = self.screen.get_username()
			password = self.screen.get_password()
			website = self.screen.get_website()

			self.data_manager.add_password(
				website,
				username,
				password
				)
			self.screen.clear_entries()

	def generate_random_password_function(self) -> None:
		password = self.password_generator.generate()
		self.screen.set_password(
			password=password
			)

def main() -> None:
	pass_man = PasswordManager()
	pass_man.run()

if __name__ == "__main__":
	main()