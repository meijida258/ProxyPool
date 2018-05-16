from pymongo import MongoClient

class Mongo:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.ProxyPool
        self.collection = self.db.UsefulProxy