import curses
from Templates.AbstractMode import NumpadMode, PhraseMode, TimeraceMode, WordsMode
from VirtualProxy.ProxyUserDataLoader import ProxyUserDataLoader
from VirtualProxy.RealUserDataLoader import RealUserDataLoader

class Text():
    def load_text(self, modo):
        if modo == "1":
            concreteMode = WordsMode()
            return concreteMode.templateMode()
        elif modo == "2":
            concreteMode = PhraseMode()
            return concreteMode.templateMode()
        elif modo == "3":
            concreteMode = TimeraceMode()
            return concreteMode.templateMode()
        elif modo == "4":
            concreteMode = NumpadMode()
            return concreteMode.templateMode()

        return 0
    
    def display_text(self, stdscr, target, current, text_changed, errors, wpm=0):
        real = RealUserDataLoader()
        userDataLoader = ProxyUserDataLoader(real)
        userData = userDataLoader.getUserData()
        characters = userData.get_characters()

        stdscr.addstr(target)
        stdscr.addstr(f"\nWPM: {wpm}")
        stdscr.move(0, 0)
        for i, char in enumerate(current):
            correct_char = target[i]
            color = curses.color_pair(1)
            if char != correct_char and not (ord(correct_char) == 8217 and ord(char) == 39):
                color = curses.color_pair(2)
            try:
                stdscr.addstr(char, color)
            except curses.error: 
                pass

        if text_changed and len(current) > 0 and target[len(current) - 1] != current[-1]: # solo revisa si se equivocó en el último caracter que se escribió
            characters[target[len(current) - 1]] = characters.get(target[len(current) - 1], 0) + 1
            errors += 1

        return errors