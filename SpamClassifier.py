#!/usr/bin/env python

from __future__ import division
import sys
import os

class SpamClassifier(object):

    '''
    self.vocabulary = map of all words -> num of occurrences in each class (map class->num)
    self.classes = map class->probability of that class
    self.docs = map class->docs of that class
    self.words_num = map class->num of words in that class
    '''
    def __init__(self):
        self.vocabulary = {}
        self.classes = {}
        self.docs = {}
        self.words_num = {}

    '''
    Initializes vocabulary, classes, docs by classes
    '''
    def parse_database(self, database):

        for line in database:
            doc_class = line.split('\t')[0]
            doc = line.split('\t')[1].strip()
            words = doc.split(' ')

            if doc_class not in self.docs:
                #init set of classes
                self.docs[doc_class] = set()
                self.words_num[doc_class] = 0

            if doc not in self.docs[doc_class]:
                self.docs[doc_class].add(doc)
                self.words_num[doc_class]+= len(words)

                #init vocabulary counting word seen for each class
                for word in words:
                    if word.strip() not in self.vocabulary:
                        self.vocabulary[word.strip()] = {}
                    if doc_class not in self.vocabulary[word.strip()]:
                        self.vocabulary[word.strip()][doc_class] = 0
                    self.vocabulary[word.strip()][doc_class] += 1


    def compute_probabilities(self):

        #prob of a class
        num_lines = 0
        for doc_class in self.docs:
            l = len(self.docs[doc_class])
            num_lines += l
            self.classes[doc_class] = l

        #prob = docs / total docs num
        for doc_class in self.classes:
            self.classes[doc_class] /= num_lines

        #compute probability of a word to be in a class
        voc_size = len(self.vocabulary)
        for 






    def learn(self, database):
        self.parse_database(database)
        self.compute_probabilities()
        print self.vocabulary








def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: %s database-name' % sys.argv[0])

    if not os.path.exists(sys.argv[1]):
        sys.exit('ERROR: Database %s was not found!' % sys.argv[1])

    spam = SpamClassifier()

    database = open(sys.argv[1],'r').readlines()
    #print database.readlines()

    spam.learn(database)



if __name__ == "__main__":
    main()
