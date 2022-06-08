import curses
from curses import newwin, wrapper
from re import S
import time
import random
import webbrowser
from emoji import emojize
import Generator
from Menu import MenuFactory
from Option import OptionFactory
from PhraseMode import PhraseMode
from Results import ResultsFactory
from Screen import ScreenFactory
from Test import TestFactory
from UserData import UserData
from WordMode import WordsMode
from connection import GameDB
from utils import Utils

user_data = UserData()
game_db = GameDB()
errors = 0
char_count = 0
characters = user_data.get_characters() # caracteres en los que se equivoca el usuario

def main(stdscr):
    global char_count, errors
    utils = Utils()

    screenFactory = ScreenFactory()
    menuFactory = MenuFactory()
    resultsFactory = ResultsFactory()
    testFactory = TestFactory()
    optionFactory = OptionFactory()

    color_correct, color_incorrect = user_data.get_colors()
    utils.set_color(1, color_correct)
    utils.set_color(2, color_incorrect)

    screenFactory.create_screen('WelcomeScreen', stdscr)

    mode = menuFactory.create_screen('MainMenu', stdscr)

    while mode != "7":
        errors = 0

        if mode == "1":
            total_wpm, char_count, errors = testFactory.create_screen('WPMTest', stdscr, mode, char_count, errors)
            stdscr.clear()
            resultsFactory.create_screen('ResultsScreen', stdscr, total_wpm, errors, char_count)
        if mode == '2':
            total_wpm, char_count, errors = testFactory.create_screen('WPMTest', stdscr, mode, char_count, errors)
            stdscr.clear()
            resultsFactory.create_screen('ResultsScreen', stdscr, total_wpm, errors, char_count)
        if mode == '3':
            total_wpm, char_count, errors = testFactory.create_screen('TimedTest', stdscr, mode, char_count, errors)
            stdscr.clear()
            resultsFactory.create_screen('ResultsScreen', stdscr, total_wpm, errors, char_count)
        if mode == "4":
            total_wpm, char_count, errors = testFactory.create_screen('WPMTest', stdscr, mode, char_count, errors)
            stdscr.clear()
            resultsFactory.create_screen('ResultsScreen', stdscr, total_wpm, errors, char_count)
        if mode == "5":
            key = menuFactory.create_screen('ConfigMenu', stdscr)
            while key != "8":
                if key == '1':
                    optionFactory.create_screen('WordLimitOption', stdscr)
                if key == '2':
                    optionFactory.create_screen('TimeLimitOption', stdscr)
                if key == '3':
                    optionFactory.create_screen('UsernameOption', stdscr)
                if key == '4':
                    optionFactory.create_screen('WrongColorOption', stdscr)
                if key == '5':
                    optionFactory.create_screen('RightColorOption', stdscr)
                if key == '6':
                    optionFactory.create_screen('FeedbackOption', stdscr)
                if key == '7':
                    pass

                key = menuFactory.create_screen('ConfigMenu', stdscr)
        if mode == "6":
            screenFactory.create_screen('StatisticsScreen', stdscr)

        
        mode = menuFactory.create_screen('MainMenu', stdscr)

wrapper(main)