import pymongo

# insert the date into MongoDB
connection = pymongo.Connection('localhost', 27017)
print(connection.database_names())
#db.collection.drop()

db = connection[u'local'] 
print(db.collection_names())  
print(u'startup_log' in db.collection_names())
collection = db[u'startup_log']
print(collection.count() == 0)

collection.drop()