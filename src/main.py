from curses import wrapper
from Templates.AbstractDisplay import TimedDisplay, WPMDisplay
from Utils.Color import Color
from Command.Config import ConfigEnvironment
from Factory.Menu import MenuFactory
from Factory.Option import OptionFactory, RightColorOption, TimeLimitOption, WordLimitOption, WrongColorOption
from VirtualProxy.ProxyUserDataLoader import ProxyUserDataLoader
from VirtualProxy.RealUserDataLoader import RealUserDataLoader
from Factory.Screen import ScreenFactory

errors = 0
char_count = 0

def main(stdscr):
    global char_count, errors
    real = RealUserDataLoader()
    userDataLoader = ProxyUserDataLoader(real)
    userData = userDataLoader.getUserData()

    color = Color()

    screenFactory = ScreenFactory()
    menuFactory = MenuFactory()
    optionFactory = OptionFactory()

    color_correct, color_incorrect = userData.get_colors()
    color.set_color(1, color_correct)
    color.set_color(2, color_incorrect)

    screenFactory.create_screen('WelcomeScreen', stdscr)

    mode = menuFactory.create_screen('MainMenu', stdscr)

    while mode != "7":
        errors = 0

        if mode == "1":
            wpmDisplay = WPMDisplay()
            wpmDisplay.render(stdscr, mode, char_count, errors)
        if mode == '2':
            wpmDisplay = WPMDisplay()
            wpmDisplay.render(stdscr, mode, char_count, errors)
        if mode == '3':
            wpmDisplay = TimedDisplay()
            wpmDisplay.render(stdscr, mode, char_count, errors)
        if mode == "4":
            wpmDisplay = WPMDisplay()
            wpmDisplay.render(stdscr, mode, char_count, errors)
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
                    configEnvironment = ConfigEnvironment()
                    configEnvironment.addConfig(WordLimitOption())
                    configEnvironment.addConfig(TimeLimitOption())
                    configEnvironment.addConfig(RightColorOption())
                    configEnvironment.addConfig(WrongColorOption())
                    configEnvironment.configEnvironment(stdscr)

                key = menuFactory.create_screen('ConfigMenu', stdscr)
        if mode == "6":
            screenFactory.create_screen('StatisticsScreen', stdscr)

        
        mode = menuFactory.create_screen('MainMenu', stdscr)

wrapper(main)