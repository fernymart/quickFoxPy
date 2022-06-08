from abc import ABCMeta, abstractmethod

class Config(metaclass=ABCMeta):
    @abstractmethod
    def displayOption(self, stdscr):
        pass

class ConfigEnvironment():
    configList = []

    def addConfig(self, config):
        self.configList.append(config)

    def configEnvironment(self, stdscr):
        for config in self.configList:
            config.displayOption(stdscr)
        self.configList.clear()


