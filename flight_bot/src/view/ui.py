from abc import ABC, abstractmethod


class UserInterface(ABC):
	"""User interface class. Responsible for showing and retrieving information from the user"""

	@abstractmethod
	def start(self) -> None:
		"""A starter, to initiate the interface."""
		pass

	@abstractmethod
	def accquire_user(self, information_needed: list) -> dict:
		"""Acquire a new user info, with a list of desired information"""
		pass

class TerminalUserInteface(UserInterface):
	"""Simple terminal user interface"""

	def start(self) -> None:
		print("Welcome to FlightBot!\n\n")

	def accquire_user(self, information_needed: list) -> dict:
		print("Please fill the necessary info")
		information: dict = {}
		for item in information_needed:
			# Could use formatting
			information[item] = input(f"{self.to_title_case(item)}: ")
		return information

	@staticmethod
	def to_title_case(string_snake_case: str) -> str:
		"""
		Auxiliary method for formating strings passed to the ui.
		'turn_this_into_that' -> 'Turn This Into That'
		"""
		splited: list[str] = string_snake_case.split("_")
		splited = [word.title() for word in splited]
		return " ".join(splited)

	@staticmethod
	def to_regular_case(string_snake_case: str) -> str:
		"""
		Auxiliary method for formating strings passed to the ui.
		'turn_this_into_that' -> 'turn this into that'
		"""	
		splited: list[str] = string_snake_case.split("_")
		return " ".join(splited)