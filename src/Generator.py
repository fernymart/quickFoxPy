import random
class Generator:
    def __init__(self):
        self.chosen = []
    
    def generateWords(self, num):
        with open("wordlist.txt", "r") as wordfile:
            words = wordfile.read().splitlines();
            for i in range(num):
                self.chosen.append(random.choice(words))
        return self.chosen