#import pymongo
#from lxml import etree
import xmltodict, json

# parse xml file

#parser = etree.XMLParser()
#infile = open('twitter-pldebatt.xml')
infile = open('example.xml')
#root = etree.parse(infile)

#events = []
#for event in root.xpath('.//event'):
#    event = {'name': event.find('name').text}
#    events.append(event)

#print events

# insert the date into MongoDB
#db = pymongo.MongoClient()
#db = pymongo.Connection()
#collection = db.test

#collection.insert(events)

o = xmltodict.parse(infile)
print json.dumps(o) # '{"e": {"a": ["text", "text"]}}'