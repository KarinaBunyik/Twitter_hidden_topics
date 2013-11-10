
from pymongo import ASCENDING, DESCENDING, Connection
import thtdb
import io
from thtpaths import output_path


def querries():
    print "first element..."
    u = db.collection.find_one()
    print u[u'text']

    print "finding feliciananasi..."
    for user in db.collection.find({u'username': u'feliciananasi'}):
        print user

    print "counting all users..."
    print db.collection.count()

    print "counting feliciananasis..."
    print db.collection.find({u'username': u'feliciananasi'}).count()

    print "find users created..."
    d = "2008-01-01"
    for user in db.collection.find({"created": {"$gt": d}}).sort("username"):
        print user
    print db.collection.find({"created": {"$gt": d}}).sort("username").explain()["cursor"]
    print db.collection.find({"created": {"$gt": d}}).sort("username").explain()["nscanned"]

    print "find indexed users created..."
    d = "2008-01-01"
    db.collection.create_index([("created", DESCENDING), ("username", ASCENDING)])
    print db.collection.find({"created": {"$lt": d}}).sort("username").explain()["cursor"]
    print db.collection.find({"created": {"$lt": d}}).sort("username").explain()["nscanned"]
    for user in db.collection.find({"created": {"$lt": d}}).sort("username"):
        print user["username"]
    print "aggregation example..."

if __name__ == "__main__":
	#client = Connection('localhost', 27017)
	#db = client.local
	#collection = db.test_3
    db = thtdb.ThtConnection(collectionName='test_pldebatt_june')
    querries()