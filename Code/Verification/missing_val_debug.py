import thtdb


def calcu():
    interesting_user_ids = []
    for user in db.collection.find():
        if u'text' in user:
            for text in user[u'text']:
                if u'sentence' in text:
                    for sentence in text[u'sentence']:
                        if u'w' in sentence:
                            for word in sentence[u'w']:
                                if u'val' in word:
                                    if word[u'val'] is not None:
                                        pass
                                else:
                                    raise NameError('No val')
                        else:
                            interesting_user_ids.append(user[u'_id'])
                            print interesting_user_ids
                            raise NameError('No word')
                else:
                    raise NameError('No sentence')
        else:
            raise NameError('No text')

db = thtdb.ThtConnection(host='squib.de', dbName='karinas_twitter_db', collectionName='twitter-pldebatt-131006')
calcu()