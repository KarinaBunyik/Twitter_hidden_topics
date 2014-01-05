#from bson.son import SON
import thtdb
import io
import os
from thtpaths import internal_path
#from bson.code import Code
import random
import itertools


def isRetweet(word_list):
    if len(word_list)>0:
        if word_list[0]=='RT' and word_list[0]=='@':
            return True
        else:
            return False
    else:
        return True

def saveToFile(word_list, filename, dirname):
        file_path = internal_path+dirname+'/'
        #user_words_filename = internal_path+'/malletTwitterOctober/'+username
        ofile = io.open(file_path+filename+'.txt', 'wb')
        for word in word_list:
            if word is not None:
                ofile.write(word.encode('utf8')+' ')
        ofile.close()


def updateFileWithFile(update_filename, filename, dirname):
    file_path = internal_path+dirname+'/'
    #user_words_filename = internal_path+'/malletTwitterOctober/'+username
    ofile = io.open(file_path+update_filename+'.txt', 'ab')
    ifile = io.open(file_path+filename+'.txt', 'rb')
    for word in ifile:
        if word is not None:
            ofile.write(word.encode('utf8')+' ')
    ofile.close()
    ifile.close()

def updateFile(word_list, filename, dirname):
        file_path = internal_path+dirname+'/'
        #user_words_filename = internal_path+'/malletTwitterOctober/'+username
        ofile = io.open(file_path+filename+'.txt', 'ab')
        for word in word_list:
            if word is not None:
                ofile.write(word.encode('utf8')+' ')
        ofile.close()


def wordForTopics(word_dict, stemming):
    if stemming == u'lemma':
        if word_dict[u'lemma'] != '|':
            return (word_dict[u'lemma'].split('|'))[1]
        else:
            return word_dict[u'val']
    elif stemming == u'val':
        return word_dict[u'val']


def mergeFiles(filename_list,new_filename, dirname):
    file_path = internal_path+dirname+'/'
    newfile = io.open(file_path+new_filename+'.txt', 'wb')
    for filename in filename_list:
        ifile = io.open(file_path+filename+'.txt', 'rb')
        file_content = ifile.read()
        ifile.close()
        os.remove(file_path+filename+'.txt')
        newfile.write(file_content)
    newfile.close()
        

def overlaps(list1, list2):
    sb = set(list2)
    overlap = any(itertools.imap(sb.__contains__, list1))
    return overlap


def findCluster(cluster_dict, hashtags):
    new_cluster_dict = dict()
    anyOverlaps = False
    for key, value in cluster_dict.iteritems():
        if overlaps(value,hashtags):
            new_cluster_dict[key] = value
            anyOverlaps = True
    new_cluster_key = str(int(max(cluster_dict.keys(), key=int)) + 1)
    if anyOverlaps:
        return new_cluster_dict, new_cluster_key
    else:
        return dict(), new_cluster_key


def collapseSubCluster(cluster_dict, current_hashtags):
    hashtag_set = set(current_hashtags)
    for key, value in cluster_dict.iteritems():
        hashtag_set.update(value)
    #print 'hashtag union: ', list(hashtag_set)
    return list(hashtag_set)

def collapsedKeys(cluster_dict):
    key_list = []
    for key in cluster_dict.iterkeys():
        key_list.append(key)
    return key_list

def updateFilesReturnNewDictElem(cluster_dict, hashtags, word_list, dirname):
    isNotEmpty = (cluster_dict and True) or False
    if not isNotEmpty:
        saveToFile(word_list, '1', dirname)
        return cluster_dict, ['1',hashtags]
    else:
        sub_cluster_dict, new_key = findCluster(cluster_dict, hashtags)
        isNotEmpty = (sub_cluster_dict and True) or False
        if not isNotEmpty:
            saveToFile(word_list, new_key, dirname)
            return sub_cluster_dict, [new_key,hashtags]
        else:
            sub_cluster_files = collapsedKeys(sub_cluster_dict)
            #print 'subcluster collapsed filenames: ', sub_cluster_files
            new_hashtags = collapseSubCluster(sub_cluster_dict, hashtags)
            updateClusterFiles(sub_cluster_files, word_list, new_key, dirname)
            return sub_cluster_dict, [new_key,new_hashtags]

def updateClusterFiles(sub_cluster_files, word_list, new_key, dirname):
    file_path = internal_path+dirname+'/'
    tempfile = io.open(file_path+'temp'+'.txt', 'wb')
    for word in word_list:
        if word is not None:
            tempfile.write(word.encode('utf8')+' ')
    tempfile.close()
    sub_cluster_files.append('temp')
    mergeFiles(sub_cluster_files, new_key, dirname)



def fileToList(filename):
        word_list = []
        ifile = io.open(internal_path+filename+'.txt', 'r')
        #ifile = codecs.open(internal_path+filename+'.txt', 'rb', "utf-8")
        for word in ifile:
            word_list.append(word.replace('\n',''))
            #word_list.append((word.replace('\n','')).encode('utf8'))
        ifile.close()
        return word_list


# The following function gathers non-pldebatt and non-username words from tweets, 
# groups them by TWEETS and saves them to a file. 
# No metadata is saved. Filtering on tweets based on #pldebatt
def saveWordsPerTweet(dirname):
    no_go_list = fileToList('english_stoplist')+fileToList('swedish_stoplist')+fileToList('domain_word_list')
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
                                            word_cond = word[u'val']!='pldebatt' and \
                                                        word[u'val'] not in mentions_list and \
                                                        word[u'val'] not in no_go_list
                                            if word_cond:
                                                tweet_words.append(wordForTopics(word,u'lemma'))
                        if tweet_words:
                            saveToFile(tweet_words, tweet_id, dirname)


# The following function gathers non-pldebatt and non-username words from tweets, 
# groups them by USER and saves them to a file. 
# No metadata is saved. Filtering on tweets based on #pldebatt
def saveWordsPerUser(dirname):
    no_go_list = fileToList('english_stoplist')+fileToList('swedish_stoplist')+fileToList('domain_word_list')
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
                                                word_cond = word[u'val']!='pldebatt' and \
                                                            word[u'val'] not in mentions_list and \
                                                            word[u'val'] not in no_go_list
                                                if word_cond:
                                                    user_words.append(wordForTopics(word,u'lemma'))
        if u'username' in user:
            username = user[u'username']
        else:
            username = str(random.randint(1, 10000))
        if len(user_words)>0:
            saveToFile(user_words, username, dirname)
            no_users += 1
        user_words = []
    print "number of LDA documents: ", no_users


# The following function gathers non-pldebatt and non-username words from tweets, 
# groups them by USER and saves them to a file. 
# No metadata is saved. Filtering on tweets based on #pldebatt
def saveWordsPerHashtag(dirname):
    no_go_list = fileToList('english_stoplist')+fileToList('swedish_stoplist')+fileToList('domain_word_list')
    retweets = 0
    tweets = 0
    for user in db.collection.find():
        if u'username' in user:
            if u'text' in user:
                for text in user[u'text']:
                    tweet_words = []
                    hashtags = []
                    if u'mentions' in text:
                        mentions_list = text[u'mentions'].split('|')
                    else:
                        mentions_list = []                    
                    if u'hashtags' in text:
                        if text[u'hashtags'] != '|#pldebatt|':
                            hashtags_temp = text[u'hashtags'].split('|')
                            hashtags = hashtags_temp[1:len(hashtags_temp)-1]
                        else:
                            hashtags = [u'noHashtag']
                        if "pldebatt" in text[u'hashtags']:
                            if u'sentence' in text:
                                for sentence in text[u'sentence']:
                                    if u'w' in sentence:
                                        for word in sentence[u'w']:
                                            if u'val' in word:
                                                word_cond = word[u'val']!='pldebatt' and \
                                                            word[u'val'] not in mentions_list and \
                                                            word[u'val'] not in no_go_list

                                                if word_cond:
                                                    if word[u'val']==u'RE':
                                                        print 'retweet'
                                                    tweet_words.append(wordForTopics(word,u'lemma'))
                    if len(tweet_words)>0:
                        tweets += 1
                        if not isRetweet(tweet_words):
                            for hashtag in hashtags:
                                if hashtag != u'#pldebatt':
                                    updateFile(tweet_words, hashtag, dirname)
                        else:
                            retweets += 1
    print "Number of retweets: ", retweets
    print "Number of tweets: ",tweets

def saveWordsPerReply(dirname):
    no_go_list = fileToList('english_stoplist')+fileToList('swedish_stoplist')+fileToList('domain_word_list')
    no_of_replies = 0
    for user in db.collection.find():
        if u'username' in user:
            if u'text' in user:
                for text in user[u'text']:
                    tweet_words = []
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
                                                word_cond = word[u'val']!='pldebatt' and \
                                                            word[u'val'] not in mentions_list and \
                                                            word[u'val'] not in no_go_list
                                                if word_cond:
                                                    tweet_words.append(wordForTopics(word,u'lemma'))

                    if len(tweet_words)>0:
                        if u'id' in text:
                            tweet_id = text[u'id']
                        else:
                            tweet_id = 'noid'
                        if u'replytostatus' not in text:
                            saveToFile(tweet_words, tweet_id, dirname)
                        else:
                            no_of_replies += 1
                            reply_id =  text[u'replytostatus']
                            if os.path.exists(internal_path+dirname+'/'+reply_id+'.txt'):
                                print reply_id, tweet_id
                            updateFile(tweet_words, reply_id, dirname)
    print 'no of replies: ', no_of_replies


# The following function gathers non-pldebatt and non-username words from tweets, 
# groups them by USER and saves them to a file. 
# No metadata is saved. Filtering on tweets based on #pldebatt
def saveWordsPerHashtagCluster(dirname):
    no_go_list = fileToList('english_stoplist')+fileToList('swedish_stoplist')+fileToList('domain_word_list')
    cluster_dict = dict()
    for user in db.collection.find():
        if u'username' in user:
            if u'text' in user:
                for text in user[u'text']:
                    tweet_words = []
                    hashtags = []
                    if u'mentions' in text:
                        mentions_list = text[u'mentions'].split('|')
                    else:
                        mentions_list = []                    
                    if u'hashtags' in text:
                        if u'#pldebatt' in text[u'hashtags']:
                            if text[u'hashtags'] != '|#pldebatt|':
                                hashtags_temp = text[u'hashtags'].split('|')
                                hashtags = hashtags_temp[1:len(hashtags_temp)-1]
                                if u'#pldebatt' in hashtags:
                                    hashtags.remove(u'#pldebatt')
                            else:
                                hashtags = [u'noHashtag']
                            if u'sentence' in text:
                                for sentence in text[u'sentence']:
                                    if u'w' in sentence:
                                        for word in sentence[u'w']:
                                            if u'val' in word:
                                                word_cond = word[u'val']!='pldebatt' and \
                                                            word[u'val'] not in mentions_list and \
                                                            word[u'val'] not in no_go_list
                                                if word_cond:
                                                    tweet_words.append(wordForTopics(word,u'lemma'))
                    if len(tweet_words)>0 and hashtags != [u'noHashtag']:
                        toDelete, keyValPair = updateFilesReturnNewDictElem(cluster_dict, hashtags, tweet_words, dirname)
                        isNotEmpty = (toDelete and True) or False
                        if isNotEmpty:
                            for key in toDelete.iterkeys():
                                del cluster_dict[key]
                        cluster_dict[keyValPair[0]] = keyValPair[1]
    print 'dict: ', cluster_dict


# The following function gathers non-username words from ALL tweets, groups them by user and saves them to a file. 
# No metadata is saved. No filtering on the tweets is made.
def saveWordsPerUserAll(dirname):
    no_go_list = fileToList('english_stoplist')+fileToList('swedish_stoplist')
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
                                    if u'val' in word:
                                        if word[u'val'] not in mentions_list and word[u'val'] not in no_go_list:
                                            user_words.append(wordForTopics(word,u'lemma'))
        if u'username' in user:
            username = user[u'username']
        else:
            username = str(random.randint(1, 10000))
        if user_words:
            saveToFile(user_words, username, dirname)
        user_words = []
        no_users += 1
    print "number of LDA documents: ", no_users


if __name__ == "__main__":
    #db = thtdb.ThtConnection(collectionName='test_pldebatt_june')
    #db = thtdb.ThtConnection(collectionName='test_pldebatt_june')

    db = thtdb.ThtConnection(host='squib.de', dbName='karinas_twitter_db', collectionName='twitter-pldebatt-131006')
    saveWordsPerReply('malletTwitterLDAOctober_test2')
    #saveWordsPerUserAll('malletTwitterLDA_short')
    #mergeFiles(['#utbpol','#age','#aftonbladet'],'new','test')
