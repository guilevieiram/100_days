from abc import ABC, abstractmethod
import os
from twilio.rest import Client

from src.decorators import log

# Abstract class
class Messager(ABC):

	@abstractmethod
	def send_message(self, telephone: str, message: str) -> None:
		pass

# Concrete classes
class TerminalMessager(Messager):
	
	def send_message(self, telephone: str, message: str) -> None:
		print(f"message to {telephone}\n{message}")
        

class FileMessager(Messager):
	
	def send_message(self, telephone: str, message: str) -> None:
		with open("message.txt", "w", encoding="utf-8") as message_file:
			message_file.write(f"message to {telephone}\n{message}")


class TwilioMessager(Messager):

	def __init__(self) -> None:
		self.sid = "ACb62737daa2ca8914b38d013ac3946891"
		self.token = os.environ.get("TWILIO_TOKEN")
		self.number = "+13868663463"
		self.client = Client(self.sid, self.token)

	@log("message")
	def send_message(self, telephone: str, message: str) -> None:
		twilio_message = self.client.messages.create(
			body=message,
			from_=self.number,
			to=telephone
			)

		print(twilio_message.sid)
		return twilio_message.sid