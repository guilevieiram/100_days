import unittest
from main import BirthdayManager, EmailManager, BirthdayBot, LetterManager

class BirthdayManagerTest(unittest.TestCase):

	def setUp(self):
		self.bm = BirthdayManager(path="birthdays.csv")
	
	def test_get_birthday_person(self):
		self.assertEqual(self.bm.get_birthday_person(day=27,month=7),
						["Gui1", "Buca"]
			)

	def test_get_person_email_correct(self):
		self.assertEqual(
			self.bm.get_person_email(name="Gui1"),
			"guilhermevmanhaes@gmail.com"
			)	

	def test_get_person_email_incorrect(self):

		self.assertEqual(
			self.bm.get_person_email(name="gu"),
			""
			)	

class LetterManagerTest(unittest.TestCase):

	def setUp(self):
		self.lm = LetterManager("letter_templates")

	def test_letter_manager_initializer(self):
		self.assertEqual(
			self.lm.letters_names,
			["letter_1.txt", "letter_2.txt", "letter_3.txt"]
			)	

	def test_get_letter(self):
		self.assertEqual(
			self.lm.get_letter(letter_name="letter_1.txt"),
'''Dear [NAME],

Happy birthday!

All the best for the year!

Guilherme'''
			)

	def test_fill_letter(self):
		self.lm.letter = "Dear [NAME],"
		self.assertEqual(
			self.lm.fill_letter(name = "gui"),
			"Dear gui,"			
			)

	def test_get_random_letter(self):
		self.assertIn(
			self.lm.get_random_letter(name="gui"),
['''Dear gui,

Happy birthday!

All the best for the year!

Guilherme''','''Hey gui,

Happy birthday! Have a wonderful time today and eat lots of cake!

Lots of love,

Guilherme''','''Dear gui,

It's your birthday! Have a great day!

All my love,

Guilherme'''
]
			)

if __name__ == '__main__':
    unittest.main()