''' Produce latin names for flowers '''
import random
from wordbuilder.WordBuilder import WordBuilder
from os import path

here = path.abspath(path.dirname(__file__))

class NominaFlora(object):
    ''' Uses WordBuilder to create flower names '''

    def __init__(self):
        self.chunk_size = 2
        self.genus_builder = self.get_builder('%s/data/genus' % here)
        self.species_builder = self.get_builder('%s/data/species' % here)
        self.common_first = self.get_common('%s/data/common_first' % here)
        self.common_second = self.get_common('%s/data/common_second' % here)


    def get_builder(self, corpus):
        ''' creates a builder object for a wordlist '''
        builder = WordBuilder(chunk_size=self.chunk_size)
        builder.ingest(corpus)
        return builder


    def get_common(self, filename):
        ''' Process lists of common name words '''
        word_list = []
        words = open(filename)
        for word in words.readlines():
            word_list.append(word.strip())
        return word_list


    def get_scientific_name(self):
        ''' Get a new flower name '''
        genus = self.genus_builder.get_word()
        species = self.species_builder.get_word()
        return '%s %s' % (genus, species)


    def get_common_name(self):
        ''' Get a flower's common name '''
        name = random.choice(self.common_first)
        if random.randint(0, 1) == 1:
            name += ' ' + random.choice(self.common_first).lower()
        name += ' ' + random.choice(self.common_second).lower()
        return name


if __name__ == '__main__':
    namer = NominaFlora()
    for _ in range(5):
        print '%s (%s)' % (namer.get_scientific_name(), namer.get_common_name())
