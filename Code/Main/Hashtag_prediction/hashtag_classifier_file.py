# -*- coding: UTF-8 -*-    
# Author: Olivier Grisel <olivier.grisel@ensta.org>
# License: BSD 3 clause

from __future__ import print_function

import thtdb
from time import time
import sys
import os
import io
import numpy as np
import scipy.sparse as sp
import pylab as pl
from thtpaths import internal_path
import matplotlib.pyplot as plt
import random
import re

from sklearn.datasets import load_mlcomp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn import svm
from sklearn import tree
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
#from sklearn.naive_bayes import MultinomialNB


print(__doc__)

#if 'MLCOMP_DATASETS_HOME' not in os.environ:
#    print("DATASETS_HOME not set; please follow the above instructions")
#    sys.exit(0)

 #Load the training set
dataset_name = '20w_nospec_may'
print("Loading twitter training set... ")
twitter_train = load_mlcomp(dataset_name, 'train')
print(twitter_train.DESCR)
print("%d documents" % len(twitter_train.filenames))
print("%d categories" % len(twitter_train.target_names))


print("Extracting features from the dataset using a sparse vectorizer")
t0 = time()

vectorizer = TfidfVectorizer(encoding='latin1')

X_train = vectorizer.fit_transform((open(f).read() for f in twitter_train.filenames))
print("done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X_train.shape)
assert sp.issparse(X_train)
y_train = twitter_train.target
print(twitter_train.target)


print("Loading twitter test set... ")
twitter_test = load_mlcomp(dataset_name, 'test')
t0 = time()
print("done in %fs" % (time() - t0))

print("Predicting the labels of the test set...")
print("%d documents" % len(twitter_test.filenames))
print("%d categories" % len(twitter_test.target_names))

print("Extracting features from the dataset using the same vectorizer")
t0 = time()
X_test = vectorizer.transform((open(f).read() for f in twitter_test.filenames))
y_test = twitter_test.target
print("done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X_test.shape)


##################################################
'''
print("Loading twitter test set... ")
twitter_test = load_mlcomp(dataset_name, 'test')
t0 = time()
print("done in %fs" % (time() - t0))

print("Predicting the labels of the test set...")
print("%d documents" % len(twitter_test.filenames))
print("%d categories" % len(twitter_test.target_names))

print("Extracting features from the dataset using the same vectorizer")
t0 = time()
X_test = vectorizer.transform((open(f).read() for f in twitter_test.filenames))
y_test = twitter_test.target
print("done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X_test.shape)
'''
##################################################
'''


print("Loading twitter prediction set... ")
twitter_predict = load_mlcomp(dataset_name, 'predict')
t0 = time()
print("done in %fs" % (time() - t0))

print("Predicting the labels of the test set...")
print("%d documents" % len(twitter_predict.filenames))

print("Extracting features from the dataset using the same vectorizer")
t0 = time()
X_predict = vectorizer.transform((open(f).read() for f in twitter_predict.filenames))
#y_predict = twitter_test.target
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
                                target_names=['pldebatt', 'other']))

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
            pred_id_list.append(twitter_predict.filenames[i])
        pass

    print("done in %fs" % (time() - t0))
    saveToFile(pred_id_list, 'predicted_tweets', 'hashtagPrediction')
    a = removePath('predicted_tweets', 'hashtagPrediction')
    print(len(a))
    saveToFile(a, 'predicted_tweet_ids', 'hashtagPrediction')


print("Testbenching a linear classifier...")

parameters = {
    'loss': 'hinge',
    'penalty': 'elasticnet',
    'n_iter': 50,
    'alpha': 0.00001,
    'fit_intercept': True,
}
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

#benchmark_prediction(SGDClassifier, parameters, 'SGD')

#print("Testbenching a MultinomialNB classifier...")
#parameters = {'alpha': 0.01}

#benchmark(MultinomialNB, parameters, 'MultinomialNB')

#pl.show()