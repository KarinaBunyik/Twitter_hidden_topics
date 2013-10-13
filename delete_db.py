import pymongo

# insert the date into MongoDB
db = pymongo.Connection()
db.drop_database('mydatabase')