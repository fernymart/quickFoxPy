from abc import ABCMeta, abstractmethod
import time
from ProxyUserDataLoader import ProxyUserDataLoader
from RealUserDataLoader import RealUserDataLoader

from utils import Utils

class Test(metaclass=ABCMeta):
    @abstractmethod
    def displayTest(self, stdscr, mode, char_count, errors):
        pass

class WPMTest(Test):
    def displayTest(self, stdscr, mode, char_count, errors):
        utils = Utils()

        target_text = utils.load_text(mode)
        char_count = len(target_text)
        current_text = []
        wpm = 0
        start_time = time.time()
        stdscr.nodelay(True)
        text_changed = False

        operadores = {
            "PADSLASH" : "/",
            "PADSTAR" : "*",
            "PADMINUS" : "-",
            "PADPLUS" : "+"
        }

        while True:
            time_elapsed = max(time.time() - start_time, 1)
            wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

            stdscr.clear()
            errors = utils.display_text(stdscr, target_text, current_text, text_changed, errors, wpm)
            text_changed = False
            stdscr.refresh()

            if "".join(current_text) == target_text:
                stdscr.nodelay(False)
                return wpm, char_count, errors
                # break

            try:
                key = stdscr.getkey()
            except:
                continue

            if mode == "4":
                if key in operadores:
                    text_changed = True
                    current_text.append(operadores[key])
                    continue
                

            if ord(key) == 27: # ESC
                stdscr.nodelay(False)
                break

            if key in ("KEY_BACKSPACE", '\b', "\x7f"):
                if len(current_text) > 0:
                    current_text.pop()
            elif len(current_text) < len(target_text):
                text_changed = True
                current_text.append(key)

        return wpm, char_count, errors

class TimedTest(Test):
    def displayTest(self, stdscr, mode, char_count, errors):
        utils = Utils()

        real = RealUserDataLoader()
        userDataLoader = ProxyUserDataLoader(real)
        userData = userDataLoader.getUserData()
        countdown_time = userData.get_time_limit()

        target_text = utils.load_text("3")
        current_text = []
        wpm = 0
        text_changed = False
        start_time = time.time()
        curr_time = start_time
        stdscr.nodelay(True)
        char_count = 0

        while True:
            if(time.time()-curr_time > 0.9):
                countdown_time -= 1
                curr_time = time.time()
            time_elapsed = max(time.time() - start_time, 1)
            wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

            stdscr.clear()
            errors = utils.display_text(stdscr, target_text, current_text, text_changed, errors, wpm)
            text_changed = False
            stdscr.addstr(5, 0, f"Remaining time: {countdown_time} seconds\n");
            stdscr.move(0, 0)
            stdscr.refresh()

            if "".join(current_text) == target_text:
                target_text = utils.load_text("3")
                current_text = []

            if countdown_time <= 0:
                char_count = len(current_text)
                stdscr.clear()
                stdscr.addstr("You ran out of time! Keep up practicing\n")
                stdscr.addstr("Press ESC to see results.\n") 
                stdscr.nodelay(False)
                key = stdscr.getkey()
                while ord(key) != 27:
                    key = stdscr.getkey()
                return wpm, char_count, errors

            try:
                key = stdscr.getkey()
            except:
                continue

            if ord(key) == 27: # ESC
                stdscr.nodelay(False)
                return wpm, char_count, errors

            if key in ("KEY_BACKSPACE", '\b', "\x7f"):
                if len(current_text) > 0:
                    current_text.pop()
            elif len(current_text) < len(target_text):
                text_changed = True
                if len(current_text) > char_count:
                    char_count = len(current_text)
                current_text.append(key)

class TestFactory(object):
    def create_screen(self, screen_name, stdscr, mode, char_count, errors):
        return eval(screen_name)().displayTest(stdscr, mode, char_count, errors)