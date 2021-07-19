import pandas as pd
import string

df = pd.read_csv('nato_phonetic_alphabet.csv')

code_dict = {row.letter: row.code for index, row in df.iterrows()}

while True:
	
	input_string = input("input a word to be spelled: ")
	
	try:
		string_code = [code_dict[letter.upper()] for letter in input_string]
	except KeyError:
		print("only letters please...")
	else:
		print(" ".join(string_code))

