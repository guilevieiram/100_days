from tkinter import *
from datetime import timedelta

"""CONSTANTS"""

# COLORS
PINK = '#e2979c'
RED = '#e7305b'
GREEN = '#9bdeac'
YELLOW = '#f7f5dd' 
BLACK = '#000000'

# Window
TITLE = 'Pomodoro'
PADX = 50
PADY = 50
COLOR = YELLOW
FONT = "Arial"

# Canvas
CANVAS_WIDTH = 250
CANVAS_HEIGHT = 250
CANVAS_ROW = 1
CANVAS_COLUMN = 1
CANVAS_COLOR = COLOR

# Image
IMAGE_PATH = 'tomato.png'
IMAGE_POSITION_X = CANVAS_WIDTH // 2
IMAGE_POSITION_Y = CANVAS_HEIGHT // 2

# Button
START_BUTTON_TEXT = 'Start'
START_BUTTON_ROW = 2
START_BUTTON_COLUMN = 0
START_BUTTON_COLOR = PINK

RESET_BUTTON_TEXT = 'Reset'
RESET_BUTTON_ROW = 2
RESET_BUTTON_COLUMN = 2
RESET_BUTTON_COLOR = PINK

# Main Text
INITIAL_TEXT = 'Pomodoro'
STUDY_TEXT = 'Study!'
BREAK_TEXT = 'Break time!'

MAIN_TEXT_SIZE =  30
MAIN_TEXT_ROW = 0
MAIN_TEXT_COLUMN = 1
MAIN_TEXT_BG_COLOR = COLOR
MAIN_TEXT_FG_COLOR = GREEN

# Tick Count
TICK_TEXT = "✔️"
TICK_SIZE = 10
TICK_TEXT_ROW = 3
TICK_TEXT_COLUMN = 1
TICK_TEXT_BG_COLOR = COLOR
TICK_TEXT_FG_COLOR = BLACK

# Timer
TIMER_POSITION_X = CANVAS_WIDTH // 2
TIMER_POSITION_Y = 150
TIMER_SIZE = 20

## MISCELANIOUS FUNCTIONS
def seconds_to_time(seconds: int) -> str:
	return str(timedelta(seconds=seconds))[2:]

class Screen():
	def __init__(self):
		#setting up all the passed functions to the backend

		self.window: Tk = self.make_window(
			title=TITLE,
			padx=PADX,
			pady=PADY,
			color=COLOR
		)

		self.image: PhotoImage

		self.canvas: Canvas = self.make_canvas(
			width=CANVAS_WIDTH,
			height=CANVAS_HEIGHT,
			row=CANVAS_ROW,
			column=CANVAS_COLUMN,
			color=CANVAS_COLOR
		) 

		self.image: PhotoImage = self.make_image(
			position_x=IMAGE_POSITION_X,
			position_y=IMAGE_POSITION_Y,
			image_path=IMAGE_PATH
		)

		self.timer: Label = self.make_timer(
			position_x=TIMER_POSITION_X,
			position_y=TIMER_POSITION_Y,
			time=0
		)

		self.start_button: Button = self.make_button(
			text=START_BUTTON_TEXT, 
			func=self.start_button_function,
			row=START_BUTTON_ROW,
			column=START_BUTTON_COLUMN,
			color=START_BUTTON_COLOR
		)
		
		self.reset_button: Button = self.make_button(
			text=RESET_BUTTON_TEXT, 
			func=self.reset_button_function,
			row=RESET_BUTTON_ROW,
			column=RESET_BUTTON_COLUMN,
			color=RESET_BUTTON_COLOR
		)

		self.main_text: Label = self.make_text(
			text=INITIAL_TEXT,
			size=MAIN_TEXT_SIZE,
			row=MAIN_TEXT_ROW,
			column=MAIN_TEXT_COLUMN,
			bg_color=MAIN_TEXT_BG_COLOR,
			fg_color=MAIN_TEXT_FG_COLOR
		)

		self.tick_text: Label = self.make_text(
			text='',
			size=TICK_SIZE,
			row=TICK_TEXT_ROW,
			column=TICK_TEXT_COLUMN,
			bg_color=TICK_TEXT_BG_COLOR,
			fg_color=TICK_TEXT_FG_COLOR
		)

	def make(self):
		self.window.mainloop()
	
	def make_window(self, title: str, padx: int, pady: int, color: str) -> Tk:
		window: Tk = Tk()
		window.title(title)
		window.config(padx=padx, pady=pady, bg=color, highlightthickness=0)
		return window

	def make_button(self, text: str, func, row: int, column: int, color: str) -> Button:
		button = Button(
			text=text,
			command=func,
			bg=color
			)
		button.grid(row=row, column=column)		
		return button

	def make_text(self, text: str, size: int, row: int, column: int, bg_color: str, fg_color: str) -> Label:
		text = Label(
			text=text,
			font=(FONT, size),
			highlightthickness=0,
			bg=bg_color,
			fg=fg_color
			)
		text.grid(row=row, column=column)		
		return text

	def make_canvas(self, row: int, column: int, width: int, height: int, color: str) -> Canvas:
		canvas = Canvas(width=width, height=height, bg=color, highlightthickness=0)
		canvas.grid(row=row, column=column)
		return canvas

	def make_image(self, position_x: int, position_y: int, image_path: str) -> None:
		image = PhotoImage(file=image_path)
		self.canvas.create_image(
			position_x,
			position_y,
			image=image
		)
		return image
	
	def make_timer(self, position_x: int, position_y: int, time: float) -> None:
		time_str = seconds_to_time(seconds=time)
		timer = self.canvas.create_text(
			position_x,
			position_y,
			text=time_str,
			font=(FONT, TIMER_SIZE)
		)
		return timer

	def increase_tick(self) -> None:
		self.tick_text["text"] += TICK_TEXT

	def update_timer(self, time: int):
		self.canvas.itemconfig(
			self.timer,
			text=seconds_to_time(time)
			)

	def count_down(self, start_time: int) -> None:
		self.update_timer(time=start_time)
		if start_time > 0: 
			self.window.after(
				1000,
				self.count_down,
				start_time - 1
			)
		else: 
			self.increase_tick()