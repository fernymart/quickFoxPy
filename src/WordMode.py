from AbstractMode import AbstractMode
from Generator import Generator

from UserData import UserData

class WordsMode(AbstractMode):

	def __init__(self):
		self.user_data = UserData()
		self.gen = Generator()

	def loadText(self):
		wordlist = self.gen.generateWords(self.user_data.get_word_limit())
		words = ' '.join(x for x in wordlist)
		return words