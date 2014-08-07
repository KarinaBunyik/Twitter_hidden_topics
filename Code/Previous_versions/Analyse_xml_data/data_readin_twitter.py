from lxml import etree
from collections import Counter

class TitleTarget(object):
    def __init__(self):
        self.text = []
    def start(self, tag, attrib):
        self.is_title = True if tag == 'w' else False
        #self.is_title = True if attrib == 'hashtags' else False
    def end(self, tag):
        pass
    def data(self, data):
        if self.is_title:
            self.text.append(data.encode('utf-8'))
    def close(self):
        return self.text

parser = etree.XMLParser(target = TitleTarget()) #, recover=True)

# This and most other samples read in the Google copyright data
#infile = open('tweetsShort.xml')
infile = open('twitter-pldebatt.xml')
#infilename = 'twitter-pldebatt.xml'

results = (''.join(etree.parse(infile, parser))).split('\n')
#print results
#results = etree.parse(infile, parser)

# When iterated over, 'results' will contain the output from 
# target parser's close() method

#out = open('outWordList.txt', 'w')
#out.write(''.join(results))
#out.close()

#words = filter(lambda x: x!='', map(lambda x: x[:-1], results))
#words = results
#print "words after map filter ", words

#with open('outWordList.txt') as f:
#    content = f.readlines()

#words = filter(lambda x: x!='', map(lambda x: x[:-1], content))
hashtags = []

for iWord in range(len(results)):
    if results[iWord] == '#':
        hashtags.append(results[iWord+1])


words_to_count = (word for word in hashtags if word[:1].isupper())
c = Counter(words_to_count)


#print 'hashtags: ', hashtags
#print 'words: ', words

#print max(hashtags, key=hashtags.count)

#from collections import Counter
#words_to_count = (word for word in word_list if word[:1].isupper())
#c = Counter(words_to_count)
#print c.most_common(2)

print "most common: ", max(hashtags, key=hashtags.count)
for a in c.most_common(40):
    print a[0], a[1]

#for word in words:
    #print word
    #word.decode('string_escape')
