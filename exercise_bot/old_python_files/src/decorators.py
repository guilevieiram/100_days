import json
import datetime

def log(name):
	def logger(function):
		def wrapper(*args, **kwargs):
			with open(f"{name}.txt", "a") as log_file:
				result = function(*args, **kwargs)	
				log_file.write(datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + "\n\n")
				log_file.write(function.__name__ + "\n\n")
				log_file.write(json.dumps(result, indent=4))
				log_file.write("\n--------------------------------------\n")
			return result		
		return wrapper
	return logger