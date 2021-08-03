from src.decorators import log
from abc import ABC, abstractmethod
import os
import smtplib

from typing import Optional

class Messager(ABC):

	@abstractmethod
	def send_message(self, destination: str, message: str, subject: str) -> None:
		pass


class TerminalMessager(Messager):

	@log("messager_log")
	def send_message(self, destination: str, message: str, subject: str) -> None:
		content = "\n-------------------------------------------------------------------"
		content += f"\nMessage to {destination}\nSubject: {subject}\n\n{message}"
		content += "\n-------------------------------------------------------------------\n"
		print(content)
		return content


class EmailMessager(Messager):

	def __init__(self, 
				user: str = os.environ.get("EMAIL_USER"),
				password: str = os.environ.get("EMAIL_PASSWORD_PYTHON"),
				server: str = "smtp.gmail.com",
				port: int = 587) -> None:

		self.user: str = user
		self.password: str = password
		self.server: str = server
		self.port: int = port

	@log("mail_log")
	def connect_to_server(self) -> Optional[str]:
		self.connection = smtplib.SMTP(self.server, self.port)
		self.connection.starttls() 

	@log("mail_log")
	def login(self) -> None:
		self.connection.login(user=self.user, password=self.password)

	@log("mail_log")
	def logout(self) -> None:
		self.connection.close()

	@log("mail_log")
	def send_message(self, destination: str, message: str, subject: str) -> Optional[str]:
		self.connect_to_server()
		self.login()
		self.connection.sendmail(
			from_addr=self.user,
			to_addrs=destination,
			msg=f"Subject:{subject}\n\n{message}"
			)
		self.logout()
