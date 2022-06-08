from AbstractMode import AbstractMode
import random

class PhraseMode(AbstractMode):

    def loadText(self):
        with open("text.txt", "r") as f:
            lines = f.readlines()
        return random.choice(lines).strip()