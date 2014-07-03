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


# Takes a twitter dataset from Sprakbanken. Creates one document for each tweet. Documents with hashtags end up in
#training example. #pldebatt hastag is positive example, other hashtags are negative examples. No hashtag tweets are
#to be predicted. The hashtags are taken away from the tweets. The positive hashtags end up in a separate folder
# called "pldebatt", the negative in "other" folder. "raw" folder contains all labeled samples without train-test split.
def saveWordsPerTweetByHashtag(folder, minimal_tweet_length):
    all_folder = internal_path+'hashtagPrediction/'+folder+'/raw'
    test_folder = internal_path+'hashtagPrediction/'+folder+'/test'
    train_folder = internal_path+'hashtagPrediction/'+folder+'/train'
    predict_folder = internal_path+'hashtagPrediction/'+folder+'/predict/unknown'
    pldebatt_folder = '/pldebatt'
    nonpldebatt_folder = '/other'

    political_context = fileToList('domain_word_list')
    #p = re.compile("[A-Za-z\såäöÅÄÖ]+$", re.UNICODE)
    #p = re.compile("[^a-zA-Z0-9]+$")
    p = re.compile("[A-Za-z\såäöÅÖÄ]+$", re.UNICODE)
    

    for user in db.collection.find():
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
                                    #res = p.match(c)
                                    elif p.match(word[u'val'].encode('UTF-8')) == None:
                                    #elif re.match('[A-Za-zÃÂÃÂÃÂÃÄĻÃÄŠÃÄ·]+$', word[u'val'].lower(), re.UNICODE) == None:
                                    #elif (re.match('[\w]+$', word[u'val'].lower(), re.U) == None):
                                        pass
                                    else:
                                        tweet_words.append(word[u'val'].lower())    
                                    #elif (u'hashtags' in text):
                                    #    if ((u'#'+word[u'val']) not in text[u'hashtags']):
                                    #        tweet_words.append(word[u'val'])
                                    #else:
                                    #    pass
                if u'hashtags' in text:
                    if len(tweet_words)>minimal_tweet_length:
                        #if (u'#pldebatt' in text[u'hashtags'] 
                        if (u'#pldebatt' in [x.lower() for x in text[u'hashtags']]
                                or u'#agenda' in [x.lower() for x in text[u'hashtags']]
                                or u'#svtagenda' in [x.lower() for x in text[u'hashtags']]
                                or u'#pldebat' in [x.lower() for x in text[u'hashtags']]
                                or is_word_pldebatt):
                            #if len(tweet_words)>minimal_tweet_length:
                            saveToDir(tweet_words, tweet_id, all_folder+pldebatt_folder)
                            test_train_division = random.random()
                            if test_train_division <0.2:
                                saveToDir(tweet_words, tweet_id, test_folder+pldebatt_folder)
                            else:
                                saveToDir(tweet_words, tweet_id, train_folder+pldebatt_folder)  
                        elif (
                                #and u'#svpol' not in text[u'hashtags'] 
                                #not is_word_pldebatt
                                not is_word_politics):
                            #sampling_probability_2 = random.uniform(1, 100)
                            sampling_probability = random.random()
                            #if rand1 <= 4.5:
                            if sampling_probability <= 0.02:
                                #if len(tweet_words)>minimal_tweet_length:
                                saveToDir(tweet_words, tweet_id, all_folder+nonpldebatt_folder)
                                test_train_division = random.random()
                                if test_train_division <0.2:
                                    saveToDir(tweet_words, tweet_id, test_folder+nonpldebatt_folder)
                                else:
                                    saveToDir(tweet_words, tweet_id, train_folder+nonpldebatt_folder)
                        elif text[u'hashtags']==u'|':
                            #rand = random.uniform(1, 100)
                            #if rand <= 1.1:
                                #if len(tweet_words)>=5:
                            pass
                            #saveToDir(tweet_words, tweet_id, predict_folder)
                        else:
                            # Tweets with other hashtags than #pldebatt
                            #raise NameError('Unexisting if case!')
                            pass
                    else:
                        # Tweets too short, will not be saved for classification.
                        pass
                else:
                    raise NameError('Obligationary "hashtags" attribute missing in data!')


if __name__ == "__main__":
    #db = thtdb.ThtConnection(collectionName='test_pldebatt_june')
    #db = thtdb.ThtConnection(host='squib.de', dbName='karinas_twitter_db', collectionName='twitter-pldebatt-130612')
    db = thtdb.ThtConnection(collectionName='twitter-pldebatt-131006')
    saveWordsPerTweetByHashtag('007', 9)
