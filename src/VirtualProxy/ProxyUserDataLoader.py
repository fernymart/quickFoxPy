from VirtualProxy.RealUserDataLoader import RealUserDataLoader
from VirtualProxy.UserDataLoader import UserDataLoader

class ProxyUserDataLoader(UserDataLoader):
    def __init__(self, real: RealUserDataLoader):
        self.loader = real

    def getUserData(self):
        return self.loader.getUserData()
