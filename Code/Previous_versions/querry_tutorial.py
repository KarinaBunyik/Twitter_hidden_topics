
from pymongo import ASCENDING, DESCENDING, Connection
import datetime
import codecs
import io
from gensim import corpora, models, similarities


client = Connection('localhost', 27017)
db = client.local
collection = db.test_2

#print "first element..."
#print collection.find_one()

#print "finding feliciananasi..."
#for user in collection.find({u'username': u'feliciananasi'}):
#    print user

#print "counting all users..."
#print collection.count()

#print "counting feliciananasis..."
#print collection.find({u'username': u'feliciananasi'}).count()

#print "find users created..."
#d = "2008-01-01"
#for user in collection.find({"created": {"$gt": d}}).sort("username"):
#    print user
#print collection.find({"created": {"$gt": d}}).sort("username").explain()["cursor"]
#print collection.find({"created": {"$gt": d}}).sort("username").explain()["nscanned"]

#print "find indexed users created..."
#d = "2008-01-01"
#collection.create_index([("created", DESCENDING), ("username", ASCENDING)])
#print collection.find({"created": {"$lt": d}}).sort("username").explain()["cursor"]
#print collection.find({"created": {"$lt": d}}).sort("username").explain()["nscanned"]
#for user in collection.find({"created": {"$lt": d}}).sort("username"):
#    print user["username"]

#print "aggregation example..."

output_path = "/Users/karinabunyik/BTSync/Twitter_hidden_topics/Output/"
output_file = io.open(output_path + "out_data1.txt", 'w', encoding='utf-8')

print "first LDA document..."
words_list = []
#collection.create_index([("username", ASCENDING)])
#for user in collection.find({u'username': u'feliciananasi'}):
print "documents loading to file..."
for user in collection.find():
	if "text" in user:
		#if len(user["text"])>0 and :
		if type(user["text"]) is list:
			#print len(user["text"]), user["text"]
			if "sentence" in user["text"][0]:
				if "w" in user["text"][0]["sentence"]:
					for word in user["text"][0]["sentence"]["w"]:
						if type(word) is dict:
							#words_list.append(word["val"]) #.encode('UTF-8'))
							output_file.write('%s ' % word["val"])
					output_file.write(u"\r")
		else:
			if "sentence" in user["text"]:
				if "w" in user["text"]["sentence"]:
					pass
			#		for word in user["text"][0]["sentence"]["w"]:
			#			words_list.append(word["val"]) #.encode('UTF-8'))
        	#			output_file.write('%s ' % word["val"])
        		#words_list = []
output_file.close()
#print words_list
print "documents loading to memory..."
documents = []
with io.open(output_path + "out_data1.txt", 'r', encoding='utf-8') as input_file:
	for line in input_file:
		documents.append(line)

print "tokenization..."
# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]

print "removing unique words..."
# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
#texts = [[word for word in text if word not in tokens_once] for text in texts]

print "dumping texts to file..."
output_file2 = io.open(output_path + "out_data2.txt", 'w', encoding='utf-8')
for text in texts:
	output_file2.write([word for word in text if word not in tokens_once])

#print "documents: ", documents
#print "stoplist: ", stoplist
#print "texts: ", texts
input_file.close()
#'\xf6'output_file.write(words_list)