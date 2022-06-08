from UserDataLoader import UserDataLoader
from UserData import UserData

class RealUserDataLoader(UserDataLoader):
    def getUserData(self):
        user_data = UserData()
        return user_data