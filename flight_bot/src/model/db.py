import requests
import pandas as pd

from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Union, Optional, Any

from src.decorators import log

# Abstract Classes
class DataBase(ABC):
	"""Abstract class for a database with a single table and simple queries."""

	@abstractmethod
	def __init__(self, table: str) -> None:
		"""Initializes the table with the given table name."""
		pass

	@abstractmethod
	def add_data(self, data: list[dict]) -> None:
		"""
		Adds several rows of data in the table
		The data is given in the form of a list of dictionaies.
		Each dictionary shoul have all the columns as keys with the desired values as values.
		"""
		pass

	@abstractmethod
	def get_data(self, key_value: Optional[dict[str, Any]] = None) -> list[dict]:
		"""
		Retrieves a list of data points as a list of dictionaries.
		Each dictionary has the table column names as keys.
		key_value is an optional value containing one attribute for the wanted data (as a filter).
		If no key_value is passed, all the data is retrieved.
		"""
		pass

	@abstractmethod
	def delete_data(self, key: int) -> None:
		"""Deletes a row of data given a key/id for that instance."""
		pass

	@abstractmethod
	def update_data(self, key: int, key_values: list[dict[str, Any]]) -> None:
		"""
		Updates a row of data given a key/id and a key_values:
			a list o key_value pairs containing the desired attributes to be changed
		"""
		pass

# Data base implementations		
class CSVDB(DataBase):
	"""
	Implementation of the data base using csv tables and the Pandas module.
	It features some necessary aditional methods as "update_table" that writes to the csv.
	More information on the parent class.
	"""

	def __init__(self, table: str) -> None:
		self.path: str = f"data/{table}.csv"
		self.data: pd.DataFrame = pd.read_csv(self.path)
		self.data.columns = self.data.columns.map(lambda x: x.lower())
		self.columns: list[str] = list(self.data.columns)

	def add_data(self, data: list[dict]) -> None:
		to_add_df: pd.DataFrame = pd.DataFrame(data)
		self.data = self.data.append(to_add_df, ignore_index=True)
		self.update_table()

	def get_data(self, key_value: Optional[dict[str, Any]] = None) -> list[dict]:
		self.data["id"] = self.data.index
		if not key_value:
			response = self.data.to_dict("records")
		else:
			key, value = list(key_value.items())[0]
			response = self.data[self.data[key]==value].to_dict("records")
		self.data = self.data.drop(columns=["id"])
		self.update_table()
		return response

	def delete_data(self, key: int) -> None:
		self.data = self.data.drop(key, axis=0)
		self.update_table()

	def update_data(self, key_values: list[dict[str, Any]], key: int) -> None:
		for key_value in key_values:
			column, value = list(key_value.items())[0]
			self.data.at[key, column] = value 
		self.update_table()

	def update_table(self) -> None:
		self.data.to_csv(self.path, index=False)

# Needs updating
class Sheety(DataBase):
	"""
	Data base implementation using the Sheety API.
	This API accesses a given Google Sheets document to use as tables.
	For being an API data base, several request methods were included for this API http operations.

	It is outdated since I used all of my free requests this month.
	"""

	def __init__(self, project: str, table: str) -> None:
		self.endpoint: str = f"https://api.sheety.co/3e41b69e3d7c105059981d0ca0c8a47e/{project}/{table}"
		self.table: str = table
		self.project: str = project

	def add_data(self, data: list[dict]) -> None:
		for item in data:
			self.post_request(item=item)

	def get_data(self, key_value: Optional[dict[str, Any]] = None) -> list[dict]:
		if not key_value:
			return self.get_request()[self.table]
		else:
			key = self.filter_request(key_value=key_value)[self.table.strip("s")]["id"] - 1
			return self.get_request(key=key)[self.table.strip("s")]

	def delete_data(self, key_value: Union[int, dict[str, Any]]) -> None:
		if not isinstance(key_value, int):
			key: int = self.filter_request(key_value=key_value)[self.table.strip("s")]["id"] - 1
			print(f"delete key {key}")
		else:
			key: int = key_value

		self.delete_request(key=key)

	def update_data(self, key: int, key_values: list[dict[str, Any]]) -> None:
		for key_value in key_values:
			self.put_request(key=key, key_value=key_value)


	# Requests 
	@log("model_log")
	def post_request(self, item: dict) -> dict:
		return requests.post(
			url=self.endpoint,
			json={self.table.strip("s").lower(): item}
			).json()

	@log("model_log")
	def get_request(self, key: Optional[int] = None) -> dict:
		if key is None:
			url: str = self.endpoint
		else:
			url: str = f"{self.endpoint}/{key}"
		return requests.get(
			url=url
			).json()

	@log("model_log")
	def filter_request(self, key_value: dict[str: Any]) -> dict:
		key, value = list(key_value.items())[0]
		return requests.post(
			url=self.endpoint,
			json={self.table.strip("s").lower(): 
					{
						f"filter[{key}]": value
					}
				}
			).json()

	@log("model_log")
	def delete_request(self, key: int) -> str:
		return requests.delete(
			url=f"{self.endpoint}/{key}"
			).text

	@log("model_log")
	def put_request(self, key: int, key_value: dict[str, Any]) -> dict:
		return requests.put(
			url=f"{self.endpoint}/{key}",
			json={self.table.strip("s").lower(): key_value}
			).json()