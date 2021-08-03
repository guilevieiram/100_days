import requests
import pandas as pd

from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Union, Optional, Any

from src.decorators import log

# Abstract Classes
class DataBase(ABC):

	@abstractmethod
	def __init__(self, project: str, table: str) -> None:
		pass

	@abstractmethod
	def add_data(self, data: list[dict]) -> None:
		pass

	@abstractmethod
	def get_data(self, key_value: Optional[dict[str, Any]]) -> list[dict]:
		pass

	@abstractmethod
	def delete_data(self, key: int) -> None:
		pass

	@abstractmethod
	def update_data(self, key: int, key_values: list[dict[str, Any]]) -> None:
		pass

# Data base implementations		
class PandasDB(DataBase):

	def __init__(self, project: str, table: str) -> None:
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

	def update_data(self, key: int, key_values: list[dict[str, Any]]) -> None:
		for key_value in key_values:
			column, value = list(key_value.items())[0]
			self.data.at[key, column] = value 
		self.update_table()

	def update_table(self) -> None:
		self.data.to_csv(self.path, index=False)

class Sheety(DataBase):

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
