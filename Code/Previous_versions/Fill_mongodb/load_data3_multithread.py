from collections import defaultdict
import json
import sys
import xml.etree.ElementTree as ET
import pymongo
import Queue
import threading


global collection
global queue


def load_data(user):

    collection.insert(user)

    #o = xmltodict.parse(infile)
    #print json.dumps(o) # '{"e": {"a": ["text", "text"]}}'

def parse_xml(file_name):
    events = ("start", "end")
    context = ET.iterparse(file_name, events=events)

    return pt(context)


def stuff(action, context, elem):
    items = defaultdict(list)
    if action == "start":
        if elem.tag == 'w':
            temp = queue.get()
            temp.update({"val":elem.text})
            items[elem.tag].append(temp)
        else:
                #temp_dict = t.start()
            temp_dict = pt(context, elem)
            items[elem.tag].append(temp_dict)
            #print pt(context, elem)
    if elem.tag == 'user':
        load_data(items[elem.tag])
        del items[elem.tag]

    elem.clear()    
    queue.put(items)


def pt(context, cur_elem=None):
    items = defaultdict(list)

    if cur_elem is not None:
        items.update(cur_elem.attrib)

    text = ""
    #queue = Queue.Queue()

    for action, elem in context:
        t = threading.Thread(target=stuff, args = (action, context, elem))
        t.start()
        
        items = queue.get()

        if action == "end":
            text = elem.text.strip() if elem.text else ""
            break
        #t.daemon = True
        #if action == "start":
        #    if elem.tag == 'w':
        #        thread_.start()
        #       temp = queue.get()
        #        temp.update({"val":elem.text})
        #        items[elem.tag].append(temp)
        #    else:
        #        #temp_dict = t.start()
        #        temp_dict = pt(context, elem)
        #        items[elem.tag].append(temp_dict)
        #    #print pt(context, elem)
        #elif action == "end":
        #    text = elem.text.strip() if elem.text else ""
        #    break
        #if elem.tag == 'user':
        #    load_data(items[elem.tag])
        #    del items[elem.tag]

        #elem.clear()
            #while elem.getprevious() is not None:
            #    del elem.getparent()[0]

    if len(items) == 0:
        return text

    return { k: v[0] if len(v) == 1 else v for k, v in items.items() }

if __name__ == "__main__":
    queue = Queue.Queue()
    client = pymongo.Connection('localhost', 27017)
    db = client.local
    collection = db.test2
    json_data = parse_xml("tweetsShort.xml")
    #json_data = parse_xml("twitter-pldebatt_trunc.xml")
    client.disconnect()
    #print(json.dumps(json_data, indent=2))
