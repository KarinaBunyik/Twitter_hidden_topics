#from bson.son import SON
import thtdb
import io
from thtpaths import internal_path


def saveToFile(word_list, filename, dirname):
        file_path = internal_path+dirname+'/'
        #user_words_filename = internal_path+'/malletTwitterOctober/'+username
        ofile = io.open(file_path+filename+'.txt', 'wb')
        for word in word_list:
            if word is not None:
                ofile.write(word.encode('utf8')+' ')
        ofile.close()


def fileToList(filename):
        word_list = []
        ifile = io.open(internal_path+'tweetIdLists/'+filename+'.txt', 'r')
        for word in ifile:
            word_list.append(word.replace('\n',''))
        ifile.close()
        return word_list


def fileToListInput(filename):
        word_list = []
        ifile = io.open(internal_path+'tfidf/representative_words/'+filename+'.txt', 'r')
        for word in ifile:
            word_list.append(word.replace('\n',''))
        ifile.close()
        return word_list


def isWordInList(sentences, wList):
    for sentence in sentences:
        if 'w' in sentence:
            for word in sentence['w']:
                if 'val' in word:
                    if word['val'] in wList:
                        return True
    return False


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


'''
def tagUsersHavingHashtag_old(hashtag, tag):
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
'''

def tagUsersHavingHashtag(hashtag, tag):
    db.collection.update({'$and': [ {u'usertags': {'$exists': False }},
        {u'text':{'$elemMatch': {u'hashtags':{'$regex': hashtag}} }}]} , 
        {'$set' : {u'usertags' : [tag] }})
    db.collection.update({'$and': [ {u'usertags': {'$exists': True }},
        {u'text':{'$elemMatch': {u'hashtags':{'$regex': hashtag}} }},
        {u'usertags': {'$ne': tag}}  ]} , 
        {'$push':{u'usertags':tag}})

#!!!!!!!!!!!!!!!!!
def tagTweetsHavingWordAsLemma(wordList, tag):
    tweet_ids_with_words = []
    tweet_ids_tagged = []
    tweet_ids_tag_exists = []
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                if 'sentence' in text:
                    if isLemmaInList(text['sentence'], wordList):
                        if 'id' in text:
                            if text['id'] not in tweet_ids_with_words:
                                tweet_ids_with_words.append(text['id'])
                                if 'tweettags' in text:
                                    if text[u'id'] not in tweet_ids_tagged:
                                        tweet_ids_tagged.append(text[u'id'])
                                    if tag in text['tweettags']:
                                        if text[u'id'] not in tweet_ids_tag_exists:
                                            tweet_ids_tag_exists.append(text[u'id'])
    for tid in tweet_ids_with_words:
        if tid not in tweet_ids_tagged:
            db.collection.update( #{'text.id':a}, {'$set' : {'text.$.tweettags' : [tag] }})
                {'text.id':tid},
                #{'text.tweettags': {'$exists': False }}  ]}, 
                {'$set' : {'text.$.tweettags' : [tag] }})
        else:
            if tid not in tweet_ids_tag_exists:
                db.collection.update( #{'text.id':a}, {'$set' : {'text.$.tweettags' : [tag] }})
                    {'text.id':tid}, 
                    {'$push' : {'text.$.tweettags' : tag }})



def tagTweetsHavingWords(wordList, tag):
    tweet_ids_with_words = []
    tweet_ids_tagged = []
    tweet_ids_tag_exists = []
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                if 'sentence' in text:
                    if isWordInList(text['sentence'], wordList):
                        if 'id' in text:
                            if text['id'] not in tweet_ids_with_words:
                                tweet_ids_with_words.append(text['id'])
                                if 'tweettags' in text:
                                    if text[u'id'] not in tweet_ids_tagged:
                                        tweet_ids_tagged.append(text[u'id'])
                                    if tag in text['tweettags']:
                                        if text[u'id'] not in tweet_ids_tag_exists:
                                            tweet_ids_tag_exists.append(text[u'id'])
    for tid in tweet_ids_with_words:
        if tid not in tweet_ids_tagged:
            db.collection.update( #{'text.id':a}, {'$set' : {'text.$.tweettags' : [tag] }})
                {'text.id':tid},
                #{'text.tweettags': {'$exists': False }}  ]}, 
                {'$set' : {'text.$.tweettags' : [tag] }})
        else:
            if tid not in tweet_ids_tag_exists:
                db.collection.update( #{'text.id':a}, {'$set' : {'text.$.tweettags' : [tag] }})
                    {'text.id':tid}, 
                    {'$push' : {'text.$.tweettags' : tag }})

def tagTweetsHavingHashtag(hashtag, tag):
    tweet_ids_hashtag = []
    tweet_ids_tagged = []
    tweet_ids_tag_exists = []
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                if u'hashtags' in text:
                    if hashtag in text[u'hashtags'].split('|'):
                        if text[u'id'] not in tweet_ids_hashtag:
                            tweet_ids_hashtag.append(text[u'id'])
                            if 'tweettags' in text:
                                if text[u'id'] not in tweet_ids_tagged:
                                    tweet_ids_tagged.append(text[u'id'])
                                if tag in text['tweettags']:
                                    if text[u'id'] not in tweet_ids_tag_exists:
                                        tweet_ids_tag_exists.append(text[u'id'])
    for tid in tweet_ids_hashtag:
        if tid not in tweet_ids_tagged:
            db.collection.update( #{'text.id':a}, {'$set' : {'text.$.tweettags' : [tag] }})
                {'text.id':tid},
                #{'text.tweettags': {'$exists': False }}  ]}, 
                {'$set' : {'text.$.tweettags' : [tag] }})
        else:
            if tid not in tweet_ids_tag_exists:
                db.collection.update( #{'text.id':a}, {'$set' : {'text.$.tweettags' : [tag] }})
                    {'text.id':tid}, 
                    {'$push' : {'text.$.tweettags' : tag }})


#!!!!!!!!!!!!!!!!
def tagTweetsAsRepliesFromHashtag(hashtag, tag):
    tweet_ids_hashtag_replies = []
    tweet_ids_tagged = []
    tweet_ids_tag_exists = []
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                if u'hashtags' in text:
                    if hashtag in text[u'hashtags'].split('|'):
                        if 'replies' in text:
                            if text['replies'] != '|':
                                for tid in text['replies'].split('|'):
                                    if tid != '':
                                        if tid not in tweet_ids_hashtag_replies:
                                            tweet_ids_hashtag_replies.append(tid)

                                            if text[u'id'] not in tweet_ids_hashtag_replies:
                                                tweet_ids_hashtag_replies.append(text[u'id'])
                                                if 'tweettags' in text:
                                                    if text[u'id'] not in tweet_ids_tagged:
                                                        tweet_ids_tagged.append(text[u'id'])
                                                    if tag in text['tweettags']:
                                                        if text[u'id'] not in tweet_ids_tag_exists:
                                                            tweet_ids_tag_exists.append(text[u'id'])
    print tweet_ids_hashtag_replies
    for tid in tweet_ids_hashtag_replies:
        if tid not in tweet_ids_tagged:
            db.collection.update( #{'text.id':a}, {'$set' : {'text.$.tweettags' : [tag] }})
                {'text.id':tid},
                #{'text.tweettags': {'$exists': False }}  ]}, 
                {'$set' : {'text.$.tweettags' : [tag] }})
        else:
            if tid not in tweet_ids_tag_exists:
                db.collection.update( #{'text.id':a}, {'$set' : {'text.$.tweettags' : [tag] }})
                    {'text.id':tid}, 
                    {'$push' : {'text.$.tweettags' : tag }})


def tagTweetsFromFile(tweetIdFile, tag):
    tweet_ids = fileToList(tweetIdFile)
    tweet_ids_tagged = []
    tweet_ids_tag_exists = []
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                if 'id' in text:
                    if text['id'] in tweet_ids:
                        if 'tweettags' in text:
                            if text[u'id'] not in tweet_ids_tagged:
                                tweet_ids_tagged.append(text[u'id'])
                            if tag in text['tweettags']:
                                if text[u'id'] not in tweet_ids_tag_exists:
                                    tweet_ids_tag_exists.append(text[u'id'])
    for tid in tweet_ids:
        if tid not in tweet_ids_tagged:
            db.collection.update( 
                {'text.id':tid},
                {'$set' : {'text.$.tweettags' : [tag] }})
        else:
            if tid not in tweet_ids_tag_exists:
                db.collection.update(
                    {'text.id':tid}, 
                    {'$push' : {'text.$.tweettags' : tag }})


def removeUserTag(tag):
    db.collection.update( {"$and": [{u'usertags': {'$exists': True }}, {u'usertags': {'$in': [tag]}} ]}, 
        {'$pull': {u'usertags': tag}} , 
        upsert=False, 
        multi=True)


def removeTweetTag(tag):
    tweet_ids = []
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                if u'tweettags' in text:
                    if tag in text['tweettags']:
                        if text[u'id'] not in tweet_ids:
                            tweet_ids.append(text[u'id'])
    for tid in tweet_ids:
        db.collection.update(
            {'text.id':tid}, 
            {'$pull': {'text.$.tweettags': tag}}, upsert=False, multi=True)


#SHOULD NOT BE USED
def removeUserTaggingValuesTo(noTag):
    db.collection.update({u'usertags': { '$exists': True }}, { "$set": { u'usertags': noTag } }, upsert=False, multi=True)

def removeUserTagging():
    db.collection.update({}, { "$unset": { u'usertags': 1 } }, upsert=False, multi=True)


def removeTweetTagging():
    tweet_ids = []
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                if u'tweettags' in text:
                    if text[u'id'] not in tweet_ids:
                        tweet_ids.append(text[u'id'])
    for tid in tweet_ids:
        db.collection.update(
            {'text.id':tid}, 
            { "$unset": { 'text.$.tweettags': 1 } }, upsert=False, multi=True)


if __name__ == "__main__":
    #db = thtdb.ThtConnection(collectionName='test_pldebatt_june')
    #db = thtdb.ThtConnection(collectionName='test_pldebatt_june')

    db = thtdb.ThtConnection(host='squib.de', dbName='karinas_twitter_db', collectionName='twitter-pldebatt-130612')
    #tagUsersHavingHashtag('#pldebatt', 'dummy3')
    #tagUsersHavingHashtag(u'#pldebatt', 'dummy3')
    

    #tagTweetsHavingHashtag('#pldebatt', 'dummy01')
    #tagTweetsAsRepliesFromHashtag('#svpol', 'dummy06')

    #tagTweetsFromFile('test', 'dummy04')
    #saveUsersHavingHashtag('#pldebatt')
    
    #tagTweetsHavingWords(fileToList('skola'), 'dummy05')

    #removeTweetTagging()
    #removeTweetTag('dummy01')
    print 'processing crime tagging...'
    tagTweetsHavingWords(fileToListInput('brottochstraff'), 'crime')
    print 'crime tagging done.'
    print 'processing school tagging...'
    tagTweetsHavingWords(fileToListInput('skolan'), 'school')
    print 'school tagging done.'
    print 'processing climate tagging...'
    tagTweetsHavingWords(fileToListInput('klimat'), 'climate')
    print 'climate tagging done.'
    print 'processing tax tagging...'
    tagTweetsHavingWords(fileToListInput('jobbochskatt'), 'tax')
    print 'tax tagging done.'
    print 'processing immigration tagging...'
    tagTweetsHavingWords(fileToListInput('flyktingar'), 'immigration')
    print 'immigration tagging done.'
    print 'processing health tagging...'
    tagTweetsHavingWords(fileToListInput('sjukvard'), 'health')
    print 'health tagging done.'
