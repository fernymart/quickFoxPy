from abc import ABCMeta, abstractmethod
import curses
from curses import newwin, wrapper
from ProxyUserDataLoader import ProxyUserDataLoader
from RealUserDataLoader import RealUserDataLoader
from connection import GameDB
from utils import Utils

class Screen(metaclass=ABCMeta):
    @abstractmethod
    def display(self, stdscr):
        pass

class WelcomeScreen(Screen):
    def display(self, stdscr):
        stdscr.clear()
        stdscr.addstr("Welcome to the Speed Typing Test!")
        stdscr.addstr("\nPress any key to begin!")
        stdscr.refresh()
        stdscr.getkey()
        return

class StatisticsScreen(Screen):
    def display(self, stdscr):
        utils = Utils()

        stdscr.clear()
        stdscr.addstr(1, 0, "Statistics")
        promedio, promedio_chars = utils.display_estadisticas(stdscr)

        stdscr.addstr("\n\nPress 1 to share your statistics on Twitter.")
        stdscr.addstr("\nPress 2 to share your statistics with other users of this app.")
        stdscr.addstr("\n\nPress any other key to return to main menu...")
        key = stdscr.getkey()

        if key == "2":
            real = RealUserDataLoader()
            userDataLoader = ProxyUserDataLoader(real)
            userData = userDataLoader.getUserData()
            id, user = userData.get_user()

            if id is None:
                stdscr.addstr("\n\nIt seems like you do not have a registered user. Please, register one in the settings.")
                stdscr.getkey()
            else:
                game_db = GameDB()
                game_db.post_stats(id, promedio, promedio_chars)
                percentage, percentage_chars = game_db.get_stats(promedio, promedio_chars)

                stdscr.addstr(f"\n\nIn terms of speed, you are above the {percentage:.2f}% of the users of this app.")
                stdscr.addstr(f"\nIn terms of number of mistakes made, you are above the {percentage_chars:.2f}% of the users of this app.")
                stdscr.addstr(f"\n\nPress 1 to share on Twitter.")
                stdscr.addstr("\nPress any other key to return to main menu...")

                key = stdscr.getkey()
                if key == "1":
                    utils.twitter_share(promedio, percentage)
        elif key == "1":
            utils.twitter_share(promedio)


class ScreenFactory(object):
    def create_screen(self, screen_name, stdscr):
        return eval(screen_name)().display(stdscr)