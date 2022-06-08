from abc import abstractmethod

class AbstractMode():

    def templateMode(self):
        return self.loadText()

    @abstractmethod
    def loadText(self):
        pass