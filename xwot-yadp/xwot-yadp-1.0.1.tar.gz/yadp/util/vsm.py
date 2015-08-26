#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Yadp  - Yet Another Discovery Protocol
# Copyright (C) 2015  Alexander Rüedlinger
#
# This file is part of Yadp.
#
# Yadp is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Yadp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Yadp.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Alexander Rüedlinger'

import math


class Document(object):

    def __init__(self, key, terms):
        self._key = key
        self._terms = terms

    @property
    def terms(self):
        return set(self._terms)

    @property
    def key(self):
        return self._key

    def apply_filters(self, filters):
        for _filter in filters:
            self._terms = map(lambda term: _filter.apply(term), self._terms)


class Corpus(object):

    def __init__(self, documents):
        self._documents = {}
        for document in documents:
            self._documents[document.key] = document

    def add_document(self, key, document):
        self._documents[key] = document

    def remove_document(self, key):
        del self._documents[key]

    def update(self):
        pass

    def apply_filters(self, _filters):
        for key, doc in self._documents.items():
            doc.apply_filters(_filters)

    @property
    def documents(self):
        return self._documents


class Engine(object):

    def __init__(self, corpus, filters=None):
        self._corpus = corpus
        self._porter_stemmer = PorterStemmer()
        self._filters = filters or [LowerCaseFilter(), PunctuationFilter(), self._porter_stemmer ]
        self._idf_table = {}
        self._term_count = {}
        self._tf_table = {}
        self._dt_table = {}
        self._terms = set()
        self._norm = {}
        self._initialize_tables()

    def _initialize_tables(self):
        N = len(self._corpus.documents.values())

        self._corpus.apply_filters(self._filters)

        for key, doc in self._corpus.documents.items():
            for term in doc.terms:

                if term not in STOP_WORDS:

                    self._terms.add(term)
                    if term not in self._idf_table:
                        self._idf_table[term] = 0
                        self._term_count[term] = 0

                    self._idf_table[term] += 1
                    self._term_count[term] += 1

                    if (key, term) not in self._tf_table:
                        self._tf_table[(key, term)] = 0

                    self._tf_table[(key, term)] += 1

        for key, idf in self._idf_table.items():
            self._idf_table[key] = math.log(1 + N / float(idf), 2)

        for (key, term), tf in self._tf_table.items():
            idf = self._idf_table[term]
            tf = self._tf_table[(key, term)]

            # computer cosine normalization component
            s = [math.pow(_tf * self._idf_table[k], 2)
                 for (i, k), _tf in self._tf_table.items() if key == i]

            sq = math.sqrt(sum(s))
            self._dt_table[(key, term)] = idf * tf / sq

        # compute norm for each document
        for key, _ in self._corpus.documents.items():
            ws = [w*w for (i, k), w in self._dt_table.items() if i == key]
            self._norm[key] = math.sqrt(sum(ws))

    SPECIAL_WEIGHTS = {
        'sensor': 2,
        'device': 2,
        'context': 2,
        'actuator': 2,
        'tag': 2,
        'resource': 2
    }

    def query(self, query_terms):
        special_weights = {}
        for key, weight in self.SPECIAL_WEIGHTS.items():
            new_key = self._porter_stemmer.apply(key)
            special_weights[new_key] = weight

        for _filter in self._filters:
            query_terms = map(lambda t: _filter.apply(t), query_terms)

        new_query_terms = {}

        for term in self._terms:
            new_query_terms[term] = 0

        for term in query_terms:
            if term in new_query_terms:
                new_query_terms[term] += special_weights.get(term, 1)

        for term, _ in new_query_terms.items():
            new_query_terms[term] = new_query_terms[term] / float(self._term_count[term]) * self._idf_table[term]

        s = [w * w for _, w in new_query_terms.items()]
        qnorm = math.sqrt(sum(s))

        # compute similarity matrix using a cosine similarity
        sim = {}
        for key, doc in self._corpus.documents.items():
            sim[key] = 0
            for term, wq in new_query_terms.items():
                if (key, term) not in self._dt_table:
                    self._dt_table[(key, term)] = 0
                dnorm = self._norm[key]
                if (qnorm * dnorm) > 0:
                    sim[key] += self._dt_table[(key, term)] * wq / (qnorm * dnorm)
                else:
                    sim[key] = 0

        return sim


class Filter(object):

    def apply(self, word):
        raise NotImplementedError


class PunctuationFilter(Filter):

    REMOVE_SYMBOLS = [',', '', ':', '-', '!', '?', '.', ';', ' ']

    def apply(self, term):
        if term not in self.REMOVE_SYMBOLS:
            if term[-1] in self.REMOVE_SYMBOLS:
                    term = term[0:-1]
        return term


class LowerCaseFilter(Filter):

    def apply(self, word):
        return word.lower()

import stemming.porter2


class PorterStemmer(Filter):

    def apply(self, word):
        return stemming.porter2.stem(word)


STOP_WORDS = """
a   an  a's able	about	above	according
accordingly	across	actually	after	afterwards
again	against	ain't	all	allow
allows	almost	alone	along	already
also	although	always	am	among
amongst	an	and	another	any
anybody	anyhow	anyone	anything	anyway
anyways	anywhere	apart	appear	appreciate
appropriate	are	aren't	around	as
aside	ask	asking	associated	at
available	away	awfully	be	became
because	become	becomes	becoming	been
before	beforehand	behind	being	believe
below	beside	besides	best	better
between	beyond	both	brief	but
by	c'mon	c's	came	can
can't	cannot	cant	cause	causes
certain	certainly	changes	clearly	co
com	come	comes	concerning	consequently
consider	considering	contain	containing	contains
corresponding	could	couldn't	course	currently
definitely	described	despite	did	didn't
different	do	does	doesn't	doing
don't	done	down	downwards	during
each	edu	eg	eight	either
else	elsewhere	enough	entirely	especially
et	etc	even	ever	every
everybody	everyone	everything	everywhere	ex
exactly	example	except	far	few
fifth	first	five	followed	following
follows	for	former	formerly	forth
four	from	further	furthermore	get
gets	getting	given	gives	go
goes	going	gone	got	gotten
greetings	had	hadn't	happens	hardly
has	hasn't	have	haven't	having
he	he's	hello	help	hence
her	here	here's	hereafter	hereby
herein	hereupon	hers	herself	hi
him	himself	his	hither	hopefully
how	howbeit	however	i'd	i'll
i'm	i've	ie	if	ignored
immediate	in	inasmuch	inc	indeed
indicate	indicated	indicates	inner	insofar
instead	into	inward	is	isn't
it	it'd	it'll	it's	its
itself	just	keep	keeps	kept
know	known	knows	last	lately
later	latter	latterly	least	less
lest	let	let's	like	liked
likely	little	look	looking	looks
ltd	mainly	many	may	maybe
me	mean	meanwhile	merely	might
more	moreover	most	mostly	much
must	my	myself	name	namely
nd	near	nearly	necessary	need
needs	neither	never	nevertheless	new
next	nine	no	nobody	non
none	noone	nor	normally	not
nothing	novel	now	nowhere	obviously
of	off	often	oh	ok
okay	old	on	once	one
ones	only	onto	or	other
others	otherwise	ought	our	ours
ourselves	out	outside	over	overall
own	particular	particularly	per	perhaps
placed	please	plus	possible	presumably
probably	provides	que	quite	qv
rather	rd	re	really	reasonably
regarding	regardless	regards	relatively	respectively
right	said	same	saw	say
saying	says	second	secondly	see
seeing	seem	seemed	seeming	seems
seen	self	selves	sensible	sent
serious	seriously	seven	several	shall
she	should	shouldn't	since	six
so	some	somebody	somehow	someone
something	sometime	sometimes	somewhat	somewhere
soon	sorry	specified	specify	specifying
still	sub	such	sup	sure
t's	take	taken	tell	tends
th	than	thank	thanks	thanx
that	that's	thats	the	their
theirs	them	themselves	then	thence
there	there's	thereafter	thereby	therefore
therein	theres	thereupon	these	they
they'd	they'll	they're	they've	think
third	this	thorough	thoroughly	those
though	three	through	throughout	thru
thus	to	together	too	took
toward	towards	tried	tries	truly
try	trying	twice	two	un
under	unfortunately	unless	unlikely	until
unto	up	upon	us	use
used	useful	uses	using	usually
value	various	very	via	viz
vs	want	wants	was	wasn't
way	we	we'd	we'll	we're
we've	welcome	well	went	were
weren't	what	what's	whatever	when
whence	whenever	where	where's	whereafter
whereas	whereby	wherein	whereupon	wherever
whether	which	while	whither	who
who's	whoever	whole	whom	whose
why	will	willing	wish	with
within	without	won't	wonder	would
wouldn't	yes	yet	you	you'd
you'll	you're	you've	your	yours
yourself    yourselves	zero
""".split()


def main():

    d1 = Document(key='d1', terms=['new', 'york', 'times'])
    d2 = Document(key='d2', terms=['new', 'york', 'post'])
    d3 = Document(key='d3', terms=['los', 'angels', 'times'])
    c = Corpus(documents=[d1, d2, d3])
    e = Engine(c)

    print("idf table")
    print(e._idf_table)

    print("tf table")
    print(e._tf_table)

    print("dt table")
    print(e._dt_table)

    sim = e.query(['new', 'new', 'times'])
    print("similarity matrix:")
    print(sim)

if __name__ == '__main__':
    main()
    print(STOP_WORDS)