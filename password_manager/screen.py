from abc import ABC, abstractmethod
from tkinter import *
from tkinter import messagebox
from constants import *


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


class TkPopUpManager:
	def ask_user(self, title: str, message: str) -> bool:
		return messagebox.askokcancel(
			title=title,
			message=message
			)
	def warn_user(self, title: str, message: str) -> None:
		return messagebox.showwarning(
			title=title,
			message=message
			)
	def show_user(self, title: str, message: str) -> None:
		return messagebox.showinfo(
			title=title,
			message=message
			)
class TkScreen(Screen):

	def __init__(self, **functions) -> None:
		self.__dict__.update(functions)

		self.pop_up_man = TkPopUpManager()

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
		self.retrieve_password = widget_manager.make_button(
			text=RETPASS_TEXT,
			row=RETPASS_ROW,
			column=RETPASS_COLUMN,
			columnspan=RETPASS_COLSPAN,
			width=RETPASS_WIDTH,
			func=self.retrieve_password_function
			)

		# Focusing
		self.website_entry.focus()

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
		self.password_entry.delete(0,END)

	def show_password(self, website: str, credentials: dict):
		title = "Here is the desired password"
		message = f"Website: {website}\n\tUsername: {credentials['username']}\n\tPassword: {credentials['password']}"
		self.pop_up_man.show_user(
			title=title,
			message=message
			)

	def field_empty(self) -> bool:
		fields = []
		if not self.get_username():
			fields.append('username')
		if not self.get_password():
			fields.append('password')
		if not self.get_website():
			fields.append('website')

		if fields:
			title = "Empty field not allowed"
			message = f"Entries {','.join(fields)} cannot be empty.\nPlease fill them."

			self.pop_up_man.warn_user(
			title=title,
			message=message
			)

		return bool(fields)

	def confirm_user_entry(self) -> bool:
		title = "Save details"
		message = f'''This are the details entered: 
	Website: {self.get_website()}
	Usename: {self.get_username()}
	Password: {self.get_password()}\n\nDo you want to save?
		'''		
		return self.pop_up_man.ask_user(
			title=title,
			message=message
			)

	def make(self) -> None:
		self.window.mainloop()