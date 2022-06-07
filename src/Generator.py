import random
class Generator:
    def __init__(self):
        self.chosen = []
    
    def generateWords(self, num):
        with open("wordlist.txt", "r") as wordfile:
            words = wordfile.read().splitlines()
            for i in range(num):
                self.chosen.append(random.choice(words))
        return self.chosen

    def generateOperations(self, num):
        text = []
        curr_num = 0
        toggle = True
        operadores = ["*", "/", "+", "-", "."]
        while curr_num < num:
            if toggle: # genera numero
                text.append(str(random.randint(0, 9999)))
                curr_num += 1
            else: # genera operador
                oper = random.choice(operadores)
                if oper == ".":
                    curr_num -= 1
                text.append(oper)
            toggle = not toggle

        text = ' '.join(text).replace(" . ", ".") # para hacer numeros con decimal
        return text
