from AbstractMode import AbstractMode
from Generator import Generator

class TimeraceMode(AbstractMode):

    def loadText(self):
        gen = Generator()
        wordlist = gen.generateWords(20)
        words = ' '.join(x for x in wordlist)
        return words