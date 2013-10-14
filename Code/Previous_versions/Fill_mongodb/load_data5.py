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
import os


global collection
global queue


def load_data(user):

    user[0]["_id"] = user[0]["id"]
    collection.save(user[0])
    #collection.insert(user)

    #o = xmltodict.parse(infile)
    #print json.dumps(o) # '{"e": {"a": ["text", "text"]}}'

def parse_xml(file_name):
    events = ("start", "end")
    print "parsing..."
    context = etree.iterparse(file_name, events=events, remove_blank_text=True)
    context = iter(context)
    event, root = context.next()
    
    counter =0

    file1 = open("dataFile1.xml", 'wb')
    file2 = open("dataFile2.xml", 'wb')
    file3 = open("dataFile3.xml", 'wb')
    file4 = open("dataFile4.xml", 'wb')

    print "splitting file..."
    print "readin file1..."
    for action, elem in context:
        if action == "start":
            if elem.tag == 'user': # i want to write out all <bucket> entries
                counter += 1
                elem.tail = None  
                if counter <= 100000:
                    pass
                #file1.write('%s\n' % user.text.encode('utf-8'))
                    file1.write(etree.tostring(elem, encoding='utf-8'))
                    #print ET.tostring(elem, encoding='utf-8')
                elif counter <= 200000:
                    if counter == 100001:
                        print "loading file1..."
                        file1.close()
                        proc = subprocess.Popen(['/Users/karinabunyik/Twitter_hidden_topics/insert_root_file1.sh'], shell=True, stdout=subprocess.PIPE)
                        proc.wait()
                        file1 = open("dataFile1.xml", 'r')
                        context1 = etree.iterparse(file1, events=events)
                        t1 = threading.Thread(target=pt, args = (context1,))
                        t1.start()
                        del context1
                        print "readin file2..."
                    file2.write(etree.tostring(elem, encoding='utf-8'))
                elif counter <= 300000:
                    if counter == 200001:
                        print "loading file2..."
                        file2.close()
                        proc = subprocess.Popen(['/Users/karinabunyik/Twitter_hidden_topics/insert_root_file2.sh'], shell=True, stdout=subprocess.PIPE)
                        proc.wait()
                        file2 = open("dataFile2.xml", 'r')
                        context2 = etree.iterparse(file2, events=events)
                        t2 = threading.Thread(target=pt, args = (context2,))
                        t2.start()
                        #pt(context2)
                        del context2
                        print "readin file3..."
                    file3.write(etree.tostring(elem, encoding='utf-8'))
                else: # counter <= 400000:
                    if counter == 300001:
                        print "loading file3..."
                        file3.close()
                        proc = subprocess.Popen(['/Users/karinabunyik/Twitter_hidden_topics/insert_root_file3.sh'], shell=True, stdout=subprocess.PIPE)
                        proc.wait()
                        file3 = open("dataFile3.xml", 'r')
                        context3 = etree.iterparse(file3, events=events)
                        t3 = threading.Thread(target=pt, args = (context3,))
                        t3.start()
                        #pt(context3)
                        del context3
                        print "readin file4..."
                    file4.write(etree.tostring(elem, encoding='utf-8'))
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
               #file1.write(ET.tostring(elem, encoding='utf-8'))
            #if elem.tag == 'resFrame':
            #    if elem.find("id").text == ":4:39644:482:-1:1": # i only want to write out resFrame entries with this id
            #        elem.tail = None
            #        print ET.tostring( elem )
            #if elem.tag in ['bucket', 'frame', 'resFrame']:
        #root.clear()  # when done parsing a section clear the tree to safe memory
    del context
    #print counter
    print "loading file4..."
    file4.close()
    proc = subprocess.Popen(['/Users/karinabunyik/Twitter_hidden_topics/insert_root_file4.sh'], shell=True, stdout=subprocess.PIPE)
    proc.wait()
    file4 = open("dataFile4.xml", 'r')
    context4 = etree.iterparse(file4, events=events)
    t4 = threading.Thread(target=pt, args = (context4,))
    t4.start()
    #pt(context4)
    del context4
    t1.join()
    file1.close()
    t2.join()
    file2.close()
    t3.join()
    file3.close()
    t4.join()
    file4.close()
    #os.remove('/Users/karinabunyik/Twitter_hidden_topics/dataFile1.xml')
    #os.remove('/Users/karinabunyik/Twitter_hidden_topics/dataFile2.xml')
    #os.remove('/Users/karinabunyik/Twitter_hidden_topics/dataFile3.xml')
    #os.remove('/Users/karinabunyik/Twitter_hidden_topics/dataFile4.xml')
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
    collection = db.test_2
    #json_data = parse_xml("tweetsShort.xml")
    json_data = parse_xml("/Users/karinabunyik/Documents/data/twitter-pldebatt.xml")
    #client.disconnect()
    #print(json.dumps(json_data, indent=2))
