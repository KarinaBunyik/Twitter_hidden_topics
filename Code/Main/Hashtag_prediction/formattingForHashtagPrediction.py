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

<<<<<<< HEAD
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

=======
>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d

# Takes a twitter dataset from Sprakbanken. Creates one document for each tweet. Documents with hashtags end up in
#training example. #pldebatt hastag is positive example, other hashtags are negative examples. No hashtag tweets are
#to be predicted. The hashtags are taken away from the tweets. The positive hashtags end up in a separate folder
# called "pldebatt", the negative in "other" folder. "raw" folder contains all labeled samples without train-test split.
<<<<<<< HEAD
def saveWordsPerTweetByHashtag(folder, minimal_tweet_length, with_spec_char):
=======
def saveWordsPerTweetByHashtag(folder, minimal_tweet_length):
>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d
    all_folder = internal_path+'hashtagPrediction/'+folder+'/raw'
    test_folder = internal_path+'hashtagPrediction/'+folder+'/test'
    train_folder = internal_path+'hashtagPrediction/'+folder+'/train'
    predict_folder = internal_path+'hashtagPrediction/'+folder+'/predict/unknown'
<<<<<<< HEAD
    element_counter = 0
=======
>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d
    pldebatt_folder = '/pldebatt'
    nonpldebatt_folder = '/other'

    political_context = fileToList('domain_word_list')
    #p = re.compile("[A-Za-z\såäöÅÄÖ]+$", re.UNICODE)
    #p = re.compile("[^a-zA-Z0-9]+$")
<<<<<<< HEAD
    p = re.compile("[A-Za-z0-9\såäöÅÖÄ:-]+$", re.UNICODE)

    for user in db.collection.find():
        element_counter += 1
        if element_counter % 1000 == 0:
            print element_counter
=======
    p = re.compile("[A-Za-z\såäöÅÖÄ]+$", re.UNICODE)
    

    for user in db.collection.find():
>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d
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
<<<<<<< HEAD
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
=======
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
>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d
                            test_train_division = random.random()
                            if test_train_division <0.2:
                                saveToDir(tweet_words, tweet_id, test_folder+pldebatt_folder)
                            else:
                                saveToDir(tweet_words, tweet_id, train_folder+pldebatt_folder)  
<<<<<<< HEAD
                    elif (not is_word_politics):
                        if len(tweet_words)>=minimal_tweet_length:
                            saveToDir(tweet_words, tweet_id, predict_folder)
                            sampling_probability = random.random()
                            if sampling_probability <= 0.03:
                            #saveToDir(tweet_words, tweet_id, all_folder+nonpldebatt_folder)
=======
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
>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d
                                test_train_division = random.random()
                                if test_train_division <0.2:
                                    saveToDir(tweet_words, tweet_id, test_folder+nonpldebatt_folder)
                                else:
                                    saveToDir(tweet_words, tweet_id, train_folder+nonpldebatt_folder)
<<<<<<< HEAD
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
=======
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
>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d
                else:
                    raise NameError('Obligationary "hashtags" attribute missing in data!')


if __name__ == "__main__":
    #db = thtdb.ThtConnection(collectionName='test_pldebatt_june')
    #db = thtdb.ThtConnection(host='squib.de', dbName='karinas_twitter_db', collectionName='twitter-pldebatt-130612')
<<<<<<< HEAD
    db = thtdb.ThtConnection(dbName='tweets_by_users_may', collectionName='twitter-pldebatt-140504_clean')
    
    saveWordsPerTweetByHashtag('20w_spec_may', 20, True)

=======
    db = thtdb.ThtConnection(collectionName='twitter-pldebatt-131006')
    saveWordsPerTweetByHashtag('007', 9)
>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d
