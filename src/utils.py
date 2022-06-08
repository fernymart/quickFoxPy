from TimeraceMode import TimeraceMode
from NumpadMode import NumpadMode
from PhraseMode import PhraseMode
from ProxyUserDataLoader import ProxyUserDataLoader
from RealUserDataLoader import RealUserDataLoader
import webbrowser
from emoji import emojize
import curses

from WordMode import WordsMode

class Utils():
    def save_results(self, wpm, errors, char_count):
        real = RealUserDataLoader()
        userDataLoader = ProxyUserDataLoader(real)
        userData = userDataLoader.getUserData()
        characters = userData.get_characters()
        userData.update_characters(characters)
        
        with open("../files/wrong_chars.txt", "a") as file: # guarda la cantidad de caracteres en los equivocó por cada 10 escritos
                file.write(f"{10 * errors / char_count}\n")

        if(wpm is not None and wpm > 0):
            with open("../files/results.txt", "a") as file:
                file.write(f"{wpm}\n")
    
    def twitter_share(self, wpm, errors = None, char_count = None):
        if char_count is not None:
            url = f"http://twitter.com/share?text=Today my speed was {wpm} wpm {emojize(':muscle::grinning_face::computer:', language='alias')}%0AI made {errors} mistakes in {char_count} characters%0A%0ACan you beat me?{emojize(':flushed:', language='alias')}https://github.com/fernymart/quickFoxPy"
        elif errors is not None:
            url = f"http://twitter.com/share?text=My average speed is {wpm:.2f} wpm {emojize(':muscle::grinning_face::computer:', language='alias')}%0AI am faster than {errors:.2f}%25 of players.{emojize(':zap:', language='alias')}%0A%0ACan you beat me?{emojize(':flushed:', language='alias')}https://github.com/fernymart/quickFoxPy"
        else:
            url = f"http://twitter.com/share?text=My average speed is {wpm:.2f} wpm {emojize(':muscle::grinning_face::computer:', language='alias')}%0A%0ACan you beat me?{emojize(':flushed:', language='alias')}https://github.com/fernymart/quickFoxPy"
        webbrowser.open(url, new=0, autoraise=True)

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

    def set_color(self, type, color):
        if color == 0:
            curses.init_pair(type, curses.COLOR_RED, curses.COLOR_BLACK)
        elif color == 1:
            curses.init_pair(type, curses.COLOR_GREEN, curses.COLOR_BLACK)
        elif color == 2:
            curses.init_pair(type, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        elif color == 3:
            curses.init_pair(type, curses.COLOR_BLUE, curses.COLOR_BLACK)
        elif color == 4:
            curses.init_pair(type, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        elif color == 5:
            curses.init_pair(type, curses.COLOR_CYAN, curses.COLOR_BLACK)

    def color_options(self, stdscr):
        colors = ["red", "green", "yellow", "blue", "magenta", "cyan"]
        for i in range(0, len(colors)):
            stdscr.addstr(f"{i + 1}. {colors[i]}\n")

        stdscr.addstr("7. Go back\n")
        key = stdscr.getkey()

        if key == "7":
            return -1

        try:
            return int(key) - 1
        except:
            return -1

    def display_estadisticas(self, stdscr):
        real = RealUserDataLoader()
        userDataLoader = ProxyUserDataLoader(real)
        userData = userDataLoader.getUserData()
        characters = userData.get_wrong_char()

        promedio = 0
        promedio_chars = 0
        suma = 0
        with open("../files/results.txt", "r") as file:
            resultados = file.readlines()
            for resultado in resultados:
                suma+=float(resultado)
            promedio = suma / len(resultados)

        suma = 0
        with open("../files/wrong_chars.txt", "r") as file:
            resultados = file.readlines()
            for resultado in resultados:
                suma+=float(resultado)
            promedio_chars = suma / len(resultados)

        stdscr.addstr(3, 0, f"Average: {promedio:.2f} wpm")
        stdscr.addstr(4, 0,f"The character you have gotten wrong more times is {characters}")
        stdscr.addstr(5, 0, f"On average you make {promedio_chars:.2f} mistakes every 10 characters.")
        return promedio, promedio_chars
    
    def get_input(self, stdscr, limit):
        count = 0
        text = ""
        while count < limit:
            key = stdscr.getkey()
            
            if ord(key) == 10 or ord(key) == 13: # Enter
                break

            if ( ord(key.upper()) >= 65 and ord(key.upper()) <= 90 ) or ( ord(key) >= 48 and ord(key) <= 57 ): # letra o numero
                stdscr.addstr(key)
                text += key
                count += 1

        stdscr.addstr("\n\nPress any key to save settings or ESC to cancel...")
        key = stdscr.getkey()

        if ord(key) == 27: # ESC (cancelar)
            text = "-1"

        return text