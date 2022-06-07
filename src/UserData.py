import json

class UserData():
    def __init__(self):
        self.file_name = "user-data.json"
        with open(self.file_name, "r") as jsonFile:
            self.data = json.load(jsonFile)

    def get_user(self):
        if "id" not in self.data:
            return None, None
        return self.data["id"], self.data["username"]

    def save_user(self, id, username):
        self.data["username"] = username
        self.data["id"] = id
        self.update_file()

    def get_word_limit(self):
        return self.data["word_limit"]

    def update_word_limit(self, limit):
        self.data["word_limit"] = limit
        self.update_file()

    def get_time_limit(self):
        return self.data["time_limit"]

    def update_time_limit(self, limit):
        self.data["time_limit"] = limit
        self.update_file()

    def get_books(self):
        return self.data["books"]
    
    def update_written_words(self, book, value):
        self.data["books"][book]["written"] += value
        self.update_file()

    def get_characters(self):
        if "wrong_chars" in self.data:
            return self.data["wrong_chars"]
        else:
            return {}

    def update_characters(self, chars):
        self.data["wrong_chars"] = chars
        self.update_file()

    def get_wrong_char(self):
        if "wrong_chars" in self.data:
            return max(self.data["wrong_chars"], key=self.data["wrong_chars"].get)
        return " "

    def get_colors(self):
        if "colors" in self.data:
            return self.data["colors"]["correct"], self.data["colors"]["incorrect"]
        else:
            self.data["colors"] = {}
            self.data["colors"]["correct"] = 1
            self.data["colors"]["incorrect"] = 0
            self.update_file()
            return 1, 0

    def change_color_opt(self, type, color):
        if type == 1:
            self.data["colors"]["correct"] = color
        elif type == 2:
            self.data["colors"]["incorrect"] = color
        self.update_file()

    def update_file(self):
        jsonFile = open(self.file_name, "w+")
        jsonFile.write(json.dumps(self.data))
        jsonFile.close()
