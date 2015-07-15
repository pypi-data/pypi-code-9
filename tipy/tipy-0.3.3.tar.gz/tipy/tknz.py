#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The Tokenizer class takes an input stream and parses it into tokens.

The parsing process is controlled by the character classification sets:

    - blankspace characters: characters that mark a token boundary and are not
                             part of the token.

    - separator characters: characters that mark a token boundary and might be
                            considered tokens, depending on the value of a flag
                            (to be implemented).

    - valid characters: any non blankspace and non separator character.

Each byte read from the input stream is regarded as a character in the range
'\\u0000' through '\\u00FF'.

In addition, an instance has flags that control:

    - whether the characters of tokens are converted to lowercase.
    - whether separator characters constitute tokens. (TBD)

A typical application first constructs an instance of this class, supplying
the input stream to be tokenized, the set of blankspaces, and the set of
eparators, and then repeatedly loops, while method has_more_tokens() returns
true, calling the next_token() method.
"""

from abc import ABCMeta, abstractmethod
from codecs import open as copen
from collections import defaultdict
from tipy.char import blankspaces, separators


class Tokenizer(object):
    """Abstract class for all tokenizers.

    G{classtree Tokenizer}"""

    __metaclass__ = ABCMeta

    def __init__(self, stream, blankspaces=blankspaces, separators=separators):
        """Constructor of the Tokenizer abstract class.

        @param stream:
            The stream to tokenize. Can be a filename or any open IO stream.
        @type stream: str or io.IOBase
        @param blankspaces:
            The characters that represent empty spaces.
        @type blankspaces: str
        @param separators:
            The characters that separate token units (e.g. word boundaries).
        @type separators: str
        """
        self.separators = separators
        self.blankspaces = blankspaces
        self.lowercase = False
        self.offbeg = 0
        self.offset = None
        self.offend = None

    def is_blankspace(self, char):
        """Test if a character is a blankspace.

        @param char:
            The character to test.
        @type char: str

        @return:
            True if character is a blankspace, False otherwise.
        @rtype: bool
        """
        if len(char) > 1:
            raise TypeError("Expected a char.")
        if char in self.blankspaces:
            return True
        else:
            return False

    def is_separator(self, char):
        """Test if a character is a separator.

        @param char:
            The character to test.
        @type char: str

        @return:
            True if character is a separator, False otherwise.
        @rtype: bool
        """
        if len(char) > 1:
            raise TypeError("Expected a char.")
        if char in self.separators:
            return True
        else:
            return False

    @abstractmethod
    def count_chars(self):
        raise NotImplementedError("Method must be implemented")

    @abstractmethod
    def reset_stream(self):
        raise NotImplementedError("Method must be implemented")

    @abstractmethod
    def count_tokens(self):
        raise NotImplementedError("Method must be implemented")

    @abstractmethod
    def has_more_tokens(self):
        raise NotImplementedError("Method must be implemented")

    @abstractmethod
    def next_token(self):
        raise NotImplementedError("Method must be implemented")

    @abstractmethod
    def progress(self):
        raise NotImplementedError("Method must be implemented")


class ForwardTokenizer(Tokenizer):
    """Tokenize a stream from the beginning to the end.

    G{classtree ForwardTokenizer}
    """

    def __init__(self, stream, lowercase=False, blankspaces=blankspaces,
                 separators=separators):
        """Constructor of the ForwardTokenizer class.

        @warning: When passing IOBase type variable as stream parameter: the
                  read() method is used to read the stream and it can be time
                  consuming. Please don't pass IOBase during the prediction
                  process!

        @param stream:
            The stream to tokenize. Can be a filename or any open IO stream.
        @type stream: str or io.IOBase
        @param blankspaces:
            The characters that represent empty spaces.
        @type blankspaces: str
        @param separators:
            The characters that separate token units (e.g. word boundaries).
        @type separators: str
        """
        Tokenizer.__init__(self, stream, blankspaces, separators)
        if type(stream)is str:
            self.text = stream
        else:
            if not hasattr(stream, 'read'):
                stream = copen(stream, "r", "utf-8")
            self.text = stream.read()
            stream.close()
        self.lowercase = lowercase
        self.offend = self.count_chars()
        self.reset_stream()

    def count_tokens(self):
        """Check the number of tokens left.

        @return:
            The number of tokens left.
        @rtype: int
        """
        count = 0
        while(self.has_more_tokens()):
            count += 1
            self.next_token()
        self.reset_stream()
        return count

    def count_chars(self):
        """Count the number of characters in the stream.

        @note: Should return the same value as the wc Unix command.

        @return:
            The number of characters in the stream.
        @rtype: int
        """
        return len(self.text)

    def has_more_tokens(self):
        """Test if at least one token remains.

        @return:
            True or False weither there is at least one token left in the
            stream.
        @rtype: bool
        """
        if self.offset < self.offend:
            return True
        else:
            return False

    def next_token(self):
        """Retrieve the next token in the stream.

        @return:
            Return the next token or '' if there is no next token.
        @rtype: str
        """
        if not self.has_more_tokens():
            return ''
        current = self.text[self.offset]
        token = ''
        if self.offset < self.offend:
            while self.is_blankspace(current) or self.is_separator(current):
                self.offset += 1
                try:
                    current = self.text[self.offset]
                except IndexError:
                    break
            while not self.is_blankspace(current) and not self.is_separator(
                    current) and self.offset < self.offend:
                if self.lowercase:
                    current = current.lower()
                token += current
                self.offset += 1
                try:
                    current = self.text[self.offset]
                except IndexError:
                    break
        return token

    def progress(self):
        """Return the progress percentage.

        @return:
            The tokenization progress percentage.
        @rtype: float
        """
        return float(self.offset) / self.offend * 100

    def reset_stream(self):
        """Reset the offset to 0."""
        self.offset = 0


class ReverseTokenizer(Tokenizer):
    """Tokenize a stream from the end to the beginning.

    G{classtree ReverseTokenizer}
    """

    def __init__(self, stream, lowercase=False, blankspaces=blankspaces,
                 separators=separators):
        """Constructor of the ReverseTokenizer class.

        @param stream:
            The stream to tokenize. Can be a filename or any open IO stream.
        @type stream: str or io.IOBase
        @param blankspaces:
            The characters that represent empty spaces.
        @type blankspaces: str
        @param separators:
            The characters that separate token units (e.g. word boundaries).
        @type separators: str
        """
        Tokenizer.__init__(self, stream, blankspaces, separators)
        if type(stream) is str:
            self.text = stream
        else:
            if not hasattr(stream, 'read'):
                stream = copen(stream, "r", "utf-8")
            self.text = stream.read()
            stream.close()
        self.lowercase = lowercase
        self.offend = self.count_chars() - 1
        self.reset_stream()

    def count_tokens(self):
        """Check the number of tokens left.

        @return:
            The number of tokens left.
        @rtype: int
        """
        curroff = self.offset
        self.offset = self.offend
        count = 0
        while (self.has_more_tokens()):
            self.next_token()
            count += 1
        self.offset = curroff
        return count

    def count_chars(self):
        """Count the number of characters in the stream.

        @note: Should return the same value as the wc Unix command.

        @return:
            The number of characters in the stream.
        @rtype: int
        """
        return len(self.text)

    def has_more_tokens(self):
        """Test if at least one token remains.

        @return:
            True or False weither there is at least one token left in the
            stream. (Keep in mind that the stream is tokenized from the end to
            the beginning).
        @rtype: bool
        """
        if self.offbeg <= self.offset:
            return True
        else:
            return False

    def next_token(self):
        """Retrieve the next token in the stream.

        @note: As this is a reversed tokenizer the "next" token is currently
               what one would call the "previous" token but in the tokenizer
               workflow if think its more logic to call it the "next" token.

        @return:
            Return the next token or '' if there is no next token.
        @rtype: str
        """
        if not self.has_more_tokens():
            return ''
        token = ""
        while self.offbeg <= self.offset and len(token) == 0:
            current = self.text[self.offset]
            if (self.offset == self.offend) and (self.is_separator(current)
                                                 or
                                                 self.is_blankspace(current)):
                self.offset -= 1
                return token
            while (self.is_blankspace(current) or self.is_separator(current)) \
                    and self.offbeg < self.offset:
                self.offset -= 1
                if (self.offbeg <= self.offset):
                    current = self.text[self.offset]

            while (not self.is_blankspace(current) and
                   not self.is_separator(current) and
                   self.offbeg <= self.offset):
                if self.lowercase:
                    current = current.lower()
                token = current + token
                self.offset -= 1
                if (self.offbeg <= self.offset):
                    current = self.text[self.offset]
        return token

    def progress(self):
        """Return the progress percentage.

        @return:
            The tokenization progress percentage.
        @rtype: float
        """
        return float(self.offend - self.offset) / (self.offend - self.offbeg)

    def reset_stream(self):
        """Reset the offset to the end offset."""
        self.offset = self.offend


class TextTokenizer(Tokenizer):
    """Tokenizer to tokenize a text file.

    This tokenizer recieve a text file and generate n-grams of a given size "n".
    It is usefule to the L{text miner<minr.TextMiner>} in order to generate
    n-grams to be inserted in a database.

    G{classtree TextTokenizer}
    """

    def __init__(self, infile, n, lowercase=False, cutoff=0, callback=None):
        """TextTokenizer creator.

        @param infile:
            Path to the file to tokenize.
        @type infile: str
        @param n:
            The n in n-gram. Specify the maximum n-gram size to be created.
        @type n: int
        @param lowercase:
            If True: all tokens are convert to lowercase before being added to
            the dictionary.
            If False: tokens case remains untouched.
        @type lowercase: bool
        @param cutoff:
            Set the minimum number of token occurences. If a token dosen't
            appear more than this number it is removed from the dictionary
            before it is returned.
        @type cutoff: int
        """
        self.infile = infile
        self.n = n
        self.lowercase = lowercase
        self.cutoff = cutoff
        self.callback = callback

    def tknize_text(self):
        """Tokenize a file and return a dictionary mapping its n-grams.

        The dictionary looks like::
            { ('in',      'the',    'second'): 4,
              ('right',   'hand',   'of'):     1,
              ('subject', 'to',     'the'):    2,
              ('serious', 'rebuff', 'in'):     1,
              ('spirit',  'is',     'the'):    1 }
        """
        ngramMap = defaultdict(int)
        ngramList = []
        tokenizer = ForwardTokenizer(open(self.infile), self.lowercase)
        for i in range(self.n - 1):
            if not tokenizer.has_more_tokens():
                break
            ngramList.append(tokenizer.next_token())
        while tokenizer.has_more_tokens():
            if self.callback:
                self.callback(tokenizer.progress())
            token = tokenizer.next_token()
            ngramList.append(token)
            ngramMap[tuple(ngramList)] += 1
            ngramList.pop(0)
        if self.cutoff > 0:
            for k in ngramMap.keys():
                if ngramMap[k] <= self.cutoff:
                    del(ngramMap[k])
        return ngramMap
