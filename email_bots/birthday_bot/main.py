import pandas as pd
import os
import datetime
import smtplib
import random

# Email
class EmailManager:
	def __init__(self, user: str, password: str, server: str, port: int) -> None:

		self.user = user
		self.password = password

		print("connecting to server...")
		self.connection = smtplib.SMTP(server, port)
		self.connection.starttls() 
		print("connection complete!")

	def login(self) -> None:
		print("login into account...")
		self.connection.login(user=self.user, password=self.password)
		print("account logged successfully!")

	def logout(self) -> None:
		print("login out and disconnecting from server ...")
		self.connection.close()
		print("logout successful!")

	def send_email(self, to_adress: str, message: str, subject: str) -> None:
		print("sending message...")
		self.connection.sendmail(
			from_addr=self.user,
			to_addrs=to_adress,
			msg=f"Subject:{subject}\n\n{message}"
			)
		print("message sent!")

class DummyEmailManager:
	def __init__(self, user: str, password: str, server: str, port: int) -> None:
		self.user = user
		self.password = password
		self.server = server
		self.port = port
		print("connecting to server...")

	def login(self):
		print(f"login in as {self.user} at {self.server}")

	def logout(self):
		print("login out")

	def send_email(self, to_adress: str, message: str, subject: str):
		print(f"\nemail to {to_adress}\n",
			f"Subject: {subject}\n\n{message}")

# Birthday
class BirthdayManager:
	def __init__(self, path: str):
		self.birthdays: pd.DataFrame = pd.read_csv(path)

	def get_birthday_person(self, day: int, month: int) -> list:
		month_filtered_df = self.birthdays[self.birthdays["month"] == month]
		day_month_filtered_df = month_filtered_df[month_filtered_df["day"] == day]
		return list(day_month_filtered_df["name"])

	def get_person_email(self, name: str) -> str:
		try:
			return self.birthdays[self.birthdays["name"] == name]["email"].values[0]
		except IndexError:
			print(ValueError("Name not found in the database"))
			return ""	

# Date
class DateManager:
	def get_today_date(self) -> tuple:
		now = datetime.datetime.now()
		return now.day, now.month

# Letter
class LetterManager:

	def __init__(self, path_to_letters: str) -> None:
		self.letter: str
		self.path = path_to_letters
		self.letters_names = os.listdir(path_to_letters)

	def get_random_letter(self, name: str) -> str:
		letter_name = random.choice(self.letters_names)
		self.letter = self.get_letter(letter_name=letter_name)
		return self.fill_letter(name=name)

	def get_letter(self, letter_name: str) -> str:
		path = os.path.join(self.path, letter_name)
		with open(path, 'r') as letter_file:
			return letter_file.read()

	def fill_letter(self, name: str) -> str:
		return self.letter.replace("[NAME]", name)

# Main bot
class BirthdayBot:
	def __init__(self) -> None:

		self.email_manager = EmailManager(
			user=os.environ.get("EMAIL_USER"),
			password=os.environ.get("EMAIL_PASSWORD_PYTHON"),
			server="smtp.gmail.com",
			port=587
			)

		self.birthday_manager = BirthdayManager(
			path="birthdays.csv"
			)

		self.letter_manager = LetterManager(
			path_to_letters="letter_templates"
			)

		self.date_manager = DateManager()

	def run(self) -> None:
		self.email_manager.login()

		today_day, today_month = self.date_manager.get_today_date()

		birthday_names = self.birthday_manager.get_birthday_person(
			day=today_day,
			month=today_month
			)

		for name in birthday_names:
			email = self.birthday_manager.get_person_email(name=name)
			letter = self.letter_manager.get_random_letter(name=name)
			self.email_manager.send_email(
				to_adress=email,
				subject="Happy birthday!",
				message=letter
				)

		self.email_manager.logout()

def main() -> None:
	BirthdayBot().run()

if __name__ == "__main__":
	main()