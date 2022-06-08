from VirtualProxy.UserDataLoader import UserDataLoader
from VirtualProxy.UserData import UserData

class RealUserDataLoader(UserDataLoader):
    def getUserData(self):
        user_data = UserData()
        return user_data