from UserData import UserData

class LoadProxy():
    def __init__(self, bookMenu):
        self.bookMenu = bookMenu

    def load(self):
        user_data = UserData()
        print(user_data.get_books())
        self.bookMenu.driver = user_data.get_books()
        self.bookMenu.driver.load()