import json
import datetime

def log(name: str):
	def logger(function):
		def wrapper(*args, **kwargs):
			with open(f"{name}.txt", "a") as log_file:
				result = function(*args, **kwargs)	
				log_file.write(str(datetime.datetime.now()))
				log_file.write(function.__name__ + "\n\n")
				log_file.write(json.dumps(result, indent=4))
			return result		
		return wrapper
	return logger