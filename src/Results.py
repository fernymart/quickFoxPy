from abc import ABCMeta, abstractmethod
from utils import Utils

class Results(metaclass=ABCMeta):
    @abstractmethod
    def displayResults(self, stdscr, total_wpm, errors, char_count):
        pass

class ResultsScreen(Results):
    def displayResults(self, stdscr, total_wpm, errors, char_count):
        utils = Utils()
        stdscr.clear()
        utils.save_results(total_wpm, errors, char_count)
        stdscr.addstr(1, 0,f"Your speed was: {total_wpm} wpm")
        stdscr.addstr(2, 0,f"You made {errors} mistakes when writing a total of {char_count} characters.")
        stdscr.addstr(4, 0, "You completed the text! \nPress 1 to share on Twitter or any other key to continue...")
        key = stdscr.getkey()
        if key == "1":
            utils.twitter_share(total_wpm, errors, char_count)

class ResultsFactory(object):
    def create_screen(self, screen_name, stdscr, total_wpm, errors, char_count):
        return eval(screen_name)().displayResults(stdscr, total_wpm, errors, char_count)