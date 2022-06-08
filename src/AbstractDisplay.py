from abc import ABCMeta, abstractmethod
from Results import ResultsFactory

from Test import TestFactory


class AbstractDisplay(metaclass=ABCMeta):
    def render(self, stdscr, mode, char_count, errors):
        total_wpm, char_count, errors = self.renderTest(stdscr, mode, char_count, errors)
        self.clear(stdscr)
        self.renderResults(stdscr, total_wpm, errors, char_count)

    @abstractmethod
    def renderTest(self, program_name, stdscr, mode, char_count, errors):
        pass

    def clear(self, stdscr):
        stdscr.clear()
    
    def renderResults(self, stdscr, total_wpm, errors, char_count):
        resultsFactory = ResultsFactory()
        return resultsFactory.create_screen('ResultsScreen', stdscr, total_wpm, errors, char_count)

class WPMDisplay(AbstractDisplay):
    def renderTest(self, stdscr, mode, char_count, errors):
        testFactory = TestFactory()
        return testFactory.create_screen('WPMTest', stdscr, mode, char_count, errors)        

class TimedDisplay(AbstractDisplay):
    def renderTest(self, stdscr, mode, char_count, errors):
        testFactory = TestFactory()
        return testFactory.create_screen('TimedTest', stdscr, mode, char_count, errors)  