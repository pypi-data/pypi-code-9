''' Create words from an existing wordlist '''
import random
import re

class WordBuilder(object):
    ''' uses an existing corpus to create new phonemically consistent words '''

    def __init__(self, initial='>', terminal='<', chunk_size=2):
        #indicators for start and ends of words - set if necessary to avoid collision
        self.initial = initial
        self.terminal = terminal

        self.chunk_size = chunk_size

        self.links = {
            self.initial: []
        }

        self.average_word_length = 0
        self.shortest = None


    def ingest(self, corpus_file):
        ''' load and parse a pre-formatted and cleaned text file. Garbage in, garbage out '''
        corpus = open(corpus_file)
        total_letters = 0
        total_words = 0
        shortest_word = 100
        for word in corpus.readlines():
            # clean word
            word = word.strip()
            word = re.sub(r'[\',\.\"]', '', word)
            total_letters += len(word)
            total_words += 1
            shortest_word = len(word) if len(word) < shortest_word else shortest_word

            # iterate through n letter groups, where 1 <= n <= 3
            n = self.chunk_size
            start = 0
            # >: C, Cys: t, yst: i
            self.links[self.initial].append(word[0:n])
            for position in range(n, len(word)):
                start = position - n if position - n >= 0 else 0
                base = word[start:position]
                if not base in self.links:
                    self.links[base] = []

                self.links[base].append(word[position])
            if not word[-n:] in self.links:
                self.links[word[-n:]] = []
            self.links[word[-n:]].append(self.terminal)

        self.average_word_length = total_letters / total_words
        self.shortest = shortest_word


    def get_word(self, word=None):
        ''' creates a new word '''
        word = word if not word == None else self.initial
        if not self.terminal in word:
            if len(word) > self.average_word_length and \
                    self.terminal in self.links[word[-self.chunk_size:]] \
                    and random.randint(0, 1):
                addon = self.terminal
            else:
                options = self.links[word[-self.chunk_size:]]
                addon = random.choice(options)

            word = word + addon
            return self.get_word(word)
        return word[1:-1]
