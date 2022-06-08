from abc import ABCMeta, abstractmethod
import random
from Utils.Generator import Generator
from VirtualProxy.UserData import UserData

class AbstractMode(metaclass=ABCMeta):

    def templateMode(self):
        return self.loadText()

    @abstractmethod
    def loadText(self):
        pass

class WordsMode(AbstractMode):

	def __init__(self):
		self.user_data = UserData()
		self.gen = Generator()

	def loadText(self):
		wordlist = self.gen.generateWords(self.user_data.get_word_limit())
		words = ' '.join(x for x in wordlist)
		return words

class NumpadMode(AbstractMode):

    def __init__(self):
        self.user_data = UserData()

    def loadText(self):
        gen = Generator()
        words = gen.generateOperations(self.user_data.get_word_limit())
        return words

class PhraseMode(AbstractMode):

    def loadText(self):
        with open("../files/text.txt", "r") as f:
            lines = f.readlines()
        return random.choice(lines).strip()

class TimeraceMode(AbstractMode):

    def loadText(self):
        gen = Generator()
        wordlist = gen.generateWords(20)
        words = ' '.join(x for x in wordlist)
        return words