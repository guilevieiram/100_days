from abc import ABC, abstractmethod
import os
import time
from tkinter import *

class View(ABC):

	@abstractmethod
	def __init__(self, input_action) -> None:
		pass

	@abstractmethod
	def show_question(self, question: str, number: int) -> None:
		pass

	@abstractmethod
	def update_score(self, score: int) -> None:
		pass

	@abstractmethod
	def end_screen(self, score: int) -> None:
		pass

	@abstractmethod
	def show_screen(self) -> None:
		pass

	@abstractmethod
	def right_answer(self) -> None:
		pass

	@abstractmethod
	def wrong_answer(self) -> None:
		pass

class TerminalView(View):

	def __init__(self, input_action) -> None:
		self.input_action = input_action

	def show_question(self, question: str, number: int) -> None:
		print(f"Q{number}:\t{question}")
		self.get_answer()

	def update_score(self, score: int, max_score: int) -> None:
		self.clear_screen()
		print("Quizzer!!")
		print(f"Score: {score}/{max_score}")		
		print("==============================================================")

	def end_screen(self, score: int, max_score: int) -> None:
		self.clear_screen()
		print("\n\nGAME OVER")
		print("You answered all the questions")
		print(f"Your final score is {score}/{max_score}")

	def show_screen(self) -> None:
		print("Welcome to Quizzer!!\n")
		print("==============================================================")

	def right_answer(self) -> None:
		print("Quizzer!!")
		print("\nThat's Correct!")
		time.sleep(1)
		
	def wrong_answer(self) -> None:
		print("Quizzer!!")
		print("\nNot quite ...")
		time.sleep(1)

	# Additional methods
	def clear_screen(self) -> None:
		os.system('cls' if os.name == 'nt' else 'clear')

	def get_answer(self) -> str:
		answer = input("A :\t(True / False)? ")
		self.clear_screen()
		self.input_action(answer=string_to_bool(answer))


class TkView(View):

	def __init__(self, input_action) -> None:

		self.theme_color: str = "#375362"

		# Window
		self.window: Tk = Tk()
		self.window.title("Quizzer")
		self.window.config(bg=self.theme_color, padx=30, pady=30)

		# Buttons
		self.true_image = PhotoImage(file="./images/true.png")
		self.true_button = Button(image=self.true_image, highlightthickness=0,
									command=lambda x=True : input_action(x))
		self.true_button.grid(row=2, column=0)

		self.false_image = PhotoImage(file="./images/false.png")
		self.false_button = Button(image=self.false_image, highlightthickness=0,
									command=lambda x=False : input_action(x))
		self.false_button.grid(row=2, column=1)

		# Canvas
		self.canvas = Canvas(width=400, height=400, highlightthickness=0, bg="white")
		self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

		# Question text
		self.question = self.canvas.create_text(200, 200, text = "Quizzer",
						font=("consola", 16, "italic"), width=380, justify="center")

		# Score text
		self.score = Label(text="Score: 0", font=("consola", 14), bg=self.theme_color)
		self.score.grid(row=0, column=1)

	def show_question(self, question: str, number: int) -> None:
		def show() -> None:
			self.change_canvas_color(color="white")
			self.canvas.itemconfig(
				self.question, text=f"Q{number}: {question}"
				)	
		self.window.after(1000, show)

	def update_score(self, score: int, max_score: int) -> None:
		self.score["text"] = f"Score: {score}"

	def end_screen(self, score: int, max_score: int) -> None:
		def end() -> None:
			self.change_canvas_color(color="white")
			self.canvas.itemconfig(
				self.question, 
				text=f"GAME OVER\n\nFinal Score: {score}/{max_score}",
				font=("consola", 24, "bold")
				)
			self.score["text"] = ""
			self.true_button["command"] = self.quit
			self.false_button["command"] = self.quit

		self.window.after(1000, end)


	def show_screen(self) -> None:
		self.window.mainloop()

	def right_answer(self) -> None:
		self.change_canvas_color(color="green")

	def wrong_answer(self) -> None:
		self.change_canvas_color(color="red")

	# Additional methods
	def quit(self) -> None:
		self.window.destroy()

	def change_canvas_color(self, color: str) -> None:
		self.canvas["bg"] = color


# Miscelanious functions
def string_to_bool(string: str) -> bool:
    """Converts similar string inputs to boolean output. Lacks better implementation"""
    if string.lower() in ["true", "t", "yes", "y"]:
        return True
    else:
        return False