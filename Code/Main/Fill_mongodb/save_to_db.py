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
import thtdb
from thtpaths import data_path, script_path, internal_data_path
import time


def parse_xml_multithread(file_name):
    print "parsing..."
    events = ("start", "end")
    context = etree.iterparse(file_name, events=events, remove_blank_text=True)
    context = iter(context)
    event, root = context.next()
    
    counter =0
    file1_name = "TempDataFile1.xml"
    file2_name = "TempDataFile2.xml"
    file3_name = "TempDataFile3.xml"
    file4_name = "TempDataFile4.xml"
    file1 = open(data_path + file1_name, 'wb')
    file2 = open(data_path + file2_name, 'wb')
    file3 = open(data_path + file3_name, 'wb')
    file4 = open(data_path + file4_name, 'wb')
    xmlroot_open_name = 'root_opening.txt'
    xmlroot_close_name = 'root_closing.txt'
    xmlroot_open_path = internal_data_path+xmlroot_open_name
    xmlroot_close_path = internal_data_path+xmlroot_close_name

    print "splitting file..."
    print "readin file1..."
    add_root_script_path = script_path+'insert_root_file.sh'
    for action, elem in context:
        if action == "start":
            if elem.tag == 'user':
                counter += 1
                elem.tail = None  
                if counter <= 5000:
                #file1.write('%s\n' % user.text.encode('utf-8'))
                    file1.write(etree.tostring(elem, encoding='utf-8'))
                elif counter <= 10000:
                    if counter == 5001:
                        print "loading file1..."
                        file1.close()
                        command_string = add_root_script_path+' '+data_path+file1_name+' '+xmlroot_open_path+' '+xmlroot_close_path
                        proc = subprocess.Popen([command_string], shell=True, stdout=subprocess.PIPE)
                        proc.wait()
                        file1 = open(data_path + file1_name, 'r')
                        context1 = etree.iterparse(file1, events=events)
                        t1 = threading.Thread(target=pt, args = (context1,))
                        t1.start()
                        print "readin file2..."
                    file2.write(etree.tostring(elem, encoding='utf-8'))
                elif counter <= 15000:
                    if counter == 10001:
                        print "loading file2..."
                        file2.close()
                        command_string = add_root_script_path+' '+data_path+file2_name+' '+xmlroot_open_path+' '+xmlroot_close_path
                        proc = subprocess.Popen([command_string], shell=True, stdout=subprocess.PIPE)
                        proc.wait()
                        file2 = open(data_path + file2_name, 'r')
                        context2 = etree.iterparse(file2, events=events)
                        t2 = threading.Thread(target=pt, args = (context2,))
                        t2.start()
                        print "readin file3..."
                    file3.write(etree.tostring(elem, encoding='utf-8'))
                else:
                    if counter == 15001:
                        print "loading file3..."
                        file3.close()
                        command_string = add_root_script_path+' '+data_path+file3_name+' '+xmlroot_open_path+' '+xmlroot_close_path
                        proc = subprocess.Popen([command_string], shell=True, stdout=subprocess.PIPE)
                        proc.wait()
                        file3 = open(data_path + file3_name, 'r')
                        context3 = etree.iterparse(file3, events=events)
                        t3 = threading.Thread(target=pt, args = (context3,))
                        t3.start()
                        print "readin file4..."
                    file4.write(etree.tostring(elem, encoding='utf-8'))
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context
    print "loading file4..."
    file4.close()
    command_string = add_root_script_path+' '+data_path+file4_name+' '+xmlroot_open_path+' '+xmlroot_close_path
    proc = subprocess.Popen([command_string], shell=True, stdout=subprocess.PIPE)
    proc.wait()
    file4 = open(data_path + file4_name, 'r')
    context4 = etree.iterparse(file4, events=events)
    t4 = threading.Thread(target=pt, args = (context4,))
    t4.start()
    t1.join()
    del context1
    file1.close()
    os.remove(data_path+file1_name)
    t2.join()
    del context2
    file2.close()
    os.remove(data_path+file2_name)
    t3.join()
    del context3
    file3.close()
    os.remove(data_path+file3_name)
    t4.join()
    del context4
    file4.close()
    os.remove(data_path+file4_name)


def parse_xml(file_name):
    events = ("start", "end")
    print "parsing..."
    context = etree.iterparse(file_name, events=events, remove_blank_text=True)
    return pt(context)


def pt(context, cur_elem=None):
    items = defaultdict(list)
    if cur_elem is not None:
        items.update(cur_elem.attrib)
    text = ""
    for action, elem in context:
        if action == "start":
            if elem.tag == 'w':
                temp = pt(context, elem)
                temp.update({"val":elem.text})
                items[elem.tag].append(temp)
            else:
                temp_dict = pt(context, elem)
                items[elem.tag].append(temp_dict)
        elif action == "end":
            text = elem.text.strip() if elem.text else ""
            break
        if elem.tag == 'user':
            save_to_db(items[elem.tag])
            del items[elem.tag]
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context
    if len(items) == 0:
        return text
    return { k: v[0] if len(v) == 1 else v for k, v in items.items() }


def save_to_db(user):
    user[0]["_id"] = user[0]["id"]
    for i in range(5):
        try:
            db.collection.save(user[0])
            break
        except pymongo.errors.AutoReconnect:
            time.sleep(pow(2, i))


if __name__ == "__main__":
    db = thtdb.ThtConnection(collectionName='test_mongod_quiet')
    #db = thtdb.ThtConnection(host='squib.de', dbName='karinas_twitter_db', collectionName='pldebatt_june')

    parse_xml("/Users/karinabunyik/BTSync/Data/twitter-pldebatt.xml")
    db.client.disconnect()
