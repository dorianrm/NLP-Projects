#!/usr/bin/env python
import json
import math
import os
import re
import sys

from PorterStemmer import PorterStemmer

# Gradescope: 30/30

class IRSystem:

    def __init__(self):
        # For holding the data - initialized in read_data()
        self.titles = []
        self.docs = []
        self.vocab = []
        # For the text pre-processing.
        self.alphanum = re.compile('[^a-zA-Z0-9]')
        self.p = PorterStemmer()


    def get_uniq_words(self):
        uniq = set()
        for doc in self.docs:
            for word in doc:
                uniq.add(word)
        return uniq


    def __read_raw_data(self, dirname):
        print("Stemming Documents...")

        titles = []
        docs = []
        os.mkdir('%s/stemmed' % dirname)
        title_pattern = re.compile('(.*) \d+\.txt')

        # make sure we're only getting the files we actually want
        filenames = []
        for filename in os.listdir('%s/raw' % dirname):
            if filename.endswith(".txt") and not filename.startswith("."):
                filenames.append(filename)

        for i, filename in enumerate(filenames):
            title = title_pattern.search(filename).group(1)
            print("    Doc %d of %d: %s" % (i+1, len(filenames), title))
            titles.append(title)
            contents = []
            f = open('%s/raw/%s' % (dirname, filename), 'r', encoding="utf-8")
            of = open('%s/stemmed/%s.txt' % (dirname, title), 'w', encoding="utf-8")
            for line in f:
                # make sure everything is lower case
                line = line.lower()
                # split on whitespace
                line = [xx.strip() for xx in line.split()]
                # remove non alphanumeric characters
                line = [self.alphanum.sub('', xx) for xx in line]
                # remove any words that are now empty
                line = [xx for xx in line if xx != '']
                # stem words
                line = [self.p.stem(xx) for xx in line]
                # add to the document's conents
                contents.extend(line)
                if len(line) > 0:
                    of.write(" ".join(line))
                    of.write('\n')
            f.close()
            of.close()
            docs.append(contents)
        return titles, docs


    def __read_stemmed_data(self, dirname):
        print("Already stemmed!")
        titles = []
        docs = []

        # make sure we're only getting the files we actually want
        filenames = []
        for filename in os.listdir('%s/stemmed' % dirname):
            if filename.endswith(".txt") and not filename.startswith("."):
                filenames.append(filename)

        if len(filenames) != 60:
            msg = "There are not 60 documents in ../data/RiderHaggard/stemmed/\n"
            msg += "Remove ../data/RiderHaggard/stemmed/ directory and re-run."
            raise Exception(msg)

        for i, filename in enumerate(filenames):
            title = filename.split('.')[0]
            titles.append(title)
            contents = []
            f = open('%s/stemmed/%s' % (dirname, filename), 'r', encoding="utf-8")
            for line in f:
                # split on whitespace
                line = [xx.strip() for xx in line.split()]
                # add to the document's conents
                contents.extend(line)
            f.close()
            docs.append(contents)

        return titles, docs


    def read_data(self, dirname):
        """
        Given the location of the 'data' directory, reads in the documents to
        be indexed.
        """
        # NOTE: We cache stemmed documents for speed
        #       (i.e. write to files in new 'stemmed/' dir).

        print("Reading in documents...")
        # dict mapping file names to list of "words" (tokens)
        filenames = os.listdir(dirname)
        subdirs = os.listdir(dirname)
        if 'stemmed' in subdirs:
            titles, docs = self.__read_stemmed_data(dirname)
        else:
            titles, docs = self.__read_raw_data(dirname)

        # Sort document alphabetically by title to ensure we have the proper
        # document indices when referring to them.
        ordering = [idx for idx, title in sorted(enumerate(titles),
            key = lambda xx : xx[1])]

        self.titles = []
        self.docs = []
        numdocs = len(docs)
        for d in range(numdocs):
            self.titles.append(titles[ordering[d]])
            self.docs.append(docs[ordering[d]])

        # Get the vocabulary.
        self.vocab = [xx for xx in self.get_uniq_words()]


#--------------------------------------------------------------------------#
# CODE TO UPDATE STARTS HERE                                               #
#--------------------------------------------------------------------------#

    def index(self):
        """
        Build an index of the documents.
        """
        print("Indexing...")
        # ------------------------------------------------------------------
        # TODO: Create an inverted, positional index.
        #       Granted this may not be a linked list as in a proper
        #       implementation.
        #       This index should allow easy access to both 
        #       1) the documents in which a particular word is contained, and 
        #       2) for every document, the positions of that word in the document 
        #       Some helpful instance variables:
        #         * self.docs = List of documents
        #         * self.titles = List of titles

        
        # inv_index = {word : {doc: [positions]}}
        inv_index = {}
        #initialize and fill doc to position dictionary
        for title,doc in zip(self.titles, self.docs):
            for word in self.vocab:
                if word in inv_index:
                    inv_index[word][title] = []
                else:
                    inv_index[word] = {}
                    inv_index[word][title] = []
            for p,word in enumerate(doc):
                inv_index[word][title].append(p)

        self.inv_index = inv_index

        # self.titles = []
        # self.docs = []
        # self.vocab = []
        # get_uniq_words(self)

        # ------------------------------------------------------------------

        # turn self.docs into a map from ID to bag of words
        id_to_bag_of_words = {}
        for d, doc in enumerate(self.docs):
            bag_of_words = set(doc)
            id_to_bag_of_words[d] = bag_of_words
        self.docs = id_to_bag_of_words


    def get_word_positions(self, word, doc):
        """
        Given a word and a document, use the inverted index to return
        the positions of the specified word in the specified document.
        """
        # ------------------------------------------------------------------
        # TODO: return the list of positions for a word in a document.
        
        # doc = index which can be used to retrieve the title to get positions
        positions = self.inv_index[word][self.titles[doc]]
        return positions
        # ------------------------------------------------------------------


    def get_posting(self, word):
        """
        Given a word, this returns the list of document indices (sorted) in
        which the word occurs.
        """
        # ------------------------------------------------------------------
        # TODO: return the list of postings for a word.

        # Loop through titles and track index which maps to doc
        posting = []
        for i,title in enumerate(self.titles):
            if len(self.inv_index[word][title]) > 0:
                posting.append(i) #i = doc id 

        return posting
        # ------------------------------------------------------------------


    def get_posting_unstemmed(self, word):
        """
        Given a word, this *stems* the word and then calls get_posting on the
        stemmed word to get its postings list. You should *not* need to change
        this function. It is needed for submission.
        """
        word = self.p.stem(word)
        return self.get_posting(word)


    def boolean_retrieve(self, query):
        """
        Given a query in the form of a list of *stemmed* words, this returns
        the list of documents in which *all* of those words occur (ie an AND
        query).
        Return an empty list if the query does not return any documents.
        """
        # ------------------------------------------------------------------
        # TODO: Implement Boolean retrieval. You will want to use your
        #       inverted index that you created in index().
        # Right now this just returns all the possible documents!

        # Create initial set using first word in query
        # Use buitl in intersection function with sets to find intersection of all postings
        docs = self.get_posting(query[0])
        query = query[1:]
        for word in query:
            docs = set(docs) & set(self.get_posting(word))
        return list(docs)

        # ------------------------------------------------------------------

        return sorted(docs)   # sorted doesn't actually matter


    def phrase_retrieve(self, query):
        """
        Given a query in the form of an ordered list of *stemmed* words, this 
        returns the list of documents in which *all* of those words occur, and 
        in the specified order. 
        Return an empty list if the query does not return any documents. 
        """
        # ------------------------------------------------------------------
        # TODO: Implement Phrase Query retrieval (ie. return the documents 
        #       that don't just contain the words, but contain them in the 
        #       correct order) You will want to use the inverted index 
        #       that you created in index(), and may also consider using
        #       boolean_retrieve. 
        #       NOTE that you no longer have access to the original documents
        #       in self.docs because it is now a map from doc IDs to set
        #       of unique words in the original document.
        # Right now this just returns all possible documents!

        # All docs that contain all words in the query 
        docs = []
        start_docs = self.boolean_retrieve(query)
        for doc in start_docs:
            first_word_pos = self.get_word_positions(query[0], doc)
            pointer = 1
            for pos1 in first_word_pos:
                for word in query[1:]:
                    next_word_pos = self.get_word_positions(word, doc)
                    if pos1+pointer not in next_word_pos:
                        break
                    else:
                        pointer += 1
                if pointer == len(query):
                    docs.append(doc)
        # ------------------------------------------------------------------

        return sorted(docs)   # sorted doesn't actually matter


    def compute_tfidf(self):
        # -------------------------------------------------------------------
        # TODO: Compute and store TF-IDF values for words and documents.
        #       Recall that you can make use of:
        #         * self.vocab: a list of all distinct (stemmed) words
        #         * self.docs: a list of lists, where the i-th document is
        #                   self.docs[i] => ['word1', 'word2', ..., 'wordN']
        #       NOTE that you probably do *not* want to store a value for every
        #       word-document pair, but rather just for those pairs where a
        #       word actually occurs in the document.

        print("Calculating tf-idf...")
        self.tfidf = {}
        for word in self.vocab:
            self.tfidf[word] = {}
            idf_compute = float(len(self.docs)) / float(len(self.get_posting(word)))
            if idf_compute == 0:
                idf = 0
            else:
                idf = math.log10(len(self.docs) / len(self.get_posting(word)))

            for d in range(len(self.docs)):
                tf_compute = len(self.get_word_positions(word, d))
                if tf_compute == 0:
                    self.tfidf[word][d] = 0
                else:
                    self.tfidf[word][d] = (1 + math.log10(tf_compute)) * idf

        # ------------------------------------------------------------------


    def get_tfidf(self, word, document):
        # ------------------------------------------------------------------
        # TODO: Return the tf-idf weigthing for the given word (string) and
        #       document index.
        tfidf = self.tfidf[word][document]
        # ------------------------------------------------------------------
        return tfidf


    def get_tfidf_unstemmed(self, word, document):
        """
        This function gets the TF-IDF of an *unstemmed* word in a document.
        Stems the word and then calls get_tfidf. You should *not* need to
        change this interface, but it is necessary for submission.
        """
        word = self.p.stem(word)
        return self.get_tfidf(word, document)


    def rank_retrieve(self, query):
        """
        Given a query (a list of words), return a rank-ordered list of
        documents (by ID) and score for the query.
        """
        scores = [0.0 for xx in range(len(self.titles))]
        # ------------------------------------------------------------------
        # TODO: Implement cosine similarity between a document and a list of
        #       query words.

        # Right now, this code simply gets the score by taking the Jaccard
        # similarity between the query and every document.

        words_in_query = set(query)
        # for d in range(len(self.docs)):
        #     tf_wt = {}
        #     norm = 0.0
        #     for word in words_in_query:
        #         if len(self.get_word_positions(word, d)) == 0:
        #             tf_wt[word] = 0
        #         else:
        #             tf_wt[word] = (1 + math.log10(len(self.get_word_positions(word, d)))) * self.idf[d]
        #         norm += tf_wt[word]**2
        #     for word in words_in_query:
        #         if norm != 0 or tf_wt[word] != 0:
        #             tf_wt[word] /= math.sqrt(norm)
        #             scores[d] += query.count(word) * tf_wt[word]

        for d in range(len(self.docs)):
            norm = 0.0
            for word in self.vocab:
                norm += self.tfidf[word][d] ** 2
            for word in words_in_query:
                if norm != 0 and self.tfidf[word][d] != 0:
                    scores[d] += (1 + math.log10(query.count(word))) * (self.tfidf[word][d] / math.sqrt(norm))

        # ------------------------------------------------------------------

        ranking = [idx for idx, sim in sorted(enumerate(scores),
            key = lambda xx : xx[1], reverse = True)]
        results = []
        for i in range(10):
            results.append((ranking[i], scores[ranking[i]]))
        return results

#--------------------------------------------------------------------------#
# CODE TO UPDATE ENDS HERE                                                 #
#--------------------------------------------------------------------------#


    def process_query(self, query_str):
        """
        Given a query string, process it and return the list of lowercase,
        alphanumeric, stemmed words in the string.
        """
        # make sure everything is lower case
        query = query_str.lower()
        # split on whitespace
        query = query.split()
        # remove non alphanumeric characters
        query = [self.alphanum.sub('', xx) for xx in query]
        # stem words
        query = [self.p.stem(xx) for xx in query]
        return query

    def query_retrieve(self, query_str):
        """
        Given a string, process and then return the list of matching documents
        found by boolean_retrieve().
        """
        query = self.process_query(query_str)
        return self.boolean_retrieve(query)

    def phrase_query_retrieve(self, query_str):
        """
        Given a string, process and then return the list of matching documents
        found by phrase_retrieve().
        """
        query = self.process_query(query_str)
        return self.phrase_retrieve(query)

    def query_rank(self, query_str):
        """
        Given a string, process and then return the list of the top matching
        documents, rank-ordered.
        """
        query = self.process_query(query_str)
        return self.rank_retrieve(query)


def run_tests(irsys):
    print("===== Running tests =====")

    ff = open('../data/queries.txt')
    questions = [xx.strip() for xx in ff.readlines()]
    ff.close()
    ff = open('../data/solutions.txt')
    solutions = [xx.strip() for xx in ff.readlines()]
    ff.close()

    epsilon = 1e-4
    for part in range(6):
        points = 0
        num_correct = 0
        num_total = 0

        prob = questions[part]
        soln = json.loads(solutions[part])

        if part == 0:   # inverted index test
            print("Inverted Index Test")
            queries = prob.split("; ")
            queries = [xx.split(", ") for xx in queries]
            queries = [(xx[0], int(xx[1])) for xx in queries]
            for i, (word, doc) in enumerate(queries):
                num_total += 1
                guess = irsys.get_word_positions(word, doc)
                if sorted(guess) == soln[i]:
                    num_correct += 1

        elif part == 1:     # get postings test
            print("Get Postings Test")
            words = prob.split(", ")
            for i, word in enumerate(words):
                num_total += 1
                posting = irsys.get_posting_unstemmed(word)
                if posting == soln[i]:
                    num_correct += 1

        elif part == 2:   # boolean retrieval test
            print("Boolean Retrieval Test")
            queries = prob.split(", ")
            for i, query in enumerate(queries):
                num_total += 1
                guess = irsys.query_retrieve(query)
                if set(guess) == set(soln[i]):
                    num_correct += 1

        elif part == 3: # phrase query test
            print("Phrase Query Retrieval")
            queries = prob.split(", ")
            for i, query in enumerate(queries):
                num_total += 1
                guess = irsys.phrase_query_retrieve(query)
                if set(guess) == set(soln[i]):
                    num_correct += 1

        elif part == 4:   # tfidf test
            print("TF-IDF Test")
            queries = prob.split("; ")
            queries = [xx.split(", ") for xx in queries]
            queries = [(xx[0], int(xx[1])) for xx in queries]
            for i, (word, doc) in enumerate(queries):
                num_total += 1
                guess = irsys.get_tfidf_unstemmed(word, doc)
                if guess >= float(soln[i]) - epsilon and \
                        guess <= float(soln[i]) + epsilon:
                    num_correct += 1

        elif part == 5:   # cosine similarity test
            print("Cosine Similarity Test")
            queries = prob.split(", ")
            for i, query in enumerate(queries):
                num_total += 1
                ranked = irsys.query_rank(query)
                top_rank = ranked[0]
                if top_rank[0] == soln[i][0]:
                    if top_rank[1] >= float(soln[i][1]) - epsilon and \
                            top_rank[1] <= float(soln[i][1]) + epsilon:
                        num_correct += 1

        feedback = "%d/%d Correct. Accuracy: %f" % \
                (num_correct, num_total, float(num_correct)/num_total)

        if part == 1:
            if num_correct == num_total:
                points = 2
            elif num_correct >= 0.5 * num_total:
                points = 1
            else:
                points = 0
        elif part == 2:
            if num_correct == num_total:
                points = 1
            else:
                points = 0
        else:
            if num_correct == num_total:
                points = 3
            elif num_correct > 0.75 * num_total:
                points = 2
            elif num_correct > 0:
                points = 1
            else:
                points = 0

        print("    Score: %d Feedback: %s" % (points, feedback))

def main(args):
    irsys = IRSystem()
    irsys.read_data('../data/RiderHaggard')
    irsys.index()
    irsys.compute_tfidf()

    if len(args) == 0:
        run_tests(irsys)
    else:
        query = " ".join(args)
        print("Best matching documents to '%s':" % query)
        results = irsys.query_rank(query)
        for docId, score in results:
            print("%s: %e" % (irsys.titles[docId], score))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)