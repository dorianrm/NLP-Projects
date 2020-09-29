"""
CS124 PA3: Sentiment // Stanford, Winter 2019
by @chumak
"""

# Gradescope: 60/60

import sys
import getopt
import os
import math
import operator
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

class LogisticRegression:
    class Splitter:
        """Represents a set of training/testing data. self.train is a list of Examples, as is self.dev. 
        """
        def __init__(self):
            self.train = []
            self.dev = []
            self.test = []

    class Example:
        """Represents a document with a label. klass is 1 if 'pos' and 0 if 'neg' by convention.
           words is a string (a single movie review).
        """
        def __init__(self):
            self.klass = -1
            self.words = ''

    def __init__(self):
        """Logistic Regression initialization"""
        self.INCLUDE_LEXICON  = False
        self.stopList = set(self.readFile(os.path.join('data', 'english.stop')))
        self.posWords = set() # positive opinion lexicon obtained from http://web.stanford.edu/class/cs124/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt
        self.negWords = set() # negative opinion lexicon
        self.vect = CountVectorizer(min_df=20, ngram_range=(1, 1)) 

        
        self.X = [] #input values
        self.Y = [] #true labels
        self.weight = [] #weight vector
        self.b = 0 #bias
        #TODO: add other data structures needed in the functions you implement below

    #############################################################################
    # TODO TODO TODO TODO TODO 
    # Implement a logistic regression model to classify movie review sentiment as either
    # positive or negative using logistic regression.
    #
    # If the INCLUDE_LEXICON  flag is true, add two more features to our Logistic Regression model
    # Feature 1: the total number of positive words in a review
    # Feature 2: the total number of negative words in a review.
    # We have already preprocessed the NRC emotion lexicon for you,
    # and you can access the set of lexicon words in self.posWords and self.negWords. 
    # We have also provided the function addFeatures() that takes in the original feature matrix X 
    # and a list of lists as the second argument; each list element is a feature vector for one input. 
    # This allows the logistic regression model to include your own features along with those from CountVectorizer()


    """ Implement a function to train a logistic regression model.
        Use vectors self.X to store your inputs and self.Y your labels.
        self.vect is a countVectorizer we have created for you. Use it
        to obtain a unigram feature vector for your training data.
        Documentation: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
        It creates a sparse matrix containing counts of words in each
        review keeping only those that appear more times than the set threshold(20).
        
        Arguments:
        trainData -- the training data which a list of examples (see class Example: above to see how it's 
        initialized and what its members are). Each example is a single review and its true class.
    """
    def train(self, trainData):
        ### Start your code here 
        # HINT: Call self.X.todense()  after you've populated self.X with counts. 
        # This converts it from a sparse matrix to a dense matrix so
        # we can use it to perform gradient descent.
        #
        # HINT: You can use self.addFeatures to add more features.
        # The first argument should be self.X and the second 
        # a list of lists. Each list is a feature vector for one document.
        #
        # HINT: Use np.zeros() to initialize self.weight to zeros
        #
        # HINT: Call self.gradientDescent to train your model

        # ---------
        train_x = []
        pos = []
        neg = [] 
        cPos = 0
        cNeg = 0
        for example in trainData:
            train_x.append(example.words)
            self.Y.append(example.klass)

            if self.INCLUDE_LEXICON == True:
                for word in example.words.split():
                    if word in self.posWords:
                        cPos += 1
                    if word in self.negWords:
                        cNeg += 1
                pos.append([cPos])
                neg.append([cNeg])
                cPos = 0
                cNeg = 0


        self.X = self.vect.fit_transform(train_x)
        self.X = self.X.todense()
        if self.INCLUDE_LEXICON == True:
            self.X = self.addFeatures(self.X, pos)
            self.X = self.addFeatures(self.X, neg)

        self.weight = np.zeros((self.X.shape[1], 1))

        self.gradientDescent()
        ###End your code here

    
    """
    Compute the sigmoid function for the input here.
    Arguments:
    x -- A scalar or numpy array.
    Return:
    s - sigmoid(x)
    HINT: use np.exp() because your input can be a numpy array
    """
    def sigmoid(self, x):
        ### START YOUR CODE HERE
        return 1/(1 + np.exp(-x))
        ### END YOUR CODE HERE
        
    """
    Predict what class an input belongs to based on its score.
    If sigmoid(X.W+b) is greater or equal to 0.5, it belongs to
    class 1 (positive class) otherwise, it belongs to class 0
    (negative class). Use the sigmoid function you implemented above.
    HINT: Use self.weight to get W and self.b to get b
    HINT: You can use np.dot to calculate the dot product of arrays
    Arguments:
    x -- A scalar or numpy array.
    Return:
    k -- the predicted class
    """
    def predict(self, x):
        assert x.shape[0] == 1, "x has the wrong shape. Expected a row vector, got: "+str(x.shape)
        ### Start your code here
        value = self.sigmoid(np.dot(x,self.weight)+self.b)
        if value >= 0.5:
            return 1
        else:
            return 0
        ### End your code here

    """
    Classify a string of words as either positive (klass =1) or negative (klass =0)
    Hint: Use the self.predict class you implemented above
    Hint: Use self.vect to get a unigram feature vector
    Hint: self.predict takes a row vector as an argument
    Hint: self.vect.transform() takes a list of strings as inputs
    Arguments:
    words -- A string of words (a single movie review)
    Return:
    k - the predicted class. 1 = positive. 0 = negative
    """
    def classify(self, words):
        ## Start your code here
        temp = []
        temp.append(words)
        vec = self.vect.transform(temp)
        vec = vec.todense()

        if self.INCLUDE_LEXICON == True:
            cPos = 0
            cNeg = 0
            pos = []
            neg = []
            for word in words.split():
                if word in self.posWords:
                    cPos += 1
                if word in self.negWords:
                    cNeg += 1
            pos.append([cPos])
            neg.append([cNeg])
            vec = self.addFeatures(vec, pos)
            vec = self.addFeatures(vec, neg)

        return self.predict(vec)
        ###End your code here

# END TODO(Modify code beyond here with caution)#######################################################################################
     ## Adds features to self.X by concatenating the unigram matrix with features
    def addFeatures(self, feature1, feature2):
        assert feature1.shape[0] == len(feature2), "features have mismatched shape"
        return np.concatenate((feature1, np.array(feature2)), axis = 1)

    ## Loss function used for logistic regression
    def loss(self, a, y):
        return (-1/y.shape[0])*(np.dot(y.T,(np.log(a))) + np.dot((1-y).T,(np.log(1-a))))

    def gradientDescent(self, alpha=0.001, numiters=1000):
        self.Y = np.array(self.Y).reshape((-1,1))
        loss = 0
        for i in range(numiters):
            Z = np.dot(self.X, self.weight)+self.b
            A = self.sigmoid(Z)
            grad = np.dot(self.X.T, (A - self.Y)) / self.Y.shape[0]
            db = np.sum(A - self.Y)/ self.Y.shape[0]
            self.weight -= alpha*grad
            self.b -= alpha*db
            prevLoss = loss
            loss = self.loss(A, self.Y)
            stepSize = abs(prevLoss - loss)

            if stepSize[0,0] < 0.000001:
                break 

            if(i % 500 == 0):
                z = np.dot(self.X, self.weight)+self.b
                a = self.sigmoid(z)
                print("loss:" + str(np.squeeze(np.array(self.loss(a, self.Y)))) +"\t %d/%d iterations" % (i, numiters))
    

    def readFile(self, fileName):
        contents = []
        f = open(fileName, encoding='latin-1')
        contents = f.read()
        f.close()
        return contents

    def buildLexicon(self):
        filePath = os.path.join('data', 'NRC-emotion-lexicon.txt')
        lines = self.readFile(filePath).splitlines()
        for line in lines:
            word,emotion,value = line.split('\t')
            if emotion == 'positive' and int(value) == 1:
                self.posWords.add(word)
            if emotion == 'negative' and int(value) == 1:
                self.negWords.add(word)     
   
    def buildSplit(self,include_test=True):
        split = self.Splitter()
        datasets = ['train','dev']
        if include_test:
            datasets.append('test')
        for dataset in datasets:
            for klass in ['pos', 'neg']:
                filePath = os.path.join('data', dataset, klass)
                dataFiles = os.listdir(filePath)
                for dataFile in dataFiles:
                    words = self.readFile(os.path.join(filePath, dataFile)).replace('\n',' ')
                    example = self.Example()
                    example.words = words
                    example.words = self.filterStopWords(example.words.split())
                    example.klass = 1 if klass == 'pos' else 0
                    if dataset == 'train':
                        split.train.append(example)
                    elif dataset == 'dev':
                        split.dev.append(example)
                    else:
                        split.test.append(example)
        return split


    def filterStopWords(self, words):
        """Filters stop words."""
        filtered = []
        for word in words:
            if not word in self.stopList and word.strip() != '':
                filtered.append(word)
        return ' '.join(filtered)


def evaluate(INCLUDE_LEXICON):
    classifier = LogisticRegression()
    classifier.INCLUDE_LEXICON  = INCLUDE_LEXICON

    classifier.buildLexicon()

    split = classifier.buildSplit(include_test=False)

    classifier.train(split.train)

    train_accuracy = calculate_accuracy(split.train, classifier)
    dev_accuracy = calculate_accuracy(split.dev, classifier)

    print('Train Accuracy: {}'.format(train_accuracy))
    print('Dev Accuracy: {}'.format(dev_accuracy))


def calculate_accuracy(dataset, classifier):
    acc = 0.0
    for example in dataset:
        guess = classifier.classify(example.words)    
        if example.klass == guess:
            acc += 1.0
    return acc / len(dataset)


def main():
    INCLUDE_LEXICON  = False
    (options, args) = getopt.getopt(sys.argv[1: ], 'l')
    if ('-l', '') in options:
        INCLUDE_LEXICON  = True

    evaluate(INCLUDE_LEXICON)

if __name__ == "__main__":
        main()
