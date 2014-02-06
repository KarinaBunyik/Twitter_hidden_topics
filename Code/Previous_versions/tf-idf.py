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


def fileToList(filename):
        word_list = []
        ifile = io.open(internal_path+'representative_words/'+filename+'.txt', 'r')
        for word in ifile:
            word_list.append(word.replace('\n',''))
        ifile.close()
        return word_list


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


if __name__ == "__main__":
    db = thtdb.ThtConnection(host='squib.de', dbName='karinas_twitter_db', collectionName='twitter-pldebatt-131006')
    #calculate_df(u'skola')
    terms=fileToList('jobbochskatt')
    calculatePldebattDfTerms(terms)

