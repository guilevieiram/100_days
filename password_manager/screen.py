from abc import ABC, abstractmethod
from tkinter import *


"""CONSTANTS"""
# Text
FONT = "Arial"
SIZE = 12
COLOR = "black"

# Website text
WEB_TEXT = "Website: "
WEB_ROW = 2
WEB_COLUMN = 0 

# Email text
EMAIL_TEXT = "Email/Username: "
EMAIL_ROW = 3
EMAIL_COLUMN = 0

# Password text
PASS_TEXT = "Password: "
PASS_ROW = 4
PASS_COLUMN = 0

# Website entry
WEB_ENTRY_COLSPAN = 2
WEB_ENTRY_ROW = WEB_ROW
WEB_ENTRY_COLUMN = 1
WEB_ENTRY_WIDTH = 60

# Email entry
EMAIL_ENTRY_COLSPAN = 2
EMAIL_ENTRY_ROW = EMAIL_ROW
EMAIL_ENTRY_COLUMN = 1
EMAIL_ENTRY_WIDTH = WEB_ENTRY_WIDTH

# Password entry
PASS_ENTRY_COLSPAN = 1
PASS_ENTRY_ROW = PASS_ROW
PASS_ENTRY_COLUMN = 1
PASS_ENTRY_WIDTH = 25

# Add password button
ADDPASS_TEXT = "Add"
ADDPASS_ROW = 5
ADDPASS_COLUMN = 1
ADDPASS_COLSPAN = 2
ADDPASS_WIDTH = WEB_ENTRY_WIDTH

# Generate random password button
RANDPASS_TEXT = "Generate password"
RANDPASS_ROW = PASS_ROW
RANDPASS_COLUMN = 2
RANDPASS_COLSPAN = 1
RANDPASS_WIDTH = PASS_ENTRY_WIDTH

# Window
TITLE = "Password Manager"
PADX = 50
PADY = 30

# App Title
TITLE_FONT = FONT
TITLE_SIZE = 20
TITLE_ROW = 0
TITLE_COLUM = 0
TITLE_COLOR = "red"
TITLE_COLSPAN = 3


# Canvas
CANVAS_ROW = 1
CANVAS_COLUMN = 0
CANVAS_WIDTH = 100
CANVAS_HEIGHT = 100
CANVAS_COLSPAN = 3

# Image
IMAGE_PATH = "./cat.png"
IMAGE_X = CANVAS_WIDTH//2
IMAGE_Y = CANVAS_HEIGHT//2


class TkWidgetManager:
	def make_window(self, title: str, padx: int, pady: int) -> Tk:
		window: Tk = Tk()
		window.title(title)
		window.config(padx=padx, pady=pady, highlightthickness=0)
		return window

	def make_button(self, text: str, func, row: int, column: int, width: int, columnspan: int = 1, sticky: str = "E") -> Button:
		button = Button(
			text=text,
			command=func,
			width=width
			)
		button.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)		
		return button
	
	def make_entry(self, row: int, column: int, width: int, columnspan: int = 1, sticky: str = "W") -> Entry:
		entry = Entry(
			width=width
			)
		entry.grid(row=row, column=column,columnspan=columnspan, sticky=sticky)
		return entry

	def make_text(self, text: str, font: int, size: int, row: int, column: int, fg_color: str, columnspan: int =1) -> Label:
		text = Label(
			text=text,
			font=(font, size),
			highlightthickness=0,
			fg=fg_color
			)
		text.grid(row=row, column=column, columnspan=columnspan)		
		return text

	def make_canvas(self, row: int, column: int, width: int, height: int, columnspan: int =1) -> Canvas:
		canvas = Canvas(width=width, height=height, highlightthickness=0)
		canvas.grid(row=row, column=column, columnspan=columnspan)
		return canvas

	def make_image(self, position_x: int, position_y: int, image_path: str, canvas: Canvas) -> None:
		image = PhotoImage(file=image_path)
		canvas.create_image(
			position_x,
			position_y,
			image=image
		)
		return image

class Screen(ABC):
	@abstractmethod
	def get_username(self) -> str:
		pass
	@abstractmethod
	def get_password(self) -> str:
		pass
	@abstractmethod
	def get_website(self) -> str:
		pass
	@abstractmethod
	def set_password(self, password: str) -> None:
		pass
	@abstractmethod
	def clear_entries(self) -> None:
		pass
	@abstractmethod
	def make(self) -> None:
		pass

class TkScreen(Screen):

	def __init__(self, **functions) -> None:
		self.__dict__.update(functions)

		widget_manager = TkWidgetManager()

		# Making window
		self.window = widget_manager.make_window(
			title=TITLE,
			padx=PADX,
			pady=PADY
			)

		# Making visuals
		self.title = widget_manager.make_text(
			text=TITLE,
			font=TITLE_FONT,
			size=TITLE_SIZE,
			row=TITLE_ROW,
			column=TITLE_COLUM,
			fg_color=TITLE_COLOR,
			columnspan=TITLE_COLSPAN
			)
		self.canvas = widget_manager.make_canvas(
			row=CANVAS_ROW,
			column=CANVAS_COLUMN,
			width=CANVAS_WIDTH,
			height=CANVAS_HEIGHT,
			columnspan=CANVAS_COLSPAN
			)
		self.image = widget_manager.make_image(
			position_x=IMAGE_X,
			position_y=IMAGE_Y,
			image_path=IMAGE_PATH,
			canvas=self.canvas
			)

		# Making texts
		self.website_text = widget_manager.make_text(
			text=WEB_TEXT,
			font=FONT,
			size=SIZE,
			row=WEB_ROW,
			column=WEB_COLUMN,
			fg_color=COLOR
			)
		self.email_text = widget_manager.make_text(
			text=EMAIL_TEXT,
			font=FONT,
			size=SIZE,
			row=EMAIL_ROW,
			column=EMAIL_COLUMN,
			fg_color=COLOR
			)
		self.password_text = widget_manager.make_text(
			text=PASS_TEXT,
			font=FONT,
			size=SIZE,
			row=PASS_ROW,
			column=PASS_COLUMN,
			fg_color=COLOR
			)

		# Making entries
		self.website_entry = widget_manager.make_entry(
			columnspan=WEB_ENTRY_COLSPAN,
			row=WEB_ENTRY_ROW,
			column=WEB_ENTRY_COLUMN,
			width=WEB_ENTRY_WIDTH
			)
		self.email_entry = widget_manager.make_entry(
			columnspan=EMAIL_ENTRY_COLSPAN,
			row=EMAIL_ENTRY_ROW,
			column=EMAIL_ENTRY_COLUMN,
			width=EMAIL_ENTRY_WIDTH
			)
		self.password_entry = widget_manager.make_entry(
			columnspan=PASS_ENTRY_COLSPAN,
			row=PASS_ENTRY_ROW,
			column=PASS_ENTRY_COLUMN,
			width=PASS_ENTRY_WIDTH
			)

		# Making buttons
		self.add_password = widget_manager.make_button(
			text=ADDPASS_TEXT,
			row=ADDPASS_ROW,
			column=ADDPASS_COLUMN,
			columnspan=ADDPASS_COLSPAN,
			width=ADDPASS_WIDTH,
			func=self.add_password_button_function
			)
		self.generate_password = widget_manager.make_button(
			text=RANDPASS_TEXT,
			row=RANDPASS_ROW,
			column=RANDPASS_COLUMN,
			columnspan=RANDPASS_COLSPAN,
			width=RANDPASS_WIDTH,
			func=self.generate_random_password_function
			)

	def get_username(self) -> str:
		return self.email_entry.get()

	def get_password(self) -> str:
		return self.password_entry.get()

	def get_website(self) -> str:
		return self.website_entry.get()

	def set_password(self, password: str) -> None:
		self.password_entry.delete(0,END)
		self.password_entry.insert(0, password)

	def clear_entries(self) -> None:
		self.website_entry.delete(0,END)
		self.email_entry.delete(0,END)
		self.password_entry.delete(0,END)

	def make(self) -> None:
		self.window.mainloop()