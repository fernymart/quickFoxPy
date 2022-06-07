from abc import ABCMeta, abstractmethod
import curses
from curses import newwin, wrapper
from UserData import UserData

user_data = UserData()
books = user_data.get_books()

total_wpm = ''
errors = ''
char_count = ''

def twitter_share(wpm, errors = None, char_count = None):
	if char_count is not None:
		url = f"http://twitter.com/share?text=Today my speed was {wpm} wpm {emojize(':muscle::grinning_face::computer:', language='alias')}%0AI made {errors} mistakes in {char_count} characters%0A%0ACan you beat me?{emojize(':flushed:', language='alias')}https://github.com/fernymart/quickFoxPy"
	elif errors is not None:
		url = f"http://twitter.com/share?text=My average speed is {wpm:.2f} wpm {emojize(':muscle::grinning_face::computer:', language='alias')}%0AI am faster than {errors:.2f}%25 of players.{emojize(':zap:', language='alias')}%0A%0ACan you beat me?{emojize(':flushed:', language='alias')}https://github.com/fernymart/quickFoxPy"
	else:
		url = f"http://twitter.com/share?text=My average speed is {wpm:.2f} wpm {emojize(':muscle::grinning_face::computer:', language='alias')}%0A%0ACan you beat me?{emojize(':flushed:', language='alias')}https://github.com/fernymart/quickFoxPy"
	webbrowser.open(url, new=0, autoraise=True)

class Screen(metaclass=ABCMeta):
    @abstractmethod
    def display(self, stdscr):
        pass

class Welcome(Screen):
    def display(self, stdscr):
        stdscr.clear()
        stdscr.addstr("Welcome to the Speed Typing Test!")
        stdscr.addstr("\nPress any key to begin!")
        stdscr.refresh()
        stdscr.getkey()

        return

class ResultsScreen(Screen):
    def display(self, stdscr):
        stdscr.addstr(1, 0,f"Your speed was: {total_wpm} wpm")
        stdscr.addstr(2, 0,f"You made {errors} mistakes when writing a total of {char_count} characters.")
        stdscr.addstr(4, 0, "You completed the text! \nPress 1 to share on Twitter or any other key to continue...")
        key = stdscr.getkey()
        if key == "1":
            twitter_share(total_wpm, errors, char_count)

class TypeScreen(Screen):
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

class ScreenFactory(object):
    def create_screen(self, screen_name, stdscr):
        return eval(screen_name)().display(stdscr)

def main(stdscr):
    fabric =  ScreenFactory()
    fabric.create_screen('ConfigMenu', stdscr)

wrapper(main)