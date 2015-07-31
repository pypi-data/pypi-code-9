#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Library for generating and translating Morse code
"""


class MorseCode:

    """
    Class that holds everything you need to generate or translate Morse
    """

    def __init__(self):
        self.alphabet = {'0': '-----', '1': '.----', '2': '..---', '3': '...--',
                         '4': '....-', '5': '.....', '6': '-....', '7': '--...',
                         '8': '---..', '9': '----.', 'a': '.-', 'b': '-...',
                         'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 'g': '--.',
                         'h': '....', 'i': '..', 'j': '.---', 'k': '-.-',
                         'l': '.-..', 'm': '--', 'n': '-.', 'o': '---', 'p': '.--.',
                         'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-',
                         'v': '..-', 'w': '.--', 'y': '-.--', 'z': '--..'}

        self.punctuation = {
            '!': '−·−·−−',
            '?': '··−−··',
            '/': '−··−·',
            ';': '−·−·−·',
            ',': '−−··−−',
            '(': '−·−−·',
            ')': '−·−−·−',
            ':': '−−−···',
            '=': '−···−',
            '-': '−····−',
            '+': '·−·−·',
            '@': '·−−·−·',
            '"': '·−··−·',
            '$': '···−··−',
            '_': '··−−·−',
            '&': '·−···',
            ' ': ''}

        # Only holds alphanumeric characters
        self.alpha_list = [letter for letter in self.alphabet.keys()]
        # Only holds Morse code
        self.code_list = [code for code in self.alphabet.values()]

        # Punctuation characters
        self.punc_eng = [punc for punc in self.punctuation.keys()]
        # Punctuation Morse code
        self.punc_codes = [code for code in self.punctuation.values()]

    def generate(self, text):
        """
        Generates Morse code from a message in English
        """
        text = text.lower()  # Make everything lower case, as case doesn't matter in Morse
        morse = []  # Create the list that will eventually hold the Morse code
        for letter in text:  # Search the message for its match in Morse
            if letter in self.alphabet:
                morse.append(self.alphabet[letter])
            # Attach punctuation or spaces as needed (periods are left out because .
            # is 'e' in Morse)
            if letter == '':
                morse.append('')
            if letter in self.punctuation:
                morse.append(self.punctuation[letter])
        return ' '.join(morse)

    def translate(self, morse):
        """
        Translates a Morse message into English
        """
        morse = morse.split(' ')
        english = []
        for code in morse:
            if code in self.code_list:
                x = self.code_list.index(code)
                english.append(self.alpha_list[x])
            # Attach punctuation or spaces as needed
            if code == '':
                english.append(' ')
            if code in self.punc_codes:
                index = self.punc_codes.index(code)
                english.append(self.punc_eng[index])
        return ''.join(english)
