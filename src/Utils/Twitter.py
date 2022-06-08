import webbrowser
from emoji import emojize

class Twitter():
    def twitter_share(self, wpm, errors = None, char_count = None):
        if char_count is not None:
            url = f"http://twitter.com/share?text=Today my speed was {wpm} wpm {emojize(':muscle::grinning_face::computer:', language='alias')}%0AI made {errors} mistakes in {char_count} characters%0A%0ACan you beat me?{emojize(':flushed:', language='alias')}https://github.com/fernymart/quickFoxPy"
        elif errors is not None:
            url = f"http://twitter.com/share?text=My average speed is {wpm:.2f} wpm {emojize(':muscle::grinning_face::computer:', language='alias')}%0AI am faster than {errors:.2f}%25 of players.{emojize(':zap:', language='alias')}%0A%0ACan you beat me?{emojize(':flushed:', language='alias')}https://github.com/fernymart/quickFoxPy"
        else:
            url = f"http://twitter.com/share?text=My average speed is {wpm:.2f} wpm {emojize(':muscle::grinning_face::computer:', language='alias')}%0A%0ACan you beat me?{emojize(':flushed:', language='alias')}https://github.com/fernymart/quickFoxPy"
        webbrowser.open(url, new=0, autoraise=True)