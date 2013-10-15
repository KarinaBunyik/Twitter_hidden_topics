#!/Library/Enthought/Canopy_64bit/User python
from collections import defaultdict
import json
import sys
import xml.etree.ElementTree as ET
import pymongo
import Queue
import threading
import subprocess
from lxml import etree


global collection
global queue
global output_file


def load_data(user):
    output_file.write(json.dumps(user[0]))
    user[0]["_id"] = user[0]["id"]
    collection.save(user[0])

    #o = xmltodict.parse(infile)
    #print json.dumps(o) # '{"e": {"a": ["text", "text"]}}'

def parse_xml(file_name):
    events = ("start", "end")
    print "parsing..."
    context = etree.iterparse(file_name, events=events, remove_blank_text=True)
    #context = iter(context)
    #event, root = context.next()
    return pt(context)



def pt(context, cur_elem=None):
    items = defaultdict(list)

    if cur_elem is not None:
        items.update(cur_elem.attrib)

    text = ""
    #queue = Queue.Queue()

    for action, elem in context:
        #t = threading.Thread(target=load_data, args = (items[elem.tag]))
        #t.daemon = True

        if action == "start":
            if elem.tag == 'w':
                temp = pt(context, elem)
                temp.update({"val":elem.text})
                items[elem.tag].append(temp)
            else:
                #temp_dict = t.start()
                temp_dict = pt(context, elem)
                items[elem.tag].append(temp_dict)
            #print pt(context, elem)
        elif action == "end":
            text = elem.text.strip() if elem.text else ""
            break
        if elem.tag == 'user':
            load_data(items[elem.tag])
            #t.start()
            del items[elem.tag]

        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    del context

    if len(items) == 0:
        return text

    return { k: v[0] if len(v) == 1 else v for k, v in items.items() }

if __name__ == "__main__":
    client = pymongo.Connection('localhost', 27017)
    db = client.local
    #client = pymongo.Connection('squib.de', 27017)
    #db = client.karinas_twitter_db
    collection = db.test_short_1

    output_path = "/Users/karinabunyik/BTSync/Twitter_hidden_topics/Output/"
    output_file = open(output_path + "out_data.txt", 'wb')

    json_data = parse_xml("/Users/karinabunyik/BTSync/Twitter_hidden_topics/Test_input/tweetsShort.xml")
    #json_data = parse_xml("/Users/karinabunyik/BTSync/Data/twitter-pldebatt.xml")
    output_file.close()
    client.disconnect()
    #print(json.dumps(json_data, indent=2))
