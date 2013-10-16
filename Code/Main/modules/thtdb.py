#!/usr/bin/python
# Filename: thtdb.py
import pymongo

class ThtConnection:
    def __init__(self, host=None, dbName=None, collectionName=None):
    	if host is None:
    		self.client = pymongo.MongoClient('localhost', 27017)
    	else:
    		self.client = pymongo.MongoClient(host, 27017)
    	if dbName is None:
    		self.db = self.client.local
    	else:
    		self.db = self.client[dbName]
    	if collectionName is None:
    		self.collection = self.db.test_1
    	else:
    		self.collection = self.db[collectionName]
# End of thtdb.py
