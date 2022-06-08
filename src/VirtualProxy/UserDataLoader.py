from abc import ABCMeta, abstractmethod

class UserDataLoader(metaclass=ABCMeta):
    @abstractmethod
    def getUserData(self):
        pass