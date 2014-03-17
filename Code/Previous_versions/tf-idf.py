import thtdb
import io
from thtpaths import internal_path
import math


def PrettyPrintList(listToPrint):
    for element in listToPrint:
        print element


def PrettyPrintListFloat(listToPrint):
    for element in listToPrint:
        print "{0:.3f}".format(element)


def fileToListInput(filename):
        word_list = []
        ifile = io.open(internal_path+'tfidf/representative_words/'+filename+'.txt', 'r')
        for word in ifile:
            word_list.append(word.replace('\n',''))
        ifile.close()
        return word_list


def fileToList(filename):
        word_list = []
        ifile = io.open(internal_path+filename+'.txt', 'r')
        #ifile = codecs.open(internal_path+filename+'.txt', 'rb', "utf-8")
        for word in ifile:
            word_list.append(word.replace('\n',''))
            #word_list.append((word.replace('\n','')).encode('utf8'))
        ifile.close()
        return word_list


def wordForTopics(word_dict, stemming):
    if stemming == u'lemma':
        if word_dict[u'lemma'] != '|':
            return (word_dict[u'lemma'].split('|'))[1]
        else:
            return word_dict[u'val']
    elif stemming == u'val':
        return word_dict[u'val']


def saveToFile(word_list, filename, dirname):
        file_path = internal_path+dirname+'/'
        #user_words_filename = internal_path+'/malletTwitterOctober/'+username
        ofile = io.open(file_path+filename+'.txt', 'wb')
        for word in word_list:
            if word is not None:
                ofile.write(word.encode('utf8')+' ')
        ofile.close()


def updateFile(word_list, filename, dirname):
        file_path = internal_path+dirname+'/'
        #word_list.insert(0,'\n')
        #user_words_filename = internal_path+'/malletTwitterOctober/'+username
        ofile = io.open(file_path+filename+'.txt', 'ab')
        for word in word_list:
            if word is not None:
                ofile.write(word.encode('utf8')+' ')
        ofile.close()


def createTopicDocuments(tag):
    no_go_list = fileToList('english_stoplist')+fileToList('swedish_stoplist')
    tweet_words = []
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                if 'tweettags' in text:
                    if tag in text['tweettags']:
                        if u'mentions' in text:
                            mentions_list = text[u'mentions'].split('|')
                        else:
                            mentions_list = [] 
                        if u'sentence' in text:
                            for sentence in text[u'sentence']:
                                if u'w' in sentence:
                                    for word in sentence[u'w']:
                                        if u'val' in word:
                                            if word[u'val'] not in mentions_list and word[u'val'] not in no_go_list:
                                                tweet_words.append(wordForTopics(word,u'lemma'))
                        updateFile(tweet_words, tag, 'tfidf')
                        tweet_words = []



#The following function calculates the document(tweet) frequency of a given term(word). It basicaly gives the number of times the term occures +/- epsilon. 
    #(in case one tweet has a term two times, only one will be calculated)
def calculateDfOneTerm(term):
    total_term_frequency = []
    doc_number = 0
    #interesting_user_ids = []
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                term_frequency = 0
                if u'sentence' in text:
                    for sentence in text[u'sentence']:
                        if u'w' in sentence:
                            for word in sentence[u'w']:
                                if u'lemma' in word and u'val' in word:
                                    if word[u'val'] is not None:
                                        if word[u'val'].lower() == term:
                                            term_frequency += 1
                                        elif word[u'lemma'] != '|':
                                            if word[u'lemma'].lower() == term:
                                                term_frequency += 1
                                    else:
                                        pass
                                        #print "None"
                total_term_frequency.append(term_frequency)
                doc_number += 1
    print "Total number of tweets: ", doc_number
    containing_doc_number = sum([1 for x in total_term_frequency if x > 0])
    is_more = sum([1 for x in total_term_frequency if x > 1])
    print "Number of times the term appears: ", sum(total_term_frequency)
    print "Number of docs the term appears in: ", containing_doc_number
    print "idf: ", math.log(doc_number/(containing_doc_number + 1),10)
    print "Number of tweets having the term frequency calculated: ", len(total_term_frequency)
    print "This many tweets have the term more than once: ", is_more


#The following function calculates the document(tweet) frequency of a list of terms(words). It basicaly gives the number of times each term occures +/- epsilon. 
    #(in case one tweet has a term two times, only one will be calculated)
def calculateDfTerms(terms):
    total_term_frequency = []
    doc_number = 0
    #interesting_user_ids = []
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                term_frequency = [0 for i in range(len(terms))]
                if u'sentence' in text:
                    for sentence in text[u'sentence']:
                        if u'w' in sentence:
                            for word in sentence[u'w']:
                                if u'lemma' in word and u'val' in word:
                                    for index in range(len(terms)):
                                        if word[u'val'] is not None:
                                            if word[u'val'].lower() == terms[index]:
                                                term_frequency[index] += 1
                                            elif word[u'lemma'] != '|':
                                                if word[u'lemma'].lower() == terms[index]:
                                                    term_frequency[index] += 1
                total_term_frequency.append(term_frequency)
                doc_number += 1
    print "Total number of tweets: ", doc_number
    total_term_frequency =  map(list, zip(*total_term_frequency))
    containing_doc_number = [sum([1 for x in y if x > 0]) for y in total_term_frequency]
    is_more = [sum([1 for x in y if x > 1]) for y in total_term_frequency]
    print "Number of times the terms appear: "
    PrettyPrintList([sum(x) for x in total_term_frequency])
    print "Number of docs the term appears in: "
    PrettyPrintList(containing_doc_number)
    print "idf: "
    PrettyPrintListFloat([math.log(doc_number/(x+1),10) for x in containing_doc_number])
    print "Number of tweets having the term frequency calculated: ", [len(x) for x in total_term_frequency]
    print "This many tweets have the term more than once: ", is_more



#The following function calculates the #pldebatt document(tweet containing #pldebatt) frequency of a list of terms(words). It basicaly gives the number of times each term occures +/- epsilon. 
    #(in case one tweet has a term two times, only one will be calculated)
def calculatePldebattDfTerms(terms):
    total_term_frequency = []
    doc_number = 0
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                if u'hashtags' in text:
                    if u'#pldebatt' in text[u'hashtags']:
                        term_frequency = [0 for i in range(len(terms))] 
                        if u'sentence' in text:
                            for sentence in text[u'sentence']:
                                if u'w' in sentence:
                                    for word in sentence[u'w']:
                                        if u'lemma' in word and u'val' in word:
                                            for index in range(len(terms)):
                                                if word[u'val'] is not None:
                                                    if word[u'val'].lower() == terms[index]:
                                                        term_frequency[index] += 1
                                                    elif word[u'lemma'] != '|':
                                                        lemmas_temp = word['lemma'].split('|')
                                                        lemmas = lemmas_temp[1:len(lemmas_temp)-1]
                                                        if terms[index] in lemmas:
                                                            term_frequency[index] += 1
                        total_term_frequency.append(term_frequency)
                        doc_number += 1
    print "Total number of tweets: ", doc_number
    total_term_frequency =  map(list, zip(*total_term_frequency))
    containing_doc_number = [sum([1 for x in y if x > 0]) for y in total_term_frequency]
    is_more = [sum([1 for x in y if x > 1]) for y in total_term_frequency]
    print "Number of times the terms appear: "
    PrettyPrintList([sum(x) for x in total_term_frequency])
    print "Number of docs the term appears in: "
    PrettyPrintList(containing_doc_number)
    print "idf: "
    PrettyPrintListFloat([math.log(doc_number/(x+1),10) for x in containing_doc_number])
    print "Number of tweets having the term frequency calculated: ", [len(x) for x in total_term_frequency]
    print "This many tweets have the term more than once: ", is_more

'''
# save tweets related to terms in files
def saveTermTweetsToFile(terms, hashtag):
    #total_term_frequency = []
    #doc_number = 0
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                tweet_text = []
                if u'hashtags' in text:
                    if hashtag in text[u'hashtags']:
                        #term_frequency = [0 for i in range(len(terms))] 
                        if u'sentence' in text:
                            for sentence in text[u'sentence']:
                                if u'w' in sentence:
                                    for word in sentence[u'w']:
                                        if u'lemma' in word:
                                            if word['lemma'] != '|':
                                                pass
                                        else:
                                            tweet_text.append()





                                                tweet_text.append()

                                        and u'val' in word:
                                            for index in range(len(terms)):
                                                if word[u'val'] is not None:
                                                    if word[u'val'].lower() == terms[index]:
                                                        term_frequency[index] += 1
                                                    elif word[u'lemma'] != '|':
                                                        if word[u'lemma'].lower() == terms[index]:
                                                            term_frequency[index] += 1
                        total_term_frequency.append(term_frequency)
                        doc_number += 1
    print "Total number of tweets: ", doc_number
    total_term_frequency =  map(list, zip(*total_term_frequency))
    containing_doc_number = [sum([1 for x in y if x > 0]) for y in total_term_frequency]
    is_more = [sum([1 for x in y if x > 1]) for y in total_term_frequency]
    print "Number of times the terms appear: "
    PrettyPrintList([sum(x) for x in total_term_frequency])
    print "Number of docs the term appears in: "
    PrettyPrintList(containing_doc_number)
    print "idf: "
    PrettyPrintListFloat([math.log(doc_number/(x+1),10) for x in containing_doc_number])
    print "Number of tweets having the term frequency calculated: ", [len(x) for x in total_term_frequency]
    print "This many tweets have the term more than once: ", is_more
'''



if __name__ == "__main__":
    db = thtdb.ThtConnection(host='squib.de', dbName='karinas_twitter_db', collectionName='twitter-pldebatt-131006')
    '''
    print 'saving crime tweets...'
    #createTopicDocuments('crime')
    print 'crime tweets done.'
    print 'saving school tweets...'
    #createTopicDocuments('school')
    print 'school tweets done.'
    print 'saving climate tweets...'
    #createTopicDocuments('climate')
    print 'climate tweets done.'
    print 'saving tax tweets...'
    createTopicDocuments('tax')
    print 'tax tweets done.'
    print 'saving immigration tweets...'
    createTopicDocuments('immigration')
    print 'immigration tweets done.'
    print 'saving health tweets...'
    createTopicDocuments('health')
    print 'health tweets done.'
    
    '''
    #calculatePldebattDfTerms(fileToListInput('brottochstraff'))
    #calculatePldebattDfTerms(fileToListInput('flyktingar'))
    #calculatePldebattDfTerms(fileToListInput('skolan'))
    calculatePldebattDfTerms(fileToListInput('jobbochskatt'))
    #calculatePldebattDfTerms(fileToListInput('klimat'))
    #calculatePldebattDfTerms(fileToListInput('sjukvard'))
    #calculateDfTerms(fileToListInput('brottochstraff'))
    #calculateDfTerms(fileToListInput('flyktingar'))
    #calculateDfTerms(fileToListInput('skolan'))
    calculateDfTerms(fileToListInput('jobbochskatt'))
    #calculateDfTerms(fileToListInput('klimat'))
    #calculateDfTerms(fileToListInput('sjukvard'))
