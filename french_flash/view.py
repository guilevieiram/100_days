from abc import ABC, abstractmethod
from tkinter import *
import time

"""CONSTANTS"""
# Window
TITLE = 			"French flash"
PADX = 				20
PADY = 				20
COLOR = 			'#b1ddc6'

# Buttons
YES_PATH = 			'./images/right.png'
YES_ROW = 			1
YES_COLUMN = 		1
YES_COLUMNSPAN = 	1
YES_PADX = 			0
YES_PADY = 			20

NO_PATH = 			'./images/wrong.png'
NO_ROW = 			1
NO_COLUMN = 		0
NO_COLUMNSPAN = 	1
NO_PADX = 			0
NO_PADY = 			20

# Canvas
CANVAS_ROW = 		0
CANVAS_COLUMN = 	0
CANVAS_WIDTH = 		800
CANVAS_HEIGHT = 	525
CANVAS_COLSPAN = 	2
CANVAS_COLOR = 		COLOR

# Images
FRONT_IMAGE_POS_X =	CANVAS_WIDTH//2
FRONT_IMAGE_POS_Y =	CANVAS_HEIGHT//2
FRONT_IMAGE_PATH =	'./images/card_front.png'

BACK_IMAGE_POS_X =	CANVAS_WIDTH//2
BACK_IMAGE_POS_Y =	CANVAS_HEIGHT//2
BACK_IMAGE_PATH =	'./images/card_back.png'

# Text
TITLE_TEXT =		'French'
TITLE_FONT =		'arial'
TITLE_SIZE =		'40'
TITLE_TYPE = 		'italic'
TITLE_POSX =		CANVAS_WIDTH//2
TITLE_POSY = 		150

WORD_TEXT =			'WORD'
WORD_FONT =			'arial'
WORD_SIZE =			'60'
WORD_TYPE = 		'bold'
WORD_POSX =			CANVAS_WIDTH//2
WORD_POSY = 		263

FRONT_WORD_COLOR = 	'black'
BACK_WORD_COLOR = 	'white'

class TkWidgetManager:
	def make_window(self, title: str, padx: int, pady: int, color: str) -> Tk:
		window: Tk = Tk()
		window.title(title)
		window.config(padx=padx, pady=pady, bg=color, highlightthickness=0)
		return window

	def make_button(self, text: str, row: int, column: int, func, columnspan: int = 1) -> Button:
		button = Button(
			text=text,
			command=func,
			)
		button.grid(row=row, column=column, columnspan=columnspan)		
		return button

	def make_image_button(self, image_path: str, row: int, column: int, func, padx: int = 0, pady:int = 0, columnspan: int = 1) -> Button:
		image = PhotoImage(file=image_path)
		button = Button(
			text='here',
			image=image,
			command=func,
			highlightthickness=0
			)
		button.image = image
		button.grid(row=row, column=column, padx=padx, pady=pady, columnspan=columnspan)		
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

	def make_canvas_text(self, canvas: Canvas, text: str, font: int, size: int, font_type: str, position_x: int, position_y: int) -> Label:
		return canvas.create_text(
			position_x,
			position_y,
			text=text,
			font=(font, size, font_type)
			)
	
	def make_canvas(self, row: int, column: int, width: int, height: int, color: str, columnspan: int =1) -> Canvas:
		canvas = Canvas(width=width, height=height, highlightthickness=0, bg=color)
		canvas.grid(row=row, column=column, columnspan=columnspan)
		return canvas

	def make_image(self, image_path: str) -> PhotoImage:

		return PhotoImage(file=image_path)

	def place_image(self, position_x: int, position_y: int, canvas: Canvas, image: PhotoImage) -> int:
		return canvas.create_image(
			position_x,
			position_y,
			image=image
		)

class View(ABC):
	@abstractmethod
	def build(self) -> None:
		pass

	@abstractmethod
	def add_functions(self, **functions) -> None:
		pass

	@abstractmethod
	def start(self) -> None:
		pass

	@abstractmethod
	def show(self, data: dict) -> None:
		pass

	@abstractmethod
	def get_word(self) -> str:
		pass

class TkView(View):

	def build(self) -> None:
		# Making window
		self.window = TkWidgetManager().make_window(
			title=	TITLE,
			padx=	PADX,
			pady=	PADY,
			color=	COLOR
			)

		# Making canvas
		self.card_canvas = TkWidgetManager().make_canvas(
			row=		CANVAS_ROW,
			column=		CANVAS_COLUMN,
			width=		CANVAS_WIDTH,
			height=		CANVAS_HEIGHT,
			columnspan=	CANVAS_COLSPAN,
			color= 		CANVAS_COLOR
			)

		# Making buttons
		self.yes_button = TkWidgetManager().make_image_button(
			image_path=	YES_PATH,
			row=		YES_ROW,
			column=		YES_COLUMN,	
			columnspan=	YES_COLUMNSPAN,
			padx= 		YES_PADX,
			pady= 		YES_PADY,
			func=		self.yes_button_function,
			)
		self.no_button = TkWidgetManager().make_image_button(
			image_path=	NO_PATH,
			row=		NO_ROW,
			column=		NO_COLUMN,	
			columnspan=	NO_COLUMNSPAN,
			padx= 		NO_PADX,
			pady= 		NO_PADY,
			func=		self.no_button_function
			)

		# Making image
		self.front_card = PhotoImage(file=FRONT_IMAGE_PATH)
		self.card_canvas.card = TkWidgetManager().place_image(
			position_x=	FRONT_IMAGE_POS_X,
			position_y=	FRONT_IMAGE_POS_Y,
			image = 	self.front_card,
			canvas =	self.card_canvas
			)

		# Making text
		self.card_canvas.title = TkWidgetManager().make_canvas_text(
			self.card_canvas,
			text=		TITLE_TEXT,
			font=		TITLE_FONT,
			size=		TITLE_SIZE,
			font_type= 	TITLE_TYPE,
			position_x=	TITLE_POSX,
			position_y=	TITLE_POSY,
			)
		self.card_canvas.word = TkWidgetManager().make_canvas_text(
			self.card_canvas,
			text=		WORD_TEXT,
			font=		WORD_FONT,
			size=		WORD_SIZE,
			font_type= 	WORD_TYPE,
			position_x=	WORD_POSX,
			position_y=	WORD_POSY,
			)

	def add_functions(self, **functions) -> None:
		self.__dict__.update(functions)

	def start(self) -> None:
		self.window.mainloop()

	def get_word(self) -> str:
		return self.card_canvas.itemcget(self.card_canvas.word, 'text')

	def show(self, wait_time: int, data: dict) -> None:
		self.update_card(title="French", word=data["French"], card="front")
		self.count_down(
			wait_time=wait_time,
			func=lambda : self.update_card(title="English", word=data["English"], card="back")
			)

	def count_down(self, wait_time: int, func) -> None:
		if wait_time > 0:
			self.window.after(
				1000,
				self.count_down,
				wait_time - 1,
				func
				)
		else:
			func()

	def update_card(self, title: str, word: str, card: str) -> None:
		if card == "front":
			self.front_card = PhotoImage(file=FRONT_IMAGE_PATH)
			self.card_canvas.itemconfig(self.card_canvas.card, image = self.front_card)
			self.card_canvas.itemconfig(self.card_canvas.title, text=title, fill=FRONT_WORD_COLOR)
			self.card_canvas.itemconfig(self.card_canvas.word, text=word, fill=FRONT_WORD_COLOR)
		if card == "back":
			self.back_card = PhotoImage(file=BACK_IMAGE_PATH)
			self.card_canvas.itemconfig(self.card_canvas.card, image = self.back_card)
			self.card_canvas.itemconfig(self.card_canvas.title, text=title, fill=BACK_WORD_COLOR)
			self.card_canvas.itemconfig(self.card_canvas.word, text=word, fill=BACK_WORD_COLOR)
