from collections import defaultdict
import json
import sys
#import xml.etree.ElementTree as ET
import pymongo
import Queue
import threading
from lxml import etree


global collection
global queue


def load_data(user):

    collection.insert(user)

    #o = xmltodict.parse(infile)
    #print json.dumps(o) # '{"e": {"a": ["text", "text"]}}'

def parse_xml(file_name):
    events = ("start", "end")
    context = etree.iterparse(file_name, events=events)

    file1 = open("dataFile1.xml", 'wb')
    file2 = open("dataFile2.xml", 'wb')
    file3 = open("dataFile3.xml", 'wb')
    file4 = open("dataFile4.xml", 'wb')

    for user, counter in get_elements(context, 'user'):
        if True:
            #print user
            if counter <= 1000:
                pass
                #file1.write('%s\n' % user.text.encode('utf-8'))
                #file1.write(etree.tostring(user, encoding='utf-8'))
            elif counter <= 200000:
                pass
                #file2.write(etree.tostring(user, encoding='utf-8'))
            elif counter <= 300000:
                pass
                #file3.write(etree.tostring(user, encoding='utf-8'))
            else:
                pass
                #file4.write(etree.tostring(user, encoding='utf-8'))

    #return pt(context)


def get_elements(context, tag):
    counter = 0
    filename = "dataFile1.xml"
    for action, elem in context:
        if elem.tag == tag:
            if action == 'start':
                counter += 1
            yield elem, counter


def split_file():
    pass


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
            #while elem.getprevious() is not None:
            #    del elem.getparent()[0]

    if len(items) == 0:
        return text

    return { k: v[0] if len(v) == 1 else v for k, v in items.items() }

if __name__ == "__main__":
    #client = pymongo.Connection('localhost', 27017)
    #db = client.local
    #collection = db.test3
    #json_data = parse_xml("tweetsShort.xml")
    json_data = parse_xml("twitter-pldebatt.xml")
    #client.disconnect()
    #print(json.dumps(json_data, indent=2))
