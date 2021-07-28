import requests
import datetime as dt
import smtplib
import os
import time

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


class SunTracer:

	def __init__(self) -> None:
		self.data: dict
		self.get_data()
	
	def get_data(self) -> None:
		response = requests.get(
		url="https://api.sunrise-sunset.org/json",
		params={
			"lat": -19.930100,
			"lng": -43.948250,
			"formatted": 0
			}
		)
		response.raise_for_status()
		self.data = response.json()

	def get_sunrise_hour(self) -> int:
		return self.get_hour_format(self.data["results"]["sunrise"])

	def get_sunset_hour(self) -> int:
		return self.get_hour_format(self.data["results"]["sunset"])

	def get_hour_format(self, time: str) -> int:
		return int(time[11:13])


class NightTracer:
	
	def is_night(self, sunrise_hour: int, sunset_hour: int) -> bool:
		now = dt.datetime.now()
		now_hour = self.get_hour_format(time=now)
		return now_hour > sunset_hour and now_hour < sunrise_hour

	def get_hour_format(self, time: dt.datetime) -> int:
		return time.hour


class IssTracer:

	def position(self) -> tuple:
		iss_data = self.request()
		return self.get_position(iss_data)

	def request(self) -> dict:
		iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
		iss_response.raise_for_status()
		return iss_response.json()

	def get_position(self, data: dict) -> tuple:
		iss_position = data["iss_position"]
		return float(iss_position["longitude"]), float(iss_position["latitude"])


class IssBot:

	def __init__(self) -> None:
		self.home_position = (-19.930100, -43.948250)

	def run(self) -> None:
		while True:
			if self.is_night() and self.are_close(self.get_iss_position(), self.home_position):
				self.send_email()
			time.sleep(60)

	def is_night(self) -> bool:
		sun_tracer = SunTracer()
		sunrise_hour = sun_tracer.get_sunrise_hour()
		sunset_hour = sun_tracer.get_sunset_hour()
		return NightTracer().is_night(
			sunrise_hour=sunrise_hour,
			sunset_hour=sunset_hour
			)

	def get_iss_position(self) -> tuple:
		return IssTracer().position()

	def are_close(self, position_1: tuple, position_2: tuple) -> bool:
		return (
			abs(position_1[0] - position_2[0]) < 5 and
			abs(position_1[1] - position_2[1]) < 5
			)

	def send_email(self) -> None:
		try:
			mail_man = EmailManager(
				user=os.environ.get("EMAIL_USER"),
				password=os.environ.get("EMAIL_PASSWORD_PYTHON"),
				server="smtp.gmail.com",
				port=587
				)
			mail_man.login()
		except Exception as e:
			print(e)
		else:
			mail_man.send_email(
				to_adress="guilhermevmanhaes@gmail.com",
				message="Look up! The International Space Station is right above your head!",
				subject="ISS above!"
				)
			mail_man.logout()


def main() -> None:
	IssBot().run()


if __name__ == "__main__":
	main()