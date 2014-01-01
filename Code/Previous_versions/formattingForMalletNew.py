#from bson.son import SON
import thtdb
import io
from thtpaths import internal_data_path
#from bson.code import Code
import random


def saveToFile(word_list, filename, dirname):
        file_path = internal_data_path+dirname+'/'
        #user_words_filename = internal_path+'/malletTwitterOctober/'+username
        ofile = io.open(file_path+filename+'.txt', 'wb')
        for word in word_list:
            ofile.write(word.encode('utf8')+' ')
        ofile.close()


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
def saveWordsPerTweet(dirname):
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                if u'mentions' in text:
                    mentions_list = text[u'mentions'].split('|')
                else:
                    mentions_list = []
                if u'hashtags' in text:
                    if "pldebatt" in text[u'hashtags']:
                        tweet_words = []
                        tweet_id = text[u'id']
                        if u'sentence' in text:
                            for sentence in text[u'sentence']:
                                if u'w' in sentence:
                                    for word in sentence[u'w']:
                                        if u'val' in word:
                                            if word[u'val']!='pldebatt' and word[u'val'] not in mentions_list:
                                                tweet_words.append(word[u'val'])
                        if tweet_words:
                            saveToFile(tweet_words, tweet_id, dirname)


# The following function gathers non-pldebatt and non-username words from tweets, 
# groups them by USER and saves them to a file. 
# No metadata is saved. Filtering on tweets based on #pldebatt
def saveWordsPerUser(dirname):
    no_users = 0
    for user in db.collection.find():
        user_words = []
        if u'username' in user:
            username = user[u'username']
            if u'text' in user:
                for text in user[u'text']:
                    if u'mentions' in text:
                        mentions_list = text[u'mentions'].split('|')
                    else:
                        mentions_list = []                    
                    if u'hashtags' in text:
                        if "pldebatt" in text[u'hashtags']:
                            if u'sentence' in text:
                                for sentence in text[u'sentence']:
                                    if u'w' in sentence:
                                        for word in sentence[u'w']:
                                            if u'val' in word:
                                                if word[u'val']!='pldebatt' and word[u'val'] not in mentions_list:
                                                    user_words.append(word[u'val'])
        if u'username' in user:
            username = user[u'username']
        else:
            username = str(random.randint(1, 10000))
        if user_words:
            saveToFile(user_words, username, dirname)
        user_words = []
        no_users += 1
    print "number of LDA documents: ", no_users


# The following function gathers non-pldebatt and non-username words from tweets, 
# groups them by TWEETS and saves them to a file. 
# No metadata is saved. Filtering on tweets based on #pldebatt
def saveWordsPerTweetByHashtag():
    print "start"
    all_folder = '/Users/karinabunyik/BTSync/Data/Test/001/raw'
    test_folder = '/Users/karinabunyik/BTSync/Data/Test/001/test'
    train_folder = '/Users/karinabunyik/BTSync/Data/Test/001/train'
    predict_folder = '/Users/karinabunyik/BTSync/Data/Test/001/predict/unknown'
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
                        if rand1 <= 1.4:
                            if len(tweet_words)>10:
                                saveToDir(tweet_words, tweet_id, all_folder+nonpldebatt_folder)
                                rand2 = random.random()
                                if rand2 < 0.2:
                                    saveToDir(tweet_words, tweet_id, test_folder+nonpldebatt_folder)
                                else:
                                    saveToDir(tweet_words, tweet_id, train_folder+nonpldebatt_folder)
                    else:
                        if len(tweet_words)>10:
                            saveToDir(tweet_words, tweet_id, predict_folder)



'''
                if u'hashtags' in text:
                    if "pldebatt" in text[u'hashtags']:
                        tweet_words = []
                        tweet_id = text[u'id']
                        is_word_pldebatt = False
                        if u'sentence' in text:
                            for sentence in text[u'sentence']:
                                if u'w' in sentence:
                                    for word in sentence[u'w']:
                                        if word[u'val'] == 'pldebatt':
                                            is_word_pldebatt = False

                                        if u'val' in word:
                                            if word[u'val'] == 'pldebatt':
                                                is_word_pldebatt = False
                                            else:
                                                tweet_words.append(word[u'val'])
                        if is_word_pldebatt:
                            if len(tweet_words)>0:
                                saveToDir(tweet_words, tweet_id, all_folder+pldebatt_folder)
                                rand = random.random()
                                if rand <0.4:
                                    saveToDir(tweet_words, tweet_id, test_folder+pldebatt_folder)
                                else:
                                    saveToDir(tweet_words, tweet_id, train_folder+pldebatt_folder)

                    elif text[u'hashtags'] == '|':
                        r = random.uniform(1, 100)
                        if r <= 1.04:
                            tweet_words = []
                            tweet_id = text[u'id']
                            if u'sentence' in text:
                                for sentence in text[u'sentence']:
                                    if u'w' in sentence:
                                        for word in sentence[u'w']:
                                            if u'val' in word and word[u'val'] != 'pldebatt':
                                                tweet_words.append(word[u'val'])
                            if len(tweet_words)>0:
                                saveToDir(tweet_words, tweet_id, all_folder+nonpldebatt_folder)
                                rand = random.random()
                                if rand <0.4:
                                    saveToDir(tweet_words, tweet_id, test_folder+nonpldebatt_folder)
                                else:
                                    saveToDir(tweet_words, tweet_id, train_folder+nonpldebatt_folder)
'''

# The following function gathers non-username words from ALL tweets, groups them by user and saves them to a file. 
# No metadata is saved. No filtering on the tweets is made.
def saveWordsPerUserAll(dirname):
    no_users = 0
    for user in db.collection.find():
        user_words = []
        if u'username' in user:
            username = user[u'username']
            if u'text' in user:
                for text in user[u'text']:
                    if u'mentions' in text:
                        mentions_list = text[u'mentions'].split('|')
                    else:
                        mentions_list = [] 
                    if u'sentence' in text:
                        for sentence in text[u'sentence']:
                            if u'w' in sentence:
                                for word in sentence[u'w']:
                                    if u'val' in word and word[u'val'] not in mentions_list:
                                        user_words.append(word[u'val'])
        if u'username' in user:
            username = user[u'username']
        else:
            username = str(random.randint(1, 10000))
        if user_words:
            saveToFile(user_words, username, dirname)
        user_words = []
        no_users += 1
    print "number of LDA documents: ", no_users


'''
# The following function gathers non-pldebatt and non-username words from tweets that include #pldebatt hashtag, 
# groups them by user and saves them to a file. 
# No metadata is saved. Filtering on tweets based on #pldebatt
def saveWordsPerUserNoUsername(dirname):
    no_users = 0
    for user in db.collection.find():
        user_words = []
        if u'username' in user:
            username = user[u'username']
            if u'text' in user:
                if isinstance(user[u'text'], dict): 
                    if u'mentions' in user[u'text']:
                        mentions_list = user[u'text'][u'mentions'].split('|')
                    else:
                        mentions_list = []
                    if u'hashtags' in user[u'text']:
                        if "pldebatt" in user[u'text'][u'hashtags']:
                            if u'sentence' in user[u'text']:
                                if isinstance(user[u'text'][u'sentence'], dict):
                                    if u'w' in user[u'text'][u'sentence']:
                                        if isinstance(user[u'text'][u'sentence'][u'w'], dict):
                                            if u'val' in user[u'text'][u'sentence'][u'w']:
                                                if user[u'text'][u'sentence'][u'w'][u'val']!='pldebatt' and user[u'text'][u'sentence'][u'w'][u'val'] not in mentions_list:
                                                    user_words.append(user[u'text'][u'sentence'][u'w'][u'val'])
                                        else:
                                            for word in user[u'text'][u'sentence'][u'w']:
                                                if u'val' in word:
                                                    if word[u'val']!='pldebatt' and word[u'val'] not in mentions_list:
                                                        user_words.append(word[u'val'])
                                else:
                                    for sentence in user[u'text'][u'sentence']:
                                        if u'w' in sentence:
                                            if isinstance(sentence[u'w'], dict):
                                                if u'val' in sentence[u'w']:
                                                    if sentence[u'w'][u'val']!='pldebatt' and sentence[u'w'][u'val'] not in mentions_list:
                                                        user_words.append(sentence[u'w'][u'val'])
                                            else:
                                                for word in sentence[u'w']: 
                                                    if u'val' in word:
                                                        if word[u'val']!='pldebatt' and word[u'val'] not in mentions_list:
                                                            user_words.append(word[u'val'])
                    mentions_list = []
                else:
                    for text in user[u'text']:
                        if u'mentions' in text:
                            mentions_list = text[u'mentions'].split('|')
                        else:
                            mentions_list = []
                        if u'hashtags' in text:
                            if "pldebatt" in text[u'hashtags']:
                                if u'sentence' in text:
                                    if isinstance(text[u'sentence'], dict):
                                        if u'w' in text[u'sentence']:
                                            if isinstance(text[u'sentence'][u'w'], dict):
                                                if u'val' in text[u'sentence'][u'w']:
                                                    if text[u'sentence'][u'w'][u'val']!='pldebatt' and text[u'sentence'][u'w'][u'val'] not in mentions_list:
                                                        user_words.append(text[u'sentence'][u'w'][u'val'])
                                            else:
                                                for word in text[u'sentence'][u'w']:
                                                    if u'val' in word:
                                                        if word[u'val']!='pldebatt' and word[u'val'] not in mentions_list:
                                                            user_words.append(word[u'val'])
                                    else:
                                        for sentence in text[u'sentence']:
                                            if u'w' in sentence:
                                                if isinstance(sentence[u'w'], dict):
                                                    if u'val' in sentence[u'w']:
                                                        if sentence[u'w'][u'val']!='pldebatt' and sentence[u'w'][u'val'] not in mentions_list:
                                                            user_words.append(sentence[u'w'][u'val'])
                                                else:
                                                    for word in sentence[u'w']:
                                                        if u'val' in word:
                                                            if word[u'val']!='pldebatt' and word[u'val'] not in mentions_list:
                                                                user_words.append(word[u'val'])
                        mentions_list = []
        if u'username' in user:
            username = user[u'username']
        else:
            username = str(random.randint(1, 10000))
        if user_words:
            saveToFile(user_words, username, dirname)
            no_users += 1
        user_words = []
    print "number of LDA documents: ", no_users
'''


# The following function gathers non-pldebatt and non-username words from tweets that include #pldebatt hashtag, 
# groups them by user and saves them to a file. 
# No metadata is saved. Filtering on tweets based on #pldebatt

'''
def saveWordsPerUserNoUsernameNoRetweets(dirname):
    no_users = 0
    for user in db.collection.find():
        user_words = []
        if u'username' in user:
            username = user[u'username']
            if u'text' in user:
                if isinstance(user[u'text'], dict): 
                    if u'mentions' in user[u'text']:
                        mentions_list = user[u'text'][u'mentions'].split('|')
                    else:
                        mentions_list = []
                    is_retweet = False
                    if u'sentence' in user[u'text']:
                        if isinstance(user[u'text'][u'sentence'], dict):
                            if u'w' in user[u'text'][u'sentence']:
                                if isinstance(user[u'text'][u'sentence'][u'w'], dict):
                                    if u'val' in user[u'text'][u'sentence'][u'w']:
                                        if user[u'text'][u'sentence'][u'w'][u'val']=='RE':
                                            is_retweet = True
                                else:
                                    for word in user[u'text'][u'sentence'][u'w']:
                                        if u'val' in word:
                                            if word[u'val']=='RE':
                                                is_retweet = True
                        else:
                            for sentence in user[u'text'][u'sentence']:
                                if u'w' in sentence:
                                    if isinstance(sentence[u'w'], dict):
                                        if u'val' in sentence[u'w']:
                                            if sentence[u'w'][u'val']=='RE':
                                                is_retweet = True
                                    else:
                                        for word in sentence[u'w']: 
                                            if u'val' in word:
                                                if word[u'val']=='RE':
                                                    is_retweet = True
                    if not is_retweet:
                        if u'hashtags' in user[u'text']:
                            if "pldebatt" in user[u'text'][u'hashtags']:
                                if u'sentence' in user[u'text']:
                                    if isinstance(user[u'text'][u'sentence'], dict):
                                        if u'w' in user[u'text'][u'sentence']:
                                            if isinstance(user[u'text'][u'sentence'][u'w'], dict):
                                                if u'val' in user[u'text'][u'sentence'][u'w']:
                                                    user[u'text'][u'sentence'][u'w'][u'val']!='RE'
                                                    if user[u'text'][u'sentence'][u'w'][u'val']!='pldebatt' and user[u'text'][u'sentence'][u'w'][u'val'] not in mentions_list:
                                                        user_words.append(user[u'text'][u'sentence'][u'w'][u'val'])
                                            else:
                                                for word in user[u'text'][u'sentence'][u'w']:
                                                    if u'val' in word:
                                                        if word[u'val']!='pldebatt' and word[u'val'] not in mentions_list:
                                                            user_words.append(word[u'val'])
                                    else:
                                        for sentence in user[u'text'][u'sentence']:
                                            if u'w' in sentence:
                                                if isinstance(sentence[u'w'], dict):
                                                    if u'val' in sentence[u'w']:
                                                        if sentence[u'w'][u'val']!='pldebatt' and sentence[u'w'][u'val'] not in mentions_list:
                                                            user_words.append(sentence[u'w'][u'val'])
                                                else:
                                                    for word in sentence[u'w']: 
                                                        if u'val' in word:
                                                            if word[u'val']!='pldebatt' and word[u'val'] not in mentions_list:
                                                                user_words.append(word[u'val'])
                    mentions_list = []
                else:
                    for text in user[u'text']:
                        if u'mentions' in text:
                            mentions_list = text[u'mentions'].split('|')
                        else:
                            mentions_list = []
                        if u'hashtags' in text:
                            if "pldebatt" in text[u'hashtags']:
                                if u'sentence' in text:
                                    if isinstance(text[u'sentence'], dict):
                                        if u'w' in text[u'sentence']:
                                            if isinstance(text[u'sentence'][u'w'], dict):
                                                if u'val' in text[u'sentence'][u'w']:
                                                    if text[u'sentence'][u'w'][u'val']!='pldebatt' and text[u'sentence'][u'w'][u'val'] not in mentions_list:
                                                        user_words.append(text[u'sentence'][u'w'][u'val'])
                                            else:
                                                for word in text[u'sentence'][u'w']:
                                                    if u'val' in word:
                                                        if word[u'val']!='pldebatt' and word[u'val'] not in mentions_list:
                                                            user_words.append(word[u'val'])
                                    else:
                                        for sentence in text[u'sentence']:
                                            if u'w' in sentence:
                                                if isinstance(sentence[u'w'], dict):
                                                    if u'val' in sentence[u'w']:
                                                        if sentence[u'w'][u'val']!='pldebatt' and sentence[u'w'][u'val'] not in mentions_list:
                                                            user_words.append(sentence[u'w'][u'val'])
                                                else:
                                                    for word in sentence[u'w']:
                                                        if u'val' in word:
                                                            if word[u'val']!='pldebatt' and word[u'val'] not in mentions_list:
                                                                user_words.append(word[u'val'])
                        mentions_list = []
        if u'username' in user:
            username = user[u'username']
        else:
            username = str(random.randint(1, 10000))
        if user_words:
            saveToFile(user_words, username, dirname)
            no_users += 1
        user_words = []
    print "number of LDA documents: ", no_users
'''

if __name__ == "__main__":
    #db = thtdb.ThtConnection(collectionName='test_pldebatt_june')
    #db = thtdb.ThtConnection(collectionName='test_pldebatt_june')
    db = thtdb.ThtConnection(host='squib.de', dbName='karinas_twitter_db', collectionName='twitter-pldebatt-130612')
    #saveWordsPerUser('malletTwitterOctober')
    #saveWordsPerUser('malletTwitterLDAJune')
    saveWordsPerTweetByHashtag()
