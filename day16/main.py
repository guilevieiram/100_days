from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine
import os

'''
Goals:
1. Print report.
2. Check resources sufficient?
3. Process coins
4. Check transaction successful?
5. Make Coffee.
'''

class CoffeeMachine():
	def __init__(self) -> None:
		self.menu: Menu = Menu()
		self.money_machine: MoneyMachine = MoneyMachine()
		self.coffee_maker: CoffeeMaker = CoffeeMaker()
		self.money_recieved_total: float = 0

	def print_report(self) -> None:
		'''Prints a full report of the coffee machine'''
		print(f"\nMoney report:")
		self.money_machine.report()
		print(f"\nCoffee Maker report:")
		self.coffee_maker.report()

	def check_sufficient_resources(self, drink_name: str) -> bool:
		'''Check if the machine has suffiecient resources for a given order from the menu'''
		drink: MenuItem = self.menu.find_drink(drink_name)
		return self.coffee_maker.is_resource_sufficient(drink)

	def print_drink_cost(self, drink_name: str) -> None:
		'''Finds the cost of a drink and print it'''
		cost = self.menu.find_drink(drink_name).cost
		print(f"Drink cost: {self.money_machine.CURRENCY}{cost}")

	def check_transaction_successful(self) -> bool:
		'''checks if a transaction was successful'''
		cost: float = self.money_machine.money_received
		return self.money_machine.make_payment(cost)

	def make_coffee(self, drink_name: str) -> None:
		'''Takes an order and makes the coffee'''
		drink: MenuItem = self.menu.find_drink(drink_name) 
		self.coffee_maker.make_coffee(drink)


	def is_drink_name_valid(self, drink_name: str) -> bool:
		'''Checks if a drink name is valid'''
		return isinstance(self.menu.find_drink(drink_name), MenuItem)


def main() -> None:
	coffee: CoffeeMachine = CoffeeMachine()

	'''Machine state'''
	on = True

	'''Main loop'''
	while on:

		'''Clearing screen'''
		os.system("clear")
		print("-----------------------------------------------")

		'''Getting the drink order'''
		print("What would you like to drink today?\nHere are the options!")
		print(coffee.menu.get_items())
		drink_name: str = input("Drink: ")

		if coffee.is_drink_name_valid(drink_name):

			'''Checking resourses'''
			if coffee.check_sufficient_resources(drink_name):

				'''Printing the cost'''
				coffee.print_drink_cost(drink_name)

				if coffee.check_transaction_successful():

					'''Making the coffee!'''
					coffee.make_coffee(drink_name)

				else: print("Transaction unsuccessful")
			else: print("Not suficcient resourses")
		else:
			print(f"{drink_name} is not a valid option ...")


		power: str = input("Turn off machine (y/n)? ")	
		if power.lower() == "y": on = False

	'''Printing report after the end of the day'''
	os.system("clear")	
	print("REPORT:")
	coffee.print_report()


if __name__ == '__main__':
	main()
