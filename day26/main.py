import pandas as pd
#TODO 1. Create a dictionary in this format:
{"A": "Alfa", "B": "Bravo"}

df = pd.read_csv('nato_phonetic_alphabet.csv')

code_dict = {row.letter: row.code for index, row in df.iterrows()}

#TODO 2. Create a list of the phonetic code words from a word that the user inputs.

input_string = input("input a word to be spelled: ")
string_code = [code_dict[letter.upper()] for letter in input_string]

print(string_code)
