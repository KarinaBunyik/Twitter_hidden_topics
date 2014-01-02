#from bson.son import SON
import thtdb
import io
from thtpaths import internal_data_path
import random


def saveToDir(word_list, filename, dirname):
        dirname = dirname+'/'
        #user_words_filename = internal_path+'/malletTwitterOctober/'+username
        ofile = io.open(dirname+filename, 'wb')
        for word in word_list:
            if word is not None:
                ofile.write(word.encode('utf8')+' ')
        ofile.close()



# The following function gathers non-pldebatt and non-username words from tweets, 
# groups them by TWEETS and saves them to a file. 
# No metadata is saved. Filtering on tweets based on #pldebatt
def saveWordsPerTweetByHashtag(folder):
    print "start"
    all_folder = internal_data_path+'/hashtagPrediction/'+folder+'/raw'
    test_folder = internal_data_path+'/hashtagPrediction/'+folder+'/test'
    train_folder = internal_data_path+'/hashtagPrediction/'+folder+'/train'
    predict_folder = internal_data_path+'/hashtagPrediction/'+folder+'/predict/unknown'
    pldebatt_folder = '/pldebatt'
    nonpldebatt_folder = '/other'
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
                                    if word[u'val'] == u'pldebatt':
                                        is_word_pldebatt = True
                                    if word[u'val'] == u'debatt' or word[u'val'] == u'svpol' or word[u'val'] == u'politik':
                                        is_word_politics = True
                                    elif (u'hashtags' in text):
                                        #print(type(word[u'val']))
                                        #print("hash: ",type(text[u'hashtags']))
                                        if (word[u'val'] not in text[u'hashtags']):
                                            tweet_words.append(word[u'val'])
                if u'hashtags' in text:
                    if u'pldebatt' in text[u'hashtags'] or is_word_pldebatt:
                        if len(tweet_words)>10:
                            saveToDir(tweet_words, tweet_id, all_folder+pldebatt_folder)
                            rand = random.random()
                            if rand <0.2:
                                saveToDir(tweet_words, tweet_id, test_folder+pldebatt_folder)
                            else:
                                saveToDir(tweet_words, tweet_id, train_folder+pldebatt_folder)  
                    elif text[u'hashtags']!=u'|' and u'svpol' not in text[u'hashtags'] and not is_word_politics:
                        rand1 = random.uniform(1, 100)
                        if rand1 <= 4.5:
                            if len(tweet_words)>10:
                                saveToDir(tweet_words, tweet_id, all_folder+nonpldebatt_folder)
                                rand2 = random.random()
                                if rand2 < 0.2:
                                    saveToDir(tweet_words, tweet_id, test_folder+nonpldebatt_folder)
                                else:
                                    saveToDir(tweet_words, tweet_id, train_folder+nonpldebatt_folder)
                    else:
                        rand = random.uniform(1, 100)
                        if rand <= 1.1:
                            if len(tweet_words)>10:
                                saveToDir(tweet_words, tweet_id, predict_folder)


if __name__ == "__main__":
    #db = thtdb.ThtConnection(collectionName='test_pldebatt_june')
    #db = thtdb.ThtConnection(collectionName='test_pldebatt_june')
    db = thtdb.ThtConnection(host='squib.de', dbName='karinas_twitter_db', collectionName='twitter-pldebatt-131006')
    saveWordsPerTweetByHashtag('001')
