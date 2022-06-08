from abc import ABCMeta, abstractmethod
from Utils.Color import Color
from Command.Config import Config
from Utils.Input import Input
from VirtualProxy.ProxyUserDataLoader import ProxyUserDataLoader
from VirtualProxy.RealUserDataLoader import RealUserDataLoader
from Database.connection import GameDB
import webbrowser

class Option(metaclass=ABCMeta):
    @abstractmethod
    def displayOption(self, stdscr):
        pass

class WordLimitOption(Option, Config):
    def displayOption(self, stdscr):
        real = RealUserDataLoader()
        userDataLoader = ProxyUserDataLoader(real)
        userData = userDataLoader.getUserData()
        word_limit = userData.get_word_limit()

        input = Input()
        
        stdscr.clear()
        stdscr.addstr("Word Limit: \n")
        stdscr.addstr("Current limit: ")
        stdscr.addstr(str(word_limit))
        stdscr.addstr("\nSet new limit (max. 3 digits): ")
        s = input.get_input(stdscr, 3)

        try:
            if s != "-1":
                userData.update_word_limit(int(s))
        except:
            stdscr.addstr("\nError. The value must be numeric")
            stdscr.getkey()

class TimeLimitOption(Option, Config):
    def displayOption(self, stdscr):
        real = RealUserDataLoader()
        userDataLoader = ProxyUserDataLoader(real)
        userData = userDataLoader.getUserData()
        time_limit = userData.get_time_limit()
        
        input = Input()

        stdscr.clear()
        stdscr.addstr("Time Limit: \n")
        stdscr.addstr("Current limit: ")
        stdscr.addstr(str(time_limit))
        stdscr.addstr("\nSet new limit (max. 3 digits): ")
        s = input.get_input(stdscr, 3)

        try:
            if s != "-1":
                userData.update_time_limit(int(s))
        except:
                stdscr.addstr("\nError. The value must be numeric")
                stdscr.getkey()

class UsernameOption(Option):
    def displayOption(self, stdscr):
        real = RealUserDataLoader()
        userDataLoader = ProxyUserDataLoader(real)
        userData = userDataLoader.getUserData()

        input = Input()
        game_db = GameDB()

        stdscr.clear()
        stdscr.addstr("Username: \n")
        id, user = userData.get_user()
        if id is None:
            stdscr.addstr("Create username (max. 10 characters): ")

            while id is None:
                newuser = input.get_input(stdscr, 10)

                if newuser == "-1": break

                newuser = newuser.strip()
                stdscr.clear()

                if newuser == "": 
                    stdscr.addstr("Error. Invalid username")
                    stdscr.addstr("\nUsername: ")
                    continue
                

                id = game_db.add_username(newuser)

                if id is None:
                    stdscr.addstr("Error. Invalid username")
                    stdscr.addstr("\nUsername: ")
                else:
                    userData.save_user(id, newuser)

            stdscr.addstr("\nUser created successfully.")
            stdscr.getkey()

        else:
            stdscr.addstr("Your current username is " + user)
            stdscr.addstr("\n\nEnter your new username (max. 10 characters): ")
            newuser = input.get_input(stdscr, 10)

            if newuser != "-1":
                newuser = newuser.strip()
                updated = game_db.change_username(id, newuser)

                while not updated:
                    stdscr.clear()
                    stdscr.addstr("Error. Invalid username")
                    stdscr.addstr("Your current username is " + user)
                    stdscr.addstr(user)
                    stdscr.addstr("\n\nNew username: ")
                    newuser = input.get_input(stdscr, 10)

                    newuser = newuser.strip()

                    if newuser == "-1":
                        break
                    if newuser == "": 
                        continue
                    updated = game_db.change_username(id, newuser)

                userData.save_user(id, newuser)

                stdscr.addstr("\nUsername changed successfully.")
                stdscr.getkey()

class WrongColorOption(Option, Config):
    def displayOption(self, stdscr):
        real = RealUserDataLoader()
        userDataLoader = ProxyUserDataLoader(real)
        userData = userDataLoader.getUserData()

        color = Color()

        stdscr.clear()
        stdscr.addstr("Wrong Color: \n")
        new_color = color.color_options(stdscr)
        color.set_color(2, new_color)
        userData.change_color_opt(2, new_color)

class RightColorOption(Option, Config):
    def displayOption(self, stdscr):
        real = RealUserDataLoader()
        userDataLoader = ProxyUserDataLoader(real)
        userData = userDataLoader.getUserData()

        color = Color()

        stdscr.clear()
        stdscr.addstr("Right Color: \n")
        new_color = color.color_options(stdscr)
        color.set_color(1, new_color)
        userData.change_color_opt(1, new_color)

class FeedbackOption(Option):
    def displayOption(self, stdscr):
        url = "mailto:?to=A01197148@tec.mx&subject=Feedback speed test app"
        webbrowser.open(url, new=0, autoraise=True)

class EnvironmentOption(Option):
    def displayOption(self, stdscr):
        pass
        
class OptionFactory(object):
    def create_screen(self, screen_name, stdscr):
        return eval(screen_name)().displayOption(stdscr)