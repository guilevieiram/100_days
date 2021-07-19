from model import Model, MyModel
from view import View, TkView

class Controller:
	def __init__(self, view: View, model: Model) -> None:

		self.view: View = view
		self.model: Model = model

		self.view.add_functions(
			yes_button_function=self.yes_button_function,
			no_button_function=self.no_button_function
			)

		self.view.build()

	def run(self) -> None:
		self.view.start()

	def yes_button_function(self) -> None:
		self.model.remove_data(self.model.get_current_data())
		self.model.generate_data()
		self.view.show(
			wait_time=3,
			data=self.model.get_current_data()
			)

	def no_button_function(self) -> None:
		self.model.generate_data()
		self.view.show(
			wait_time=3,
			data=self.model.get_current_data()
			)

def main() -> None:

	# controller-model-view architecture on a bridge pattern
	controller = Controller(
		view = TkView(),
		model = MyModel()
		)

	controller.run()

if __name__=="__main__":
	main()