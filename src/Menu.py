from abc import ABCMeta, abstractmethod
import curses
from curses import newwin, wrapper
from UserData import UserData

class Menu(metaclass=ABCMeta):
    @abstractmethod
    def displayMenu(self, stdscr):
        pass

class MainMenu(Menu):
    def display(self, stdscr):
        stdscr.clear()
        stdscr.addstr("MAIN MENU\n")
        stdscr.addstr("Choose practice mode\n")
        stdscr.addstr("1. Words pool\n")
        stdscr.addstr("2. Random phrase\n")
        stdscr.addstr("3. Race against time\n")
        stdscr.addstr("4. Write a book\n")
        stdscr.addstr("5. Numpad mode\n")
        stdscr.addstr("6. Settings\n")
        stdscr.addstr("7. Statistics\n")
        stdscr.addstr("8. Exit\n")

        key = stdscr.getkey()

        return key

class ConfigMenu(Menu):
    def display(self, stdscr):
        stdscr.clear()
        stdscr.addstr("Settings\n")
        stdscr.addstr("1. Change word limit\n")
        stdscr.addstr("2. Change time limit\n")
        stdscr.addstr("3. Change username\n")
        stdscr.addstr("4. Change wrong character color\n")
        stdscr.addstr("5. Change correct character color\n")
        stdscr.addstr("6. Send feedback\n")
        stdscr.addstr("7. Go Back\n")

        key = stdscr.getkey()
        return key

class BookMenu(Menu):
    def display(self, stdscr):
        stdscr.clear()
        stdscr.addstr("Books:\n")

        for i in range(0, len(books)):
            text = str(i+1) + ". " + books[i]["title"] + " ({:.4f})\n".format(books[i]["written"] / float(books[i]["total_words"]))
            stdscr.addstr(text)

        back_opt = len(books) + 1
        text = str(back_opt) + ". Go back\n"
        stdscr.addstr(text)
        stdscr.addstr("\nDuring the practice press ESC to finish.\n")
        key = stdscr.getkey()

        if key == str(back_opt):
            return -1

        try:
            return int(key) - 1
        except:
            return -1

class MenuFactory(object):
    def create_screen(self, screen_name, stdscr):
        return eval(screen_name)().display(stdscr)