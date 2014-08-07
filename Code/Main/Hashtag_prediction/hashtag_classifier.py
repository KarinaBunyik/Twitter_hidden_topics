<<<<<<< HEAD
# -*- coding: UTF-8 -*-    
=======
<<<<<<< HEAD
# -*- coding: UTF-8 -*-    
=======
>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d
>>>>>>> b2fc47e05158e187ff5a4ff4374d7fee030fc416
# Author: Olivier Grisel <olivier.grisel@ensta.org>
# License: BSD 3 clause

from __future__ import print_function

<<<<<<< HEAD
import thtdb
=======
<<<<<<< HEAD
import thtdb
=======
>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d
>>>>>>> b2fc47e05158e187ff5a4ff4374d7fee030fc416
from time import time
import sys
import os
import io
import numpy as np
import scipy.sparse as sp
import pylab as pl
from thtpaths import internal_path
import matplotlib.pyplot as plt
<<<<<<< HEAD
import random
import re
=======
<<<<<<< HEAD
import random
import re
=======
>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d
>>>>>>> b2fc47e05158e187ff5a4ff4374d7fee030fc416

from sklearn.datasets import load_mlcomp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
<<<<<<< HEAD
from sklearn import svm
from sklearn import tree
=======
<<<<<<< HEAD
from sklearn import svm
from sklearn import tree
=======
>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d
>>>>>>> b2fc47e05158e187ff5a4ff4374d7fee030fc416
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
#from sklearn.naive_bayes import MultinomialNB


<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b2fc47e05158e187ff5a4ff4374d7fee030fc416
global pldebatt_list
global other_list
global predict_list



def fileToList(filename):
        word_list = []
        ifile = io.open(internal_path+filename+'.txt', 'r')
        for word in ifile:
            word_list.append(word.replace('\n',''))
        ifile.close()
        return word_list


def saveToDir(word_list, filename, dirname):
        dirname = dirname+'/'
        ofile = io.open(dirname+filename, 'wb')
        for word in word_list:
            if word is not None:
                ofile.wr


#training example. #pldebatt hastag is positive example, other hashtags are negative examples. No hashtag tweets are
#to be predicted. The hashtags are taken away from the tweets. The positive hashtags end up in a separate folder
# called "pldebatt", the negative in "other" folder. "raw" folder contains all labeled samples without train-test split.
def saveWordsPerTweetByHashtag(folder, minimal_tweet_length, with_spec_char):
    element_counter = 0

    political_context = fileToList('domain_word_list')
    p = re.compile("[A-Za-z0-9\såäöÅÖÄ:-]+$", re.UNICODE)
    for user in db.collection.find():
        element_counter += 1
        if element_counter % 1000 == 0:
            print("Number of users processed: ", element_counter)
            print("Number of users processed: ", pldebatt_list)
            print("Number of users processed: ", other_list)
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
                            #test_train_division = random.random()
                            pldebatt_list.append({'tweet': ' '.join(tweet_words), 'id': tweet_id})
                            #if test_train_division <0.2:
                            #    saveToDir(tweet_words, tweet_id, test_folder+pldebatt_folder)
                            #else:
                            #    saveToDir(tweet_words, tweet_id, train_folder+pldebatt_folder)  
                    elif (not is_word_politics):
                        if len(tweet_words)>=minimal_tweet_length:
                            #saveToDir(tweet_words, tweet_id, predict_folder)
                            sampling_probability = random.random()
                            if sampling_probability <= 0.03:
                                other_list.append({'tweet': ' '.join(tweet_words), 'id': tweet_id})
                            else:
                                predict_list.append({'tweet': ' '.join(tweet_words), 'id': tweet_id})
                            #saveToDir(tweet_words, tweet_id, all_folder+nonpldebatt_folder)
                                #test_train_division = random.random()
                                #if test_train_division <0.2:
                                #    saveToDir(tweet_words, tweet_id, test_folder+nonpldebatt_folder)
                                #else:
                                #    saveToDir(tweet_words, tweet_id, train_folder+nonpldebatt_folder)
                            #elif text[u'hashtags']==u'|':
                                # tweets with no political words and hashtags, and having NO other hashtag
                                #saveToDir(tweet_words, tweet_id, predict_folder)
                                #pass
                                # tweets with no political words and hashtags, but having some other hashtags
                    else:
                        # tweets with a political word, but without a political hashtag
                        if len(tweet_words)>=minimal_tweet_length:
                            predict_list.append({'tweet': ' '.join(tweet_words), 'id': tweet_id})
                else:
                    raise NameError('Obligationary "hashtags" attribute missing in data!')


<<<<<<< HEAD
=======
=======
>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d
>>>>>>> b2fc47e05158e187ff5a4ff4374d7fee030fc416
def saveToFile(word_list, filename, dirname):
        file_path = internal_path+dirname+'/'
        #user_words_filename = internal_path+'/malletTwitterOctober/'+username
        ofile = io.open(file_path+filename+'.txt', 'wb')
        for word in word_list:
            if word is not None:
                ofile.write(str(word)+'\n')
        ofile.close()


def removePath(filename, dirname):
        word_list = []
        ifile = io.open(internal_path+dirname+'/'+filename+'.txt', 'r')
        for word in ifile:
            word_list.append(word[len(word)-19:len(word)-1])
            #word_list.append(word.replace('\n',''))
        ifile.close()
        return word_list

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b2fc47e05158e187ff5a4ff4374d7fee030fc416

print(__doc__)

db = thtdb.ThtConnection(dbName='tweets_by_users_test', collectionName='twitter-pldebatt-medium')

pldebatt_list = []
predict_list = []
other_list = []

saveWordsPerTweetByHashtag('20w_spec_may', 20, True)

saveToDir(pldebatt_list,internal_path+'hashtagPrediction','pldebatt_list')
saveToDir(pldebatt_list,internal_path+'hashtagPrediction','other_list')
saveToDir(pldebatt_list,internal_path+'hashtagPrediction','pldebatt_list')


#if 'MLCOMP_DATASETS_HOME' not in os.environ:
#    print("DATASETS_HOME not set; please follow the above instructions")
#    sys.exit(0)

# Load the training set
#dataset_name = '20w_nospec_may'
#print("Loading twitter training set... ")
#twitter_train = load_mlcomp(dataset_name, 'train')
#print(twitter_train.DESCR)
#print("%d documents" % len(twitter_train.filenames))
#print("%d categories" % len(twitter_train.target_names))

#print("Extracting features from the dataset using a sparse vectorizer")
#t0 = time()



vectorizer = TfidfVectorizer(encoding='latin1')
#X_train = vectorizer.fit_transform((open(f).read()
#                                    for f in twitter_train.filenames))
X_train = vectorizer.fit_transform(line['tweet'] for line in (pldebatt_list + other_list))
#for f in twitter_train.filenames:
#    print(open(f).read())
#print("done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X_train.shape)
assert sp.issparse(X_train)
#y_train = twitter_train.target
y_train = [1] * len(pldebatt_list) + [0] * len(other_list)
#print(twitter_train.target)

X_test = vectorizer.fit_transform(line['tweet'] for line in (pldebatt_list + other_list))
#for f in twitter_train.filenames:
#    print(open(f).read())
#print("done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X_test.shape)
assert sp.issparse(X_test)
#y_train = twitter_train.target
y_test = [1] * len(pldebatt_list) + [0] * len(other_list)
#print(twitter_train.target)

##################################################
'''
<<<<<<< HEAD
=======
=======
print(__doc__)

if 'MLCOMP_DATASETS_HOME' not in os.environ:
    print("DATASETS_HOME not set; please follow the above instructions")
    sys.exit(0)

# Load the training set
dataset_name = 'hashtagging-tweets-linn-0words-nospecchar'
print("Loading twitter training set... ")
twitter_train = load_mlcomp(dataset_name, 'train')
print(twitter_train.DESCR)
print("%d documents" % len(twitter_train.filenames))
print("%d categories" % len(twitter_train.target_names))

print("Extracting features from the dataset using a sparse vectorizer")
t0 = time()
vectorizer = TfidfVectorizer(encoding='latin1')
X_train = vectorizer.fit_transform((open(f).read()
                                    for f in twitter_train.filenames))
print("done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X_train.shape)
assert sp.issparse(X_train)
y_train = twitter_train.target

##################################################

>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d
>>>>>>> b2fc47e05158e187ff5a4ff4374d7fee030fc416
print("Loading twitter test set... ")
news_test = load_mlcomp(dataset_name, 'test')
t0 = time()
print("done in %fs" % (time() - t0))

print("Predicting the labels of the test set...")
print("%d documents" % len(news_test.filenames))
print("%d categories" % len(news_test.target_names))

print("Extracting features from the dataset using the same vectorizer")
t0 = time()
X_test = vectorizer.transform((open(f).read() for f in news_test.filenames))
y_test = news_test.target
print("done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X_test.shape)
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b2fc47e05158e187ff5a4ff4374d7fee030fc416
'''
##################################################
'''


<<<<<<< HEAD
=======
=======

##################################################


'''
>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d
>>>>>>> b2fc47e05158e187ff5a4ff4374d7fee030fc416
print("Loading twitter prediction set... ")
news_predict = load_mlcomp(dataset_name, 'predict')
t0 = time()
print("done in %fs" % (time() - t0))

print("Predicting the labels of the test set...")
print("%d documents" % len(news_predict.filenames))

print("Extracting features from the dataset using the same vectorizer")
t0 = time()
X_predict = vectorizer.transform((open(f).read() for f in news_predict.filenames))
#y_predict = news_test.target
print("done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X_predict.shape)
'''

###############################################################################
# Benchmark classifiers
def benchmark(clf_class, params, name):
    print("parameters:", params)
    t0 = time()
    clf = clf_class(**params).fit(X_train, y_train)
    print("done in %fs" % (time() - t0))

    if hasattr(clf, 'coef_'):
        print("Percentage of non zeros coef: %f"
              % (np.mean(clf.coef_ != 0) * 100))
    print("Predicting the outcomes of the testing set")
    t0 = time()
    pred = clf.predict(X_test)
    print("done in %fs" % (time() - t0))

    print("Classification report on test set for classifier:")
    print(clf)
    print()
    print(classification_report(y_test, pred,
<<<<<<< HEAD
                                target_names=['pldebatt', 'other']))
=======
<<<<<<< HEAD
                                target_names=['pldebatt', 'other']))
=======
                                target_names=news_test.target_names))
>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d
>>>>>>> b2fc47e05158e187ff5a4ff4374d7fee030fc416

    cm = confusion_matrix(y_test, pred)
    print("Confusion matrix:")
    print(cm)
    #cm = metrics.confusion_matrix(expected, predicted)
    plt.matshow(cm)
    plt.title('Confusion matrix')
    plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()

    # Show confusion matrix
    pl.matshow(cm)
    pl.title('Confusion matrix of the %s classifier' % name)
    pl.colorbar()


def benchmark_prediction(
    clf_class, params, name):
    print("parameters:", params)
    t0 = time()
    clf = clf_class(**params).fit(X_train, y_train)
    print("done in %fs" % (time() - t0))

    if hasattr(clf, 'coef_'):
        print("Percentage of non zeros coef: %f"
              % (np.mean(clf.coef_ != 0) * 100))
    print("Predicting the outcomes of the prediction set")
    t0 = time()

    pred = clf.predict(X_predict)
    print(type(X_predict))
    pred_list = pred.tolist()
    print("First label predicted ", len(pred_list) - sum(pred_list)), " times."
    print("Second label predicted ", sum(pred_list)), " times"
    pred_id_list = []
    for i in range(len(pred_list)):
        if pred_list[i] == 1:
            pred_id_list.append(news_predict.filenames[i])
        pass

    print("done in %fs" % (time() - t0))
    saveToFile(pred_id_list, 'predicted_tweets', 'hashtagPrediction')
    a = removePath('predicted_tweets', 'hashtagPrediction')
    print(len(a))
    saveToFile(a, 'predicted_tweet_ids', 'hashtagPrediction')


print("Testbenching a linear classifier...")
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b2fc47e05158e187ff5a4ff4374d7fee030fc416

parameters = {
    'loss': 'hinge',
    'penalty': 'elasticnet',
<<<<<<< HEAD
=======
=======
parameters = {
    'loss': 'hinge',
    'penalty': 'l2',
>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d
>>>>>>> b2fc47e05158e187ff5a4ff4374d7fee030fc416
    'n_iter': 50,
    'alpha': 0.00001,
    'fit_intercept': True,
}
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b2fc47e05158e187ff5a4ff4374d7fee030fc416
'''
parameters = {
    'degree': 3,
    'gamma': 0.0, 
    'kernel': 'rbf', 
    'max_iter': -1,
    'probability': False,
    'random_state': None,
    'shrinking': True, 
    'tol': 0.001
}

parameters = {
    'penalty': 'l1', 
    'loss': 'l2', 
    'dual': False, 
    'tol': 0.00001, 
    'C': 1.0, 
    'multi_class':'ovr', 
    'fit_intercept': True,
    'intercept_scaling': 1, 
    'verbose': 1
    }

parameters = {
    'criterion': 'gini', 
    'splitter': 'best', 
    'max_depth': None, 
    'min_samples_split': 2, 
    'min_samples_leaf': 1,
    'max_features': None,
    'random_state': None,
    'min_density': None, 
    'compute_importances': None
    }
'''
benchmark(SGDClassifier, parameters, 'SGD') 


#benchmark(svm.SVC, parameters, 'SVC')
#benchmark(svm.LinearSVC, parameters, 'LinearSVC')
#benchmark(tree.DecisionTreeClassifier, parameters, 'DecisionTree')
<<<<<<< HEAD
=======
=======

benchmark(SGDClassifier, parameters, 'SGD')
>>>>>>> 8f45800ea1947d1682d24928447c45c54826984d
>>>>>>> b2fc47e05158e187ff5a4ff4374d7fee030fc416

#benchmark_prediction(SGDClassifier, parameters, 'SGD')

#print("Testbenching a MultinomialNB classifier...")
#parameters = {'alpha': 0.01}

#benchmark(MultinomialNB, parameters, 'MultinomialNB')

#pl.show()