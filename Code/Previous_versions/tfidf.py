#!/usr/bin/env python
# 
# Copyright 2009  Niniane Wang (niniane@gmail.com)
# Reviewed by Alex Mendes da Costa.
#
# This is a simple Tf-idf library.  The algorithm is described in
#   http://en.wikipedia.org/wiki/Tf-idf
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# Tfidf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details:
#
#   http://www.gnu.org/licenses/lgpl.txt

__author__ = "Niniane Wang"
__email__ = "niniane at gmail dot com"

from thtpaths import internal_path
import math
import re
import io
import codecs
from operator import itemgetter


def saveToFile(word_list, filename, dirname):
        file_path = internal_path+dirname+'/'
        #user_words_filename = internal_path+'/malletTwitterOctober/'+username
        ofile = io.open(file_path+filename+'.txt', 'wb')
        #ofile = codecs.open(file_path+filename+'.txt','w','utf-8')
        for word in word_list:
            if word is not None:
                #ofile.write(word[0]+' ')
                ofile.write(word[0].encode('utf8') +' ')
                ofile.write(str(word[1])+'\n')
                #ofile.write(unicode(word[1]))
        ofile.close()



class TfIdf:

  """Tf-idf class implementing http://en.wikipedia.org/wiki/Tf-idf.
  
     The library constructs an IDF corpus and stopword list either from
     documents specified by the client, or by reading from input files.  It
     computes IDF for a specified term based on the corpus, or generates
     keywords ordered by tf-idf for a specified document.
  """

  def __init__(self, corpus_filename = None, stopword_filename = None,
               DEFAULT_IDF = 1.5):
    """Initialize the idf dictionary.  
    
       If a corpus file is supplied, reads the idf dictionary from it, in the
       format of:
         # of total documents
         term: # of documents containing the term

       If a stopword file is specified, reads the stopword list from it, in
       the format of one stopword per line.

       The DEFAULT_IDF value is returned when a query term is not found in the
       idf corpus.
    """
    self.num_docs = 0
    self.term_num_docs = {}     # term : num_docs_containing_term
    self.stopwords = []
    self.idf_default = DEFAULT_IDF

    if corpus_filename:
      corpus_file = open(corpus_filename, "r")

      # Load number of documents.
      line = corpus_file.readline()
      self.num_docs = int(line.strip())

      # Reads "term:frequency" from each subsequent line in the file.
      for line in corpus_file:
       tokens = line.split(":")
       term = tokens[0].strip()
       frequency = int(tokens[1].strip())
       self.term_num_docs[term] = frequency

    if stopword_filename:
      stopword_file = open(stopword_filename, "r")
      self.stopwords = [line.strip() for line in stopword_file]

  def get_tokens(self, str):
    """Break a string into tokens, preserving URL tags as an entire token.

       This implementation does not preserve case.  
       Clients may wish to override this behavior with their own tokenization.
    """
    return re.findall(r"<a.*?/a>|<[^\>]*>|[\w'@#]+", str.lower())

  def add_input_document(self, input):
    """Add terms in the specified document to the idf dictionary."""
    self.num_docs += 1
    words = set(self.get_tokens(input))
    for word in words:
      if word in self.term_num_docs:
        self.term_num_docs[word] += 1
      else:
        self.term_num_docs[word] = 1

  def save_corpus_to_file(self, idf_filename, stopword_filename,
                          STOPWORD_PERCENTAGE_THRESHOLD = 0.01):
    """Save the idf dictionary and stopword list to the specified file."""
    output_file = open(idf_filename, "w")

    output_file.write(str(self.num_docs) + "\n")
    for term, num_docs in self.term_num_docs.items():
      output_file.write(term + ": " + str(num_docs) + "\n")

    sorted_terms = sorted(self.term_num_docs.items(), key=itemgetter(1),
                          reverse=True)
    stopword_file = open(stopword_filename, "w")
    for term, num_docs in sorted_terms:
      if num_docs < STOPWORD_PERCENTAGE_THRESHOLD * self.num_docs:
        break

      stopword_file.write(term + "\n")

  def get_num_docs(self):
    """Return the total number of documents in the IDF corpus."""
    return self.num_docs

  def get_idf(self, term):
    """Retrieve the IDF for the specified term. 
    
       This is computed by taking the logarithm of ( 
       (number of documents in corpus) divided by (number of documents
        containing this term) ).
     """
    if term in self.stopwords:
      return 0

    if not term in self.term_num_docs:
      return self.idf_default

    return math.log(float(1 + self.get_num_docs()) / 
      (1 + self.term_num_docs[term]))

  def get_doc_keywords(self, curr_doc):
    """Retrieve terms and corresponding tf-idf for the specified document.

       The returned terms are ordered by decreasing tf-idf.
    """
    tfidf = {}
    tokens = self.get_tokens(curr_doc)
    tokens_set = set(tokens)
    for word in tokens_set:
      mytf = float(tokens.count(word)) / len(tokens_set)
      myidf = self.get_idf(word)
      tfidf[word] = mytf * myidf

    return sorted(tfidf.items(), key=itemgetter(1), reverse=True)

tfidf_1 = TfIdf()
#print tfidf
crimeFile = io.open(internal_path+'tfidf/'+'crime'+'.txt', 'r')
schoolFile = io.open(internal_path+'tfidf/'+'school'+'.txt', 'r')
climateFile = io.open(internal_path+'tfidf/'+'climate'+'.txt', 'r')
taxFile = io.open(internal_path+'tfidf/'+'tax'+'.txt', 'r')
#immigrationFile = io.open(internal_path+'tfidf/'+'immigration'+'.txt', 'r')
#healthFile = io.open(internal_path+'tfidf/'+'health'+'.txt', 'r')

print 'adding crime to corpus...'
tfidf_1.add_input_document(crimeFile.read())
print 'crime in corpus.'
print 'adding school to corpus...'
tfidf_1.add_input_document(schoolFile.read())
print 'school in corpus.'
print 'adding climate to corpus...'
tfidf_1.add_input_document(climateFile.read())
print 'climate in corpus.'
print 'adding tax to corpus...'
tfidf_1.add_input_document(taxFile.read())
print 'tax in corpus.'
print 'No of documents: ', tfidf_1.num_docs
print 'term num docs: ', len(tfidf_1.term_num_docs)
#print 'adding immigration to corpus...'
#tfidf.add_input_document(immigrationFile.read())
#print 'immigration in corpus.'
#print 'adding health to corpus...'
#tfidf.add_input_document(healthFile.read())
#print 'health in corpus.'


crimeFile.close()
schoolFile.close()
climateFile.close()
taxFile.close()



crimeFile = io.open(internal_path+'tfidf/'+'crime'+'.txt', 'r')
schoolFile = io.open(internal_path+'tfidf/'+'school'+'.txt', 'r')
climateFile = io.open(internal_path+'tfidf/'+'climate'+'.txt', 'r')
taxFile = io.open(internal_path+'tfidf/'+'tax'+'.txt', 'r')

print 'calculation crime tf-idf...'
saveToFile(tfidf_1.get_doc_keywords(crimeFile.read()), 'crime_out', 'tfidf')
print 'crime tf-idf done.'
print 'calculating school tf-idf...'
#saveToFile(tfidf_1.get_doc_keywords(schoolFile .read()), 'school_out', 'tfidf')
print 'school tf-idf done.'
print 'calculating climate tf-idf...'
#saveToFile(tfidf_1.get_doc_keywords(climateFile.read()), 'climate_out', 'tfidf')
print 'climate tf-idf done.'
print 'calculating tax tf-idf...'
#saveToFile(tfidf_1.get_doc_keywords(taxFile.read()), 'tax_out', 'tfidf')
print 'tax tf-idf done.'

#print 'calculating immigration tf-idf...'
#tfidf.get_doc_keywords(immigrationFile.read())
#print 'immigration tf-idf done.'
#print 'calculating health tf-idf...'
#tfidf.get_doc_keywords(healthFile.read())
#print 'health tf-idf done.'
