from lxml import etree

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
infile = open('tweetsShort.xml')
#infile = open('twitter-pldebatt.xml')
#infilename = 'twitter-pldebatt.xml'

results = etree.parse(infile, parser)    

# When iterated over, 'results' will contain the output from 
# target parser's close() method

out = open('outWordList.txt', 'w')
#out.write('\n'.join(results))
out.write(''.join(results))
out.close()

with open('outWordList.txt') as f:
    content = f.readlines()

words = filter(lambda x: x!='', map(lambda x: x[:-1], content))
hashtags = []

for iWord in range(len(words)):
    if words[iWord] == '#':
        hashtags.append(words[iWord+1])

#print 'hashtags: ', hashtags
#print 'words: ', words

print max(hashtags, key=hashtags.count)

#from collections import Counter
#words_to_count = (word for word in word_list if word[:1].isupper())
#c = Counter(words_to_count)
#print c.most_common(3)

#for word in words:
    #print word
    #word.decode('string_escape')