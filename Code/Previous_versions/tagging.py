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


def saveUsersHavingHashtag(hashtag):
    users_hashtag = []
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                if u'hashtags' in text:
                    if hashtag in text[u'hashtags'].split('|'):
                        if user[u'_id'] not in users_hashtag:
                            users_hashtag.append(user[u'_id'])
    saveToFile(users_hashtag, 'sampleUsersHashtagPldebatt', 'testSamples')



def tagUsersHavingHashtag(hashtag, tag):
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                if u'hashtags' in text:
                    if hashtag in text[u'hashtags'].split('|'):
                        if u'usertags' not in user:
                            db.collection.update({'_id' : user[u'_id']}, {'$set' : {'usertags' : [tag] }})
                            print 'tagged!'
                        else:
                            if tag not in user[u'usertags']:
                                db.collection.update({'_id' : user[u'_id']}, {'$push':{u'usertags':tag}})
                                print "apended"
                            else:
                                print "in"

def tagUsersHavingHashtag2(hashtag, tag):
    db.collection.update({'$and': [ {u'usertags': {'$exists': False }},
        {u'text':{'$elemMatch': {u'hashtags':{'$regex': hashtag}} }}]} , 
        {'$set' : {u'usertags' : [tag] }})
    db.collection.update({'$and': [ {u'usertags': {'$exists': True }},
        {u'text':{'$elemMatch': {u'hashtags':{'$regex': hashtag}} }},
        {u'usertags': {'$ne': tag}}  ]} , 
        {'$push':{u'usertags':tag}})
    #for user in db.collection.find({u'text':{'$elemMatch': {u'hashtags':u'|#pldebatt|'}   }}):
    #    print user['_id']
    #{u'text':{'$elemMatch': {u'hashtags':'/'+tag+'/'}   }}

def tagTweetsHavingWords(wordList, tag):
    pass

def tagTweetsHavingHashtag(hashtag, tag):
    tweet_ids = []
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                if u'hashtags' in text:
                    if hashtag in text[u'hashtags'].split('|'):
                        tweet_ids.append(text[u'id'])
    db.collection.update( {
        {u'text':{'$elemMatch': {
        '$and': [ 
        {},
        u'id':{'$in': tweet_ids}} }}]},
        {})

def tagTweetsAsRepliesFromHashtag(hashtag, tag):
    pass


def tagTweetsFromList(tweetIdList, tag):
    pass


def removeTag(tag):
    db.collection.update( {"$and": [{u'usertags': {'$exists': True }}, {u'usertags': {'$in': [tag]}} ]}, 
        {'$pull': {u'usertags': tag}} , 
        upsert=False, 
        multi=True)

#SHOULD NOT BE USED
def removeTaggingValuesTo(noTag):
    db.collection.update({u'usertags': { '$exists': True }}, { "$set": { u'usertags': noTag } }, upsert=False, multi=True)

def removeTagging():
    db.collection.update({}, { "$unset": { u'usertags': 1 } }, upsert=False, multi=True)



if __name__ == "__main__":
    #db = thtdb.ThtConnection(collectionName='test_pldebatt_june')
    #db = thtdb.ThtConnection(collectionName='test_pldebatt_june')

    db = thtdb.ThtConnection(host='squib.de', dbName='karinas_twitter_db', collectionName='twitter-pldebatt-medium')
    #tagUsersHavingHashtag('#pldebatt', 'dummy3')
    
    #tagUsersHavingHashtag2(u'#pldebatt', 'dummy3')
    #saveUsersHavingHashtag('#pldebatt')
    #removeTagging()
    removeTag('dummy2')
