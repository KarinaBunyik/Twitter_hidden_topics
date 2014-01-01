# Author: Olivier Grisel <olivier.grisel@ensta.org>
# License: BSD 3 clause

from __future__ import print_function

from time import time
import sys
import os
import numpy as np
import scipy.sparse as sp
import pylab as pl
import random

from sklearn.datasets import load_mlcomp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB


print(__doc__)

if 'MLCOMP_DATASETS_HOME' not in os.environ:
    print("DATASETS_HOME not set; please follow the above instructions")
    sys.exit(0)

# Load the training set
print("Loading twitter training set... ")
twitter_train = load_mlcomp('hashtagging-tweets', 'train')
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

print("Loading twitter test set... ")
news_test = load_mlcomp('hashtagging-tweets', 'test')
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

##################################################
'''
print("Loading twitter prediction set... ")
news_predict = load_mlcomp('hashtagging-tweets', 'predict')
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
                                target_names=news_test.target_names))

    cm = confusion_matrix(y_test, pred)
    print("Confusion matrix:")
    print(cm)

    # Show confusion matrix
    pl.matshow(cm)
    pl.title('Confusion matrix of the %s classifier' % name)
    pl.colorbar()


def benchmark_prediction(clf_class, params, name):
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
    print("Second label predicted ", len(pred_list)), " times"
    for i in range(19):
        print(news_predict.filenames[i], ' :: ', pred_list[i])
        pass

    print("done in %fs" % (time() - t0))


print("Testbenching a linear classifier...")
parameters = {
    'loss': 'hinge',
    'penalty': 'l2',
    'n_iter': 50,
    'alpha': 0.00001,
    'fit_intercept': True,
}

benchmark(SGDClassifier, parameters, 'SGD')

#benchmark_prediction(SGDClassifier, parameters, 'SGD')

#print("Testbenching a MultinomialNB classifier...")
#parameters = {'alpha': 0.01}

#benchmark(MultinomialNB, parameters, 'MultinomialNB')

#pl.show()