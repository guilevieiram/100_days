import datetime as dt
import smtplib 
import random as r
import time
import os


class QuotesGenerator:
	def get_quote(self, quotes_path: str) -> str:
		print("generating quote...")
		with open(quotes_path, 'r') as file:
			quotes = file.readlines()
		print("quote generated!")
		return r.choice(quotes)

class EmailManager:
	def __init__(self, 
				user: str = os.environ.get("EMAIL_USER"),
				password: str = os.environ.get("EMAIL_PASSWORD_PYTHON"),
				server: str = "smtp.gmail.com",
				port: int = 587) -> None:

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

class MotivationalBot:

	def run(self) -> None:
		self.send_quote()
		time.sleep(60*60*24*7)

	def send_quote(self) -> None:
		try:
			mail_man = EmailManager()
			mail_man.login()
		except Exception as e:
			print(e)
		else:
			if dt.datetime.now().weekday() == 0:
				mail_man.send_email(
					to_adress="guilhermevmanhaes@gmail.com",
					message=QuotesGenerator().get_quote(quotes_path="./quotes.txt"),
					subject="Have a good week!"
					)
		finally:
			mail_man.logout()


def main() -> None:
	MotivationalBot().run()

if __name__ == "__main__":
	main()