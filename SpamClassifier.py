#!/usr/bin/env python

from __future__ import division
import sys
import os
import random
import time
import itertools

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
        for word in self.vocabulary:
            for doc_class in self.classes:
                if doc_class not in self.vocabulary[word]:
                    self.vocabulary[word][doc_class] = 0;
                self.vocabulary[word][doc_class] = (self.vocabulary[word][doc_class] + 1)/(self.words_num[doc_class] + voc_size)


    def learn(self, database):
        self.parse_database(database)
        self.compute_probabilities()
        #print self.vocabulary

    def classify(self, doc):
        words = filter(lambda w: w in self.vocabulary,doc.split(' '))
        if not words:
            return self.classes.keys()[int(random.random())]
        hypotesys = 0
        max_prob = -1
        for doc_class in self.classes:
            prob = self.classes[doc_class]* reduce((lambda x,y: x * y), map(lambda w: self.vocabulary[w][doc_class], words))
            if prob > max_prob:
                max_prob = prob
                hypotesys = doc_class
        return hypotesys

def k_fold_cross_validation(data, k):
    #partitioning data
    size = len(data)
    datasets = []
    for i in range(k):
        datasets.append([])
    random.seed(time.time())
    while data:
        i = int(random.random()*k)
        datasets[i].append(data.pop())

    accuracy = 0
    for i in range(k):
        correct = 0
        done = 0

        training = itertools.chain.from_iterable([datasets[j] for j in filter(lambda j: j != i, range(k))])
        testing = datasets[i]
        spam = SpamClassifier()
        spam.learn(training)
        for test in testing:
            done += 1
            expected = test.split('\t')[0]
            doc = test.split('\t')[1].strip()
            if spam.classify(doc) == expected:
                correct += 1
        accuracy += (correct / done)
        sys.stdout.write('\r|'+('='*i)+('  '*(k-i-1)+'|'))
        sys.stdout.flush()

    print '\n[+] K-Fold accuracy:', accuracy / k







def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: %s database-name' % sys.argv[0])

    if not os.path.exists(sys.argv[1]):
        sys.exit('ERROR: Database %s was not found!' % sys.argv[1])

    database = open(sys.argv[1],'r').readlines()
    #print database.readlines()

    k_fold_cross_validation(database, 100)

    #spam.learn(database)
    #doc = 'I\'m gonna be hhome soon and i don\'t want you and me to talk about you and this stuff anymore tonight, k? I\'ve cried enough todayyyyyyyy.'
    #print spam.classify(doc)



if __name__ == "__main__":
    main()
