
import pymongo


client = pymongo.Connection('localhost', 27017)
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

