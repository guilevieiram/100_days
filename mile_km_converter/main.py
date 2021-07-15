from tkinter import *

"""CONSTANTS"""

# Window
TITLE = "Converter App"
WIDTH = 300
HEIGHT = 100 
PADX = 20
PADY = 20

# Text
FONT = 'Arial'
FONT_SIZE = 14

# Labels
MILES_TEXT = 'Miles'
MILES_POSY = 2
MILES_POSX = 0

KM_TEXT = 'Km'
KM_POSY = 2
KM_POSX = 1

EQUAL_TEXT = 'equals '
EQUAL_POSY = 0
EQUAL_POSX = 1

RESULT_TEXT = ''
RESULT_POSY = 1
RESULT_POSX = 1

# Entry
ENTRY_WIDTH = 20
ENTRY_POSX = 0
ENTRY_POSY = 1

# Button
BUTTON_TEXT = 'Calculate!'
BUTTON_POSX = 2
BUTTON_POSY = 1



class Screen():
	def __init__(self, **functions):
		#setting up all the passed functions to the backend
		self.__dict__.update(functions)

		self.window: Tk
		self.label: Label
		self.button: Button
		self.entry: Entry

		self.setup_widgets()

	def setup_widgets(self) -> None:
		self.setup_window()
		self.setup_labels()
		self.setup_button()
		self.setup_entry()

	def setup_window(self) -> None:
		window: Tk = Tk()
		window.title(TITLE)
		window.minsize(width=WIDTH, height=HEIGHT)
		window.config(padx=PADX, pady=PADY)
		self.window = window

	def setup_labels(self) -> None:
		self.miles = Label(
			text=MILES_TEXT,
			font=(FONT, FONT_SIZE)
			)
		self.miles.grid(row=MILES_POSX, column=MILES_POSY)

		self.km = Label(
			text=KM_TEXT,
			font=(FONT, FONT_SIZE)
			)
		self.km.grid(row=KM_POSX, column=KM_POSY)

		self.equal = Label(
			text=EQUAL_TEXT,
			font=(FONT, FONT_SIZE)
			)
		self.equal.grid(row=EQUAL_POSX, column=EQUAL_POSY)

		self.result = Label(
			text=RESULT_TEXT,
			font=(FONT, FONT_SIZE)
			)
		self.result.grid(row=RESULT_POSX, column=RESULT_POSY)

	def setup_button(self) -> None:
		self.button = Button(
			text=BUTTON_TEXT,
			command=self.button_function
			)
		self.button.grid(row=BUTTON_POSX, column=BUTTON_POSY)

	def setup_entry(self) -> None:
		self.entry = Entry(
			width=ENTRY_WIDTH
			)
		self.entry.grid(row=ENTRY_POSX, column=ENTRY_POSY)

	def update_text(self, text:str, *args) -> None:
		for arg in args:
			self.__dict__[arg]["text"] = text

	def get_input(self) -> str:
		return self.entry.get()

	def make(self):
		self.window.mainloop()

class ConverterApp():

	def __init__(self) -> None:
		self.screen: Screen = Screen(
			button_function=self.main_button_function
			)

	def run(self) -> None:
		self.screen.make()

	def main_button_function(self) -> None:
		def miles_to_km(number: float) -> float:
			return round(1.6 * number, 1)

		numeber_miles = float(self.screen.get_input())
		self.screen.update_text(str(miles_to_km(numeber_miles)), "result")

def main() -> None:
	convapp = ConverterApp()
	convapp.run()

if __name__=="__main__":
	main()