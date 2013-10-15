
from pymongo import ASCENDING, DESCENDING, Connection
import datetime


client = Connection('localhost', 27017)
db = client.local
collection = db.test_1

print "first element..."
print collection.find_one()

print "finding feliciananasi..."
for user in collection.find({u'username': u'feliciananasi'}):
    print user

print "counting all users..."
print collection.count()

print "counting feliciananasis..."
print collection.find({u'username': u'feliciananasi'}).count()

#print "find users created..."
d = "2005-01-01"
#for user in collection.find({"created": {"$gt": d}}).sort("username"):
#    print user
#print collection.find({"created": {"$gt": d}}).sort("username").explain()["cursor"]
#print collection.find({"created": {"$gt": d}}).sort("username").explain()["nscanned"]

print "find indexed users created..."
collection.create_index([("created", DESCENDING), ("username", ASCENDING)])
print collection.find({"created": {"$lt": d}}).sort("username").explain()["cursor"]
print collection.find({"created": {"$lt": d}}).sort("username").explain()["nscanned"]
#date_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')