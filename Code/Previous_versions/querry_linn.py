
import thtdb
import io
from thtpaths import output_path


def querries():

    # most frequent words co-occuring with the hashtag #pldebatt
    word_stat_filename = output_path+"word_stat_june_test"
    word_stat_file = io.open(word_stat_filename+'.out', 'wb')

    # usernames that tweet most frequently with the hashtag #pldebatt
    user_stat_filename = output_path+"user_stat_june_test"
    user_stat_file = io.open(user_stat_filename+'.out', 'wb')

    # most frequent hashtags co-occuring with the hashtag #pldebatt
    hash_stat_filename = output_path+"hash_stat_june_test"
    hash_stat_file = io.open(hash_stat_filename+'.out', 'wb')

    count = 0
    user_stat = dict()
    hash_stat = dict()
    word_stat = dict()
    for user in db.collection.find():
        if u'username' in user:
            username = user[u'username']
            count += 1
            if True:
                if u'text' in user:
                    if isinstance(user[u'text'], dict): 
                        if u'hashtags' in user[u'text']:
                            if "pldebatt" in user[u'text'][u'hashtags']:
                                hash_list = user[u'text'][u'hashtags'].split('|')
                                if hash_list:
                                    for hashtag in hash_list:
                                        if hashtag != '#pldebatt' and hashtag!='':
                                            if hashtag in hash_stat:
                                                hash_stat[hashtag] += 1
                                            else:
                                                hash_stat[hashtag] = 1
                                if username in user_stat:
                                    user_stat[username] += 1
                                else:
                                    user_stat[username] = 1
                                if u'sentence' in user[u'text']:
                                    if isinstance(user[u'text'][u'sentence'], dict):
                                        if u'w' in user[u'text'][u'sentence']:
                                            if isinstance(user[u'text'][u'sentence'][u'w'], dict):
                                                if u'val' in user[u'text'][u'sentence'][u'w']:
                                                    if user[u'text'][u'sentence'][u'w'][u'val'] in word_stat:
                                                        word_stat[user[u'text'][u'sentence'][u'w'][u'val']] += 1
                                                    else:
                                                        word_stat[user[u'text'][u'sentence'][u'w'][u'val']] = 1
                                            else:
                                                for word in user[u'text'][u'sentence'][u'w']:
                                                    if u'val' in word:
                                                        if word[u'val'] in word_stat:
                                                            word_stat[word[u'val']] += 1
                                                        else:
                                                            word_stat[word[u'val']] = 1

                                    else:
                                        for sentence in user[u'text'][u'sentence']:
                                            if u'w' in sentence:
                                                if isinstance(sentence[u'w'], dict):
                                                    if u'val' in sentence[u'w']:
                                                        if sentence[u'w'][u'val'] in word_stat:
                                                            word_stat[sentence[u'w'][u'val']] += 1
                                                        else:
                                                            word_stat[sentence[u'w'][u'val']] = 1
                                                else:
                                                    for word in sentence[u'w']:
                                                        if u'val' in word:
                                                            if word[u'val'] in word_stat:
                                                                word_stat[word[u'val']] += 1
                                                            else:
                                                                word_stat[word[u'val']] = 1
                    else:
                        for text in user[u'text']:
                            if u'hashtags' in text:
                                if "pldebatt" in text[u'hashtags']:
                                    hash_list = text[u'hashtags'].split('|')
                                    if hash_list:
                                        for hashtag in hash_list:
                                            if hashtag != '#pldebatt' and hashtag!='':
                                                if hashtag in hash_stat:
                                                    hash_stat[hashtag] += 1
                                                else:
                                                    hash_stat[hashtag] = 1
                                    if username in user_stat:
                                        user_stat[username] += 1
                                    else:
                                        user_stat[username] = 1
                                    if u'sentence' in text:
                                        if isinstance(text[u'sentence'], dict):
                                            if u'w' in text[u'sentence']:
                                                if isinstance(text[u'sentence'][u'w'], dict):
                                                    if u'val' in text[u'sentence'][u'w']:
                                                        if text[u'sentence'][u'w'][u'val'] in word_stat:
                                                            word_stat[text[u'sentence'][u'w'][u'val']] += 1
                                                        else:
                                                            word_stat[text[u'sentence'][u'w'][u'val']] = 1
                                                else:
                                                    for word in text[u'sentence'][u'w']:
                                                        if u'val' in word:
                                                            if word[u'val'] in word_stat:
                                                                word_stat[word[u'val']] += 1
                                                            else:
                                                                word_stat[word[u'val']] = 1

                                        else:
                                            for sentence in text[u'sentence']:
                                                if u'w' in sentence:
                                                    if isinstance(sentence[u'w'], dict):
                                                        if u'val' in sentence[u'w']:
                                                            if sentence[u'w'][u'val'] in word_stat:
                                                                word_stat[sentence[u'w'][u'val']] += 1
                                                            else:
                                                                word_stat[sentence[u'w'][u'val']] = 1
                                                    else:
                                                        for word in sentence[u'w']:
                                                            if u'val' in word:
                                                                if word[u'val'] in word_stat:
                                                                    word_stat[word[u'val']] += 1
                                                                else:
                                                                    word_stat[word[u'val']] = 1
    while user_stat != {}:
        max_key = max(user_stat.iterkeys(), key=(lambda key: user_stat[key]))
        max_val = user_stat[max_key]
        user_stat_file.write(max_key.encode('utf8')+','+str(max_val)+'\n')
        del user_stat[max_key]

    while hash_stat != {}:
        max_key = max(hash_stat.iterkeys(), key=(lambda key: hash_stat[key]))
        max_val = hash_stat[max_key]
        hash_stat_file.write(max_key.encode('utf8')+','+str(max_val)+'\n')
        del hash_stat[max_key]

    while word_stat != {}:
        max_key = max(word_stat.iterkeys(), key=(lambda key: word_stat[key]))
        max_val = word_stat[max_key]
        word_stat_file.write(max_key.encode('utf8')+','+str(max_val)+'\n')
        del word_stat[max_key]

if __name__ == "__main__":
    #db = thtdb.ThtConnection(collectionName='test_pldebatt_june')
    db = thtdb.ThtConnection(host='squib.de', dbName='karinas_twitter_db', collectionName='import_steffen')
    querries()