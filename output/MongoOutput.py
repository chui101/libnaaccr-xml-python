from pymongo import MongoClient

class MongoOutput:
    def __init__(self, host='localhost', port=27017, db='test', collection='naaccr'):
        self.client = MongoClient(host=host, port=port)
        self.db = self.client[db]
        self.collection = self.db[collection]

    def output(self,record):
        self.collection.insert_one(record)