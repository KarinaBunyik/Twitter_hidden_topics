# -*- coding: UTF-8 -*-   
#from bson.son import SON
import thtdb
import io
from thtpaths import internal_path
import random
import re

def saveToDir(word_list, filename, dirname):
        dirname = dirname+'/'
        ofile = io.open(dirname+filename, 'wb')
        for word in word_list:
            if word is not None:
                ofile.write(word.encode('utf8')+' ')
        ofile.close()

def fileToList(filename):
        word_list = []
        ifile = io.open(internal_path+filename+'.txt', 'r')
        for word in ifile:
            word_list.append(word.replace('\n',''))
        ifile.close()
        return word_list

def isLemmaInList(sentences, wList):
    for sentence in sentences:
        if 'w' in sentence:
            for word in sentence['w']:
                if 'lemma' in word:
                    lemmas_temp = word['lemma'].split('|')
                    lemmas = lemmas_temp[1:len(lemmas_temp)-1]
                if bool(set(wList) & set(lemmas)):
                        return True
    return False


# Takes a twitter dataset from Sprakbanken. Creates one document for each tweet. Documents with hashtags end up in
#training example. #pldebatt hastag is positive example, other hashtags are negative examples. No hashtag tweets are
#to be predicted. The hashtags are taken away from the tweets. The positive hashtags end up in a separate folder
# called "pldebatt", the negative in "other" folder. "raw" folder contains all labeled samples without train-test split.
def saveWordsPerTweetByHashtag(folder, minimal_tweet_length, with_spec_char):
    all_folder = internal_path+'hashtagPrediction/'+folder+'/raw'
    test_folder = internal_path+'hashtagPrediction/'+folder+'/test'
    train_folder = internal_path+'hashtagPrediction/'+folder+'/train'
    predict_folder = internal_path+'hashtagPrediction/'+folder+'/predict/unknown'
    element_counter = 0
    pldebatt_folder = '/pldebatt'
    nonpldebatt_folder = '/other'

    political_context = fileToList('domain_word_list')
    #p = re.compile("[A-Za-z\såäöÅÄÖ]+$", re.UNICODE)
    #p = re.compile("[^a-zA-Z0-9]+$")
    p = re.compile("[A-Za-z0-9\såäöÅÖÄ:-]+$", re.UNICODE)

    for user in db.collection.find():
        element_counter += 1
        if element_counter % 1000 == 0:
            print element_counter
        if u'text' in user:
            for text in user[u'text']:
                is_word_pldebatt = False
                is_word_politics = False
                if u'sentence' in text:
                    tweet_id = text[u'id']
                    tweet_words = []
                    for sentence in text[u'sentence']:
                        if u'w' in sentence:
                            for word in sentence[u'w']:
                                if u'val' in word and word[u'val'] is not None:
                                    if word[u'val'].lower in political_context:
                                        is_word_politics = True
                                    if (word[u'val'].lower() == u'pldebatt' 
                                            or word[u'val'].lower() == u'agenda'
                                            or word[u'val'].lower() == u'svtagenda'
                                            or word[u'val'].lower() == u'pldebat'):
                                        is_word_pldebatt = True
                                    elif not with_spec_char and (p.match(word[u'val'].encode('UTF-8')) == None):
                                        pass
                                    else:
                                        if 'lemma' in word:
                                            lemmas_temp = word['lemma'].split('|')
                                            lemmas = lemmas_temp[1:-1]
                                            if not lemmas:
                                                tweet_words.append(word[u'val'].lower())
                                            else:
                                                tweet_words.append(lemmas[0].lower())
                if u'hashtags' in text:                    
                    #if (u'#pldebatt' in text[u'hashtags'] 
                    if (u'#pldebatt' in [x.lower() for x in text[u'hashtags']]
                            or u'#agenda' in [x.lower() for x in text[u'hashtags']]
                            or u'#svtagenda' in [x.lower() for x in text[u'hashtags']]
                            or u'#pldebat' in [x.lower() for x in text[u'hashtags']]
                            or is_word_pldebatt):
                        if len(tweet_words)>=minimal_tweet_length:
                            test_train_division = random.random()
                            if test_train_division <0.2:
                                saveToDir(tweet_words, tweet_id, test_folder+pldebatt_folder)
                            else:
                                saveToDir(tweet_words, tweet_id, train_folder+pldebatt_folder)  
                    elif (not is_word_politics):
                        if len(tweet_words)>=minimal_tweet_length:
                            saveToDir(tweet_words, tweet_id, predict_folder)
                            sampling_probability = random.random()
                            if sampling_probability <= 0.03:
                            #saveToDir(tweet_words, tweet_id, all_folder+nonpldebatt_folder)
                                test_train_division = random.random()
                                if test_train_division <0.2:
                                    saveToDir(tweet_words, tweet_id, test_folder+nonpldebatt_folder)
                                else:
                                    saveToDir(tweet_words, tweet_id, train_folder+nonpldebatt_folder)
                            elif text[u'hashtags']==u'|':
                                # tweets with no political words and hashtags, and having NO other hashtag
                                #saveToDir(tweet_words, tweet_id, predict_folder)
                                pass
                            else:
                                # tweets with no political words and hashtags, but having some other hashtags
                                pass
                    else:
                        # tweets with a political word, but without a political hashtag
                        if len(tweet_words)>=minimal_tweet_length:
                            saveToDir(tweet_words, tweet_id, predict_folder)
                else:
                    raise NameError('Obligationary "hashtags" attribute missing in data!')


if __name__ == "__main__":
    #db = thtdb.ThtConnection(collectionName='test_pldebatt_june')
    #db = thtdb.ThtConnection(host='squib.de', dbName='karinas_twitter_db', collectionName='twitter-pldebatt-130612')
    db = thtdb.ThtConnection(dbName='tweets_by_users_may', collectionName='twitter-pldebatt-140504_clean')
    
    saveWordsPerTweetByHashtag('20w_spec_may', 20, True)

