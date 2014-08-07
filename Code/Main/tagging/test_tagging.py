# -*- coding: utf-8 -*-#
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
            word_list.append(word.encode("utf-8").replace('\n',''))
        ifile.close()
        return word_list


def all_pairs(L):
    answer = []
    for i in range(len(L)):
        for j in range(i+1, len(L)):
            if (L[i],L[j]) not in answer:
                answer.append((L[i],L[j]))
    return answer


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

def countTopicWordOccurence(topic_fime_name):
    print "Count occurence of topic words"
    topic_occurences = {}
    topic_list = fileToListInput(topic_fime_name)
    print topic_list
    for user in db.collection.find({'text.tweettags': {'$exists': True}}):
        if u'text' in user:
            for text in user[u'text']:
                if u'sentence' in text:
                    for sentence in text[u'sentence']:
                        if u'w' in sentence:
                            for word in sentence[u'w']:
                                if u'val' in word:
                                    if (word['val'].lower().encode('utf-8') in topic_list):
                                        #print word['val'].lower().encode('utf-8')
                                        if word['val'].lower().encode('utf-8') not in topic_occurences:
                                            topic_occurences[word['val'].lower().encode('utf-8')]= 1
                                        else:
                                             topic_occurences[word['val'].lower().encode('utf-8')] += 1
                                    else:
                                        if 'lemma' in word:
                                            lemmas_temp = word['lemma'].split('|')
                                            lemmas = lemmas_temp[1:len(lemmas_temp)-1]
                                            if len(lemmas) > 0:
                                                if lemmas[0].encode('utf-8') in topic_list:
                                                    #print "lemma: ", lemmas[0].encode('utf-8')
                                                    if lemmas[0].encode('utf-8') not in topic_occurences:
                                                        topic_occurences[lemmas[0].encode('utf-8')] = 1
                                                    else:
                                                        topic_occurences[lemmas[0].encode('utf-8')] += 1
                                                #else:
                                                    #print word['val'].lower().encode('utf-8')
    for key in topic_occurences:
        print key, topic_occurences[key]

#The following function calculates the document(tweet) frequency of a given term(word). It basicaly gives the number of times the term occures +/- epsilon. 
    #(in case one tweet has a term two times, only one will be calculated)
def countTweetTags(tags):
    print 'Counting tags...'
    count_tags = {}
    for user in db.collection.find({'text.tweettags': {'$exists': True}}):
        if u'text' in user:
            for text in user[u'text']:
                if u'tweettags' in text:
                    for tag in tags:
                        if tag in text[u'tweettags']:
                            if tag not in count_tags:
                                count_tags[tag] = 1
                            else:
                                count_tags[tag] += 1
        else:
            print "Error, user has no tweets: ", user[u'_id']
    print 'Tagged tweet occurences: ', count_tags


def countTweetTagsWithOverlap(tags, overlap_tag):
    print 'Counting tags...'
    count_tags = {}
    for user in db.collection.find({'text.tweettags': {'$exists': True}}):
        if u'text' in user:
            for text in user[u'text']:
                if u'tweettags' in text:
                    for tag in tags:
                        if tag in text[u'tweettags'] and overlap_tag in text[u'tweettags']:
                            if tag not in count_tags:
                                count_tags[tag] = 1
                            else:
                                count_tags[tag] += 1
        else:
            print "Error, user has no tweets: ", user[u'_id']
    print 'Tagged tweet occurences: ', count_tags


def countTweetTagPairs(topic_tag_list, tag_topics, tag_pairs):
    print 'Counting tag pairs...'
    #count_tags = {}
    many_tag_count = 0
    for user in db.collection.find({'text.tweettags': {'$exists': True}}):
        if u'text' in user:
            for text in user[u'text']:
                if u'tweettags' in text:
                    tag_intersection = list(set(text[u'tweettags']) & set(topic_tag_list))

                    if len(tag_intersection) > 2 :
                        for pair_t in all_pairs(tag_intersection):
                            for pair in tag_pairs:
                                if set(pair['tags']) & set(pair_t):
                                    pair['count'] += 1

                    elif len(tag_intersection) == 2:
                        for pair in tag_pairs:
                            if set(pair['tags']) & set(tag_intersection):
                                pair['count'] += 1

                    elif len(tag_intersection) == 1:
                        tag_topics[tag_intersection[0]] += 1 
        else:
            print "Error, user has no tweets: ", user[u'_id']
    print 'Number of tweets having multiple tags: ', many_tag_count
    print tag_pairs
    print tag_topics


def countTweet_other(tags):
    count_tags = {}
    count_tweets = 0
    count_coordinates = 0
    count_pldebatt = 0
    count_agenda = 0
    count_debatt = 0
    count_debatten = 0
    count_svpol = 0
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                count_tweets += 1
                #if u'coordinates' in text:
                #    if u'hashtags' in text:
                #        if '#pldebatt' in text[u'hashtags'].split('|'):
                #            count_coordinates += 1
                if u'hashtags' in text:
                    if '#pldebatt' in text[u'hashtags'].split('|'):
                       count_pldebatt += 1
                    if '#agenda' in text[u'hashtags'].split('|'):
                        count_agenda += 1
                    if '#debatt' in text[u'hashtags'].split('|'):
                        count_debatt += 1
                    if '#debatten' in text[u'hashtags'].split('|'):
                        count_debatten += 1
                    if '#svpol' in text[u'hashtags'].split('|'):
                        count_svpol += 1
                if u'tweettags' in text:
                    for tag in tags:
                        if tag in text[u'tweettags']:
                            if tag not in count_tags:
                                count_tags[tag] = 1
                            else:
                                count_tags[tag] += 1
        else:
            print user[u'_id']
    print 'Tagged tweet occurences: ', count_tags
    #print "Number of ", tag, " occurences in tweets: ", count_tag
    print '#pldebatt tweet occurences: ', count_pldebatt
    print "#svpol tweet occurences: ", count_svpol
    print 'agenda tweet occurences: ', count_agenda
    print 'debatt tweet occurences: ', count_debatt
    print 'debatten tweet occurences: ', count_debatten
    #print "Number of tweets with coordinaetes: ", count_coordinates
    print "Total number of tweets: ", count_tweets


def countUserTags(tag):
    count_tag = 0
    count_users = 0
    for user in db.collection.find():
        count_users += 1
        if u'usertags' in user:
            if tag in user[u'usertags']:
                count_tag += 1
    print "Number of ", tag, " occurences in users: ", count_tag
    print "Number of users: ", count_users

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
    db = thtdb.ThtConnection(dbName='tweets_by_users_october_2', collectionName='twitter-pldebatt-131006')
    #db = thtdb.ThtConnection(dbName='tweets_by_users', collectionName='twitter-pldebatt-140504')
    #db = thtdb.ThtConnection(dbName='tweets_by_users', collectionName='twitter-pldebatt-130612')
    #db = thtdb.ThtConnection(dbName='tweets_by_users', collectionName='twitter-pldebatt-medium')
    #db = thtdb.ThtConnection(host='squib.de', dbName='karinas_twitter_db', collectionName='pldebatt_june')
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
    tags = ['school', 'crime', 'climate', 'tax', 'health', 
            'immigration', 'antiracism', 'feminism', 'antirasism', 'eu',
            'defense', 'openborders', 'welfaregains', 'pldebatt_context_linn', 'predicted_linn']

    one_tag_may_extra = {'feminism': 0,
                    'antiracism': 0,
                    'eu': 0,
                    'welfaregains': 0}

    one_tag_october = {'school': 0,
                    'tax': 0,
                    'crime': 0,
                    'climate': 0,
                    'health': 0,
                    'immigration': 0}

    two_tag_october = [{'tags':['school', 'crime'], 'count': 0},
                    {'tags':['school', 'climate'], 'count': 0},
                    {'tags':['school', 'health'], 'count': 0},
                    {'tags':['school', 'tax'], 'count': 0},
                    {'tags':['school', 'immigration'], 'count': 0},
                    {'tags':['crime', 'climate'], 'count': 0},
                    {'tags':['tax', 'climate'], 'count': 0},
                    {'tags':['immigration', 'climate'], 'count': 0},
                    {'tags':['health', 'climate'], 'count': 0},
                    {'tags':['crime', 'immigration'], 'count': 0},
                    {'tags':['crime', 'health'], 'count': 0},
                    {'tags':['crime', 'tax'], 'count': 0},
                    {'tags':['tax', 'immigration'], 'count': 0},
                    {'tags':['health', 'immigration'], 'count': 0},
                    {'tags':['health', 'tax'], 'count': 0}
                    ]
    two_tag_may_extra  = [{'tags':['feminism', 'antiracism'], 'count': 0},
                    {'tags':['feminism', 'eu'], 'count': 0},
                    {'tags':['feminism', 'welfaregains'], 'count': 0},
                    {'tags':['antiracism', 'eu'], 'count': 0},
                    {'tags':['antiracism', 'welfaregains'], 'count': 0},
                    {'tags':['eu', 'welfaregains'], 'count': 0}
                    ]
    topic_tags_may_extra = ['feminism', 'eu', 'welfaregains', 'antiracism']
    topic_tags_october = ['crime', 'climate', 'school', 'immigration', 'tax', 'health']


    list_tax = [
    'heltidsjobb',
    'instegsjobb',
    'svartjobb',
    'jobbprognos',
    'jobbskapande',
    'anställning',
    'arbeta',
    'deltidsarbete',
    'skatt',
    'avdrag',
    'beskatta',
    'förmögenhetsskatt',
    'inkomstskatt',
    'kommunalskatt',
    'konsumtionsskatt',
    'punktskatt',
    'skattebas',
    'skattemedel',
    'arbetslöshet',
    'massarbetslöshet',
    'småföretagare',
    'finanskris',
    'bidrag',
    'subvention',
    'bidragsberoende',
    'bidragsgrundande',
    'bidragssystem',
    'förtidspension',
    'förtidspensionera',
    'ungdomsavgifter',
    'näringspolitik',
    'näringspolitisk',
    'utgifter',
    'budget',
    'skuggbudget',
    'budgetförslag',
    'budgetmotion',
    'budgetunderskott',
    'budgetöverskott',
    'fas3',
    'inkomstskattesänkning',
    'lågkonjunktur',
    'löneavdrag',
    'skatteavdrag',
    'beskattning',
    'chockbeskatta',
    'åtgärdspolitik',
    'chockskatt',
    'skattehöjning',
    'närningsliv',
    'skatteintäkt',
    'utförsäkra',
    'pension',
    'skattechock',
    'skattesubvention',
    'finansminister',
    'entreprenörskap',
    'reformutrymme',
    'jobbfrågan',
    'arbetsgivare',
    'skattepeng',
    'låginkomsttagare',
    'tillväxt',
    'sysselsättning',
    'krogmoms',
    'arbetsförmedling',
    'sjukförsäkring',
    'ams',
    'bidragsutbyggnad',
    'försörjningsstöd',
    'förtidspensionering',
    'arbetskraftsandel',
    'utanförskap',
    'investeringar',
    'kassako',
    'ams-politik',
    'konjunktur',
    'lärlingssystem',
    'arbetsmarknadspolitisk',
    'inträdesjobb',
    'ungdomsrabatt',
    'småföretag',
    'överskott',
    'arbetslöshetsförsäkring',
    'arbetskraft',
    'arbetstillfällen',
    'skattepolitik',
    'skattesänkning',
    'kalkyl',
    'konkurrenskraft',
    'arbetslöshetstid',
    'arbetslösheten',
    'arbetslösa',
    'arbetsmarknaden',
    'skatten',
    'a-kassan',
    'arbete',
    'skattesänkningar',
    'jobbpolitik',
    'skatter',
    'arbetsmarknad',
    'rot',
    'arbetstagare',
    'ekonomi',
    'arbetslöshetsförsäkringen',
    'sjukförsäkringen',
    'skatterna',
    'statsskuld',
    'a-kassa',
    'jobbskatteavdraget',
    'bidragspolitik',
    'bidragslinjen',
    'restaurangmomsen',
    'akassan',
    'inkomstklyftor',
    'skattesatsen',
    'inkomstskatter',
    'långtidsarbetslösa',
    'skatteintäkterna',
    'finanserna',
    'skattesänkningarna',
    'skattesänkningsplaner',
    'arbetsgivaravgift',
    'jobbavdrag',
    '90-dagars-garantier',
    'sysselsättningsgraden',
    'momshöjning',
    'akassa',
    'arbetslinjen',
    'ungdomsarbetslösheten',
    'ungdomsarbetslöshet',
    '90-dagarsgaranti',
    'jobbtillväxten',
    'jobb',
    'jobben',
    'finanser',
    'sysselsättningsgrad',
    'företagare',
    'småföretagarna',
    'sysselsättningen',
    '90-dagarsgarantin',
    'finanskrisen',
    'anställningar',
    'finansiella',
    'jobbskatteavdrag',
    'jobbskapare',
    'sysselsatta',
    'restaurangmoms',
    'arbetslös',
    'visstidsanställningar',
    'krogmomsen',
    'skattehöjningar',
    'jobbskaparna',
    'löntagare',
    'jobbdebatten',
    'skatteintäkter',
    'överskottsmålet',
    'företag',
    'skattehöjningarna',
    'arbetsförmedlingen',
    'arbetskraften',
    'långtidsarbetslöshet',
    'massarbetslösheten',
    'löntagarorganisationernas']

    countTopicWordOccurence('jobbochskatt')

    #countTweetTags(tags)

    #countTweetTagPairs(topic_tags, one_tag_may_extra, two_tag_may_extra)
    #countTweetTagPairs(topic_tags_october, one_tag_october, two_tag_october)
    #calculatePldebattDfTerms(fileToListInput('brottochstraff'))
    #calculatePldebattDfTerms(fileToListInput('flyktingar'))
    #calculatePldebattDfTerms(fileToListInput('skolan'))
    #calculatePldebattDfTerms(fileToListInput('jobbochskatt'))
    #calculatePldebattDfTerms(fileToListInput('klimat'))
    #calculatePldebattDfTerms(fileToListInput('sjukvard'))
    #calculateDfTerms(fileToListInput('brottochstraff'))
    #calculateDfTerms(fileToListInput('flyktingar'))
    #calculateDfTerms(fileToListInput('skolan'))
    #calculateDfTerms(fileToListInput('jobbochskatt'))
    #calculateDfTerms(fileToListInput('klimat'))
    #calculateDfTerms(fileToListInput('sjukvard'))
