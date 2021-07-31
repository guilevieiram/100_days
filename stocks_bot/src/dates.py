import datetime

class Date:

	@staticmethod
	def _date(delta: int) -> str:
		now = datetime.datetime.now()
		date = now.date() - datetime.timedelta(days=delta)
		return str(date)

	def get(self, day: str = "today") -> str:

		if day.lower() == "today":
			return self._date(delta=1)

		elif day.lower() == "yesterday":
			return self._date(delta=2)