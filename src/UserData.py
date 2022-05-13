import json

class UserData():
    def __init__(self):
        self.file_name = "user-data.json"
        with open(self.file_name, "r") as jsonFile:
            self.data = json.load(jsonFile)

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

    def update_file(self):
        jsonFile = open(self.file_name, "w+")
        jsonFile.write(json.dumps(self.data))
        jsonFile.close()
