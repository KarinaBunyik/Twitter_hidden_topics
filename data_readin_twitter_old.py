#file -- data_readin.py
import openpyxl as px
import pandas as pd
from xml.dom import minidom
from xml.dom import pulldom
from lxml import etree

# Returns a dictionary of timestamped parameter readings for each vehicle contained in the given directory.

def fast_iter(context, func):
    # http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
    # Author: Liza Daly
    for event, elem in context:
        func(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context

def process_element(elem):
    elem.xpath( 'description/text( )' )

#infile = open('twitter-pldebatt.xml')
infile = open('twitterShort.xml')
context = etree.iterparse( infile, tag='w' )
fast_iter(context,process_element)
#doc = etree.parse('bloggmix2013.xml')


#def createDataSet():    
    #xmldoc = minidom.parse('bloggmix2013.xml')
    #itemlist = xmldoc.getElementsByTagName('text') 
    #print len(itemlist)
    #print itemlist[0].attributes['direct-messages'].value
    #for s in itemlist :
    #    print s.attributes['direct-messages'].value

print "start"
print "finish"