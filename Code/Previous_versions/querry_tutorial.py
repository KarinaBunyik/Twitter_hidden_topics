
from pymongo import ASCENDING, DESCENDING, Connection

def querries():
    print "first element..."
    print collection.find_one()

    print "finding feliciananasi..."
    for user in collection.find({u'username': u'feliciananasi'}):
        print user

    print "counting all users..."
    print collection.count()

    print "counting feliciananasis..."
    print collection.find({u'username': u'feliciananasi'}).count()

    print "find users created..."
    d = "2008-01-01"
    for user in collection.find({"created": {"$gt": d}}).sort("username"):
        print user
    print collection.find({"created": {"$gt": d}}).sort("username").explain()["cursor"]
    print collection.find({"created": {"$gt": d}}).sort("username").explain()["nscanned"]

    print "find indexed users created..."
    d = "2008-01-01"
    collection.create_index([("created", DESCENDING), ("username", ASCENDING)])
    print collection.find({"created": {"$lt": d}}).sort("username").explain()["cursor"]
    print collection.find({"created": {"$lt": d}}).sort("username").explain()["nscanned"]
    for user in collection.find({"created": {"$lt": d}}).sort("username"):
        print user["username"]

    print "aggregation example..."

if __name__ == "__main__":
	client = Connection('localhost', 27017)
	db = client.local
	collection = db.test_1
