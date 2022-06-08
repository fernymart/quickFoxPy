from abc import ABCMeta, abstractmethod
import curses
from curses import newwin, wrapper
from ProxyUserDataLoader import ProxyUserDataLoader
from RealUserDataLoader import RealUserDataLoader

class Menu(metaclass=ABCMeta):
    @abstractmethod
    def displayMenu(self, stdscr):
        pass

class MainMenu(Menu):
    def displayMenu(self, stdscr):
        stdscr.clear()
        stdscr.addstr("MAIN MENU\n")
        stdscr.addstr("Choose practice mode\n")
        stdscr.addstr("1. Words pool\n")
        stdscr.addstr("2. Random phrase\n")
        stdscr.addstr("3. Race against time\n")
        stdscr.addstr("4. Numpad mode\n")
        stdscr.addstr("5. Settings\n")
        stdscr.addstr("6. Statistics\n")
        stdscr.addstr("7. Exit\n")

        key = stdscr.getkey()

        return key

class ConfigMenu(Menu):
    def displayMenu(self, stdscr):
        stdscr.clear()
        stdscr.addstr("Settings\n")
        stdscr.addstr("1. Change word limit\n")
        stdscr.addstr("2. Change time limit\n")
        stdscr.addstr("3. Change username\n")
        stdscr.addstr("4. Change wrong character color\n")
        stdscr.addstr("5. Change correct character color\n")
        stdscr.addstr("6. Send feedback\n")
        stdscr.addstr("7. Set environment\n")
        stdscr.addstr("8. Go Back\n")

        key = stdscr.getkey()
        return key

class MenuFactory(object):
    def create_screen(self, screen_name, stdscr):
        return eval(screen_name)().displayMenu(stdscr)