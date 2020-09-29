import sys
import getopt
import os
import math
import operator
from collections import defaultdict

# Gradescope: 90/90

class NaiveBayes:
    class TrainSplit:
        """Represents a set of training/testing data. self.train is a list of Examples, as is self.dev and self.test. 
        """
        def __init__(self):
            self.train = []
            self.dev = []
            self.test = []

    class Example:
        """Represents a document with a label. klass is 'aid' or 'not' by convention.
             words is a list of strings.
        """
        def __init__(self):
            self.klass = ''
            self.words = []

    def __init__(self):
        """NaiveBayes initialization"""
        self.FILTER_STOP_WORDS = False
        self.USE_BIGRAMS = False
        self.BEST_MODEL = False
        self.stopList = set(self.readFile('data/english.stop'))
        #TODO: add other data structures needed in classify() and/or addExample() below
        self.wordsInClass = defaultdict(lambda: 0)   #All words found in a class with their counts wordsInClass[(word,klass)]
        self.classWords = defaultdict(lambda: 0)     #Number of words per class classWords[klass]
        self.classes = defaultdict(lambda: 0)  #all unique classes classes[klass] and their count of docs in the corpus
        self.vocab = set()  #unique words in all docs
        self.count = 0    #count of all docs D in the corpus


    #############################################################################
    # TODO TODO TODO TODO TODO 
    # Implement the Multinomial Naive Bayes classifier with add-1 smoothing
    # If the FILTER_STOP_WORDS flag is true, you must remove stop words
    # If the USE_BIGRAMS flag is true, your methods must use bigram features instead of the usual 
    # bag-of-words (unigrams)
    # If either of the FILTER_STOP_WORDS or USE_BIGRAMS flags is on, the other is meant to be off. 
    # Hint: Use filterStopWords(words) defined below
    # Hint: Remember to add start and end tokens in the bigram implementation
    # Hint: When doing add-1 smoothing with bigrams, V = # unique bigrams in data. 

    def classify(self, words):
        """ TODO
            'words' is a list of words to classify. Return 'aid' or 'not' classification.
        """
        pAid = math.log(self.classes['aid'] / self.count)  #Added priors to start
        pNot = math.log(self.classes['not'] / self.count)


        if self.USE_BIGRAMS == False:
            for word in words:
                if word in self.vocab:
                    pAid += math.log((self.wordsInClass[(word, 'aid')] + 1) / (self.classWords['aid'] + len(self.vocab)))
                    pNot += math.log((self.wordsInClass[(word, 'not')] + 1) / (self.classWords['not'] + len(self.vocab)))

        if self.USE_BIGRAMS == True:
            prev = "<s>"
            words.append("</s>")
            for word in words:
                if(prev, word) in self.vocab:
                    pAid += math.log((self.wordsInClass[(prev, word, 'aid')] + 1) / (self.classWords['aid'] + len(self.vocab)))
                    pNot += math.log((self.wordsInClass[(prev, word, 'not')] + 1) / (self.classWords['not'] + len(self.vocab)))
                    prev = word
                else:
                    prev = word

        if pAid > pNot:
            return 'aid'
        else:
            return 'not'
    

    def addExample(self, klass, words):
        """
         * TODO
         * Train your model on an example document with label klass ('aid' or 'not') and
         * words, a list of strings.
         * You should store whatever data structures you use for your classifier 
         * in the NaiveBayes class.
         * Returns nothing
        """

        self.classes[klass] += 1   #Add count of Docs D per class
        self.count += 1             #Add to total count of Docs D in corpus

        if self.FILTER_STOP_WORDS == True: #Apply stop words filter
            words = self.filterStopWords(words)

        if self.USE_BIGRAMS == False:
            for word in words:
                self.vocab.add(word)                #Add unique word
                self.classWords[klass] += 1         #Number of words per class
                self.wordsInClass[(word, klass)] += 1       #(word | class)
        
        if self.USE_BIGRAMS == True: 
            prev = "<s>" #Add start and end tokens to capture first and last word bigrams
            words.append("</s>")
            for word in words:
                self.vocab.add((prev, word))  #Add unique bigram
                self.classWords[klass] += 1         #Number of bigrams per class
                self.wordsInClass[(prev, word, klass)] += 1        #(bigram | class)
                prev = word




                    
        
    # END TODO (Modify code beyond here with caution)
    #############################################################################
    
    def readFile(self, fileName):
        """
         * Code for reading a file.  you probably don't want to modify anything here, 
         * unless you don't like the way we segment files.
        """
        contents = []
        f = open(fileName,encoding="utf8")
        for line in f:
            contents.append(line)
        f.close()
        result = self.segmentWords('\n'.join(contents)) 
        return result

    def segmentWords(self, s):
        """
         * Splits lines on whitespace for file reading
        """
        return s.split()

    def buildSplit(self,include_test=True):
    
        split = self.TrainSplit()
        datasets = ['train','dev']
        if include_test:
            datasets.append('test')
        for dataset in datasets:
            for klass in ['aid','not']:
                dataFile = os.path.join('data',dataset,klass + '.txt')
                with open(dataFile,'r', encoding="utf8") as f:
                    docs = [line.rstrip('\n') for line in f]
                    for doc in docs:
                        example = self.Example()
                        example.words = doc.split()
                        example.klass = klass
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
        return filtered
    
def evaluate(FILTER_STOP_WORDS,USE_BIGRAMS):
    classifier = NaiveBayes()
    classifier.FILTER_STOP_WORDS = FILTER_STOP_WORDS
    classifier.USE_BIGRAMS = USE_BIGRAMS
    split = classifier.buildSplit(include_test=False)
   
    for example in split.train:
        classifier.addExample(example.klass,example.words)

    train_accuracy = calculate_accuracy(split.train,classifier)
    dev_accuracy = calculate_accuracy(split.dev,classifier)

    print('Train Accuracy: {}'.format(train_accuracy))
    print('Dev Accuracy: {}'.format(dev_accuracy))


def calculate_accuracy(dataset,classifier):
    acc = 0.0
    if len(dataset) == 0:
        return 0.0
    else:
        for example in dataset:
            guess = classifier.classify(example.words)
            if example.klass == guess:
                acc += 1.0
        return acc / len(dataset)

        
def main():
    FILTER_STOP_WORDS = False
    USE_BIGRAMS = False
    (options, args) = getopt.getopt(sys.argv[1:], 'fb')
    if ('-f','') in options:
      FILTER_STOP_WORDS = True
    elif ('-b','') in options:
      USE_BIGRAMS = True

    evaluate(FILTER_STOP_WORDS,USE_BIGRAMS)

if __name__ == "__main__":
        main()
