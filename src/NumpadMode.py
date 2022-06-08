from AbstractMode import AbstractMode
from Generator import Generator

from UserData import UserData

class NumpadMode(AbstractMode):

    def __init__(self):
        self.user_data = UserData()

    def loadText(self):
        gen = Generator()
        words = gen.generateOperations(self.user_data.get_word_limit())
        return words
