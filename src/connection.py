from bson import ObjectId
import pymongo

class GameDB:
    def __init__(self):
        self.uri = "mongodb+srv://typing:apis@cluster0.ud4pu.mongodb.net/?retryWrites=true&w=majority"

    def add_username(self, username):
        with pymongo.MongoClient(self.uri) as client:
            db = client['TypingTest']
            users = db['users']
            data = {'username': username }

            user = users.find_one(data)

            if user:
                return None
            
            id = users.insert_one(data).inserted_id
            return str(id)

    def change_username(self, id, username):
        with pymongo.MongoClient(self.uri) as client:
            db = client['TypingTest']
            users = db['users']
            find = { '_id' : ObjectId(id) }
            newdata = {'username': username }

            user = users.find_one(newdata)

            if user:
                return False

            users.update_one(find, {"$set": newdata })
            return True

    def post_stats(self, userid, stat):
        with pymongo.MongoClient(self.uri) as client:
            db = client['TypingTest']
            stats = db['stats']
            find = { 'user' : ObjectId(userid) }
            data = {'speed': stat }
            stats.update_one(find, {"$set": data }, upsert=True)

    def get_stats(self, stat):
        with pymongo.MongoClient(self.uri) as client:
            db = client['TypingTest']
            stats = db['stats']
            total = stats.count_documents({})
            lower = stats.count_documents({ 'speed' : { '$lt' : stat } })

            # está por encima del x%
            return lower / total * 100