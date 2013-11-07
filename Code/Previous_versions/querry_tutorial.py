
from pymongo import ASCENDING, DESCENDING, Connection
import thtdb
import io
from thtpaths import output_path

def querries():
    #print "first element..."
    #u = db.collection.find_one()
    #print u[u'text']

    #print "finding feliciananasi..."
    #for user in db.collection.find({u'username': u'feliciananasi'}):
    #    print user

    #print "counting all users..."
    #print db.collection.count()

    #print "counting feliciananasis..."
    #print db.collection.find({u'username': u'feliciananasi'}).count()

    user_stat_filename = output_path+"user_stat_june"
    user_stat_file = io.open(user_stat_filename+'.out', 'wb')

    count = 0
    user_stat = dict()
    for user in db.collection.find():
        if u'username' in user:
            username = user[u'username']
            count += 1
            if True:
                if u'text' in user:
                    if isinstance(user[u'text'], dict): 
                        #print 'text type:', type(user[u'text'])
                        if u'hashtags' in user[u'text']:
                            if "pldebatt" in user[u'text'][u'hashtags']:
                                if username in user_stat:
                                    user_stat[username] += 1
                                else:
                                    user_stat[username] = 1
                #elif isinstance(user[u'text'], basestring):
                    else:
                        #print type(user[u'text'])
                        for text in user[u'text']:
                            if u'hashtags' in text:
                                if "pldebatt" in text[u'hashtags']:
                                    if username in user_stat:
                                        user_stat[username] += 1
                                    else:
                                        user_stat[username] = 1
                #else:
                #    print "ERROR"
                    #print type(user[u'text'])
    #print max(user_stat.iteritems(), key=operator.itemgetter(1))[0]
    while user_stat != {}:
        max_key = max(user_stat.iterkeys(), key=(lambda key: user_stat[key]))
        max_val = user_stat[max_key]
        user_stat_file.write(max_key.encode('utf8')+','+str(max_val)+'\n')
        #print max_key, max_val
        del user_stat[max_key]
    #print list(sorted(user_stat, key=user_stat.__getitem__, reverse=True))


                    #if u'sentence' in user[u'text']:
                    #    if isinstance(user[u'text'][u'sentence'], dict):
                    #        print 'sentence type:', type(user[u'text'][u'sentence'])
                    #        print user[u'text'][u'hashtags']
                    #if isinstance(user[u'text'][u'sentence'], dict):
                    #    pass
                        #if not isinstance(user[u'text'][u'sentence'], dict):
                        #    print (user[u'text'][u'sentence'])
                        #    for sentence in user[u'text'][u'sentence']:
                        #        print sentence
                #for key, val in user[u'text'].iteritems():
                #    print 'text: ', key, val
                    #if u'sentence' in text:
                    #    if isinstance(text[u'sentence'], dict):
                    #        pass
                    #print 'sentence', type(text[u'sentence'])
                            #for sentence in text[u'sentence']:
                             #   print "a"
                    #print type(text[u'sentence'])

    #print "find users created..."
    #d = "2008-01-01"
    #for user in db.collection.find({"created": {"$gt": d}}).sort("username"):
    #    print user
    #print db.collection.find({"created": {"$gt": d}}).sort("username").explain()["cursor"]
    #print db.collection.find({"created": {"$gt": d}}).sort("username").explain()["nscanned"]

    #print "find indexed users created..."
    #d = "2008-01-01"
    #db.collection.create_index([("created", DESCENDING), ("username", ASCENDING)])
    #print db.collection.find({"created": {"$lt": d}}).sort("username").explain()["cursor"]
    #print db.collection.find({"created": {"$lt": d}}).sort("username").explain()["nscanned"]
    #for user in db.collection.find({"created": {"$lt": d}}).sort("username"):
    #    print user["username"]
    #print "aggregation example..."

if __name__ == "__main__":
	#client = Connection('localhost', 27017)
	#db = client.local
	#collection = db.test_3
    db = thtdb.ThtConnection(collectionName='test_2')
    querries()