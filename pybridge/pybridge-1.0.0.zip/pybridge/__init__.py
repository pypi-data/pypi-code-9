import re

class atom():
    def __init__(self, types, value):
        self.types = types
        self.value = value

class grammar():
    def __init__(self, types, definitions, value, weight):
        self.definitions = definitions
        self.value = value
        self.types = types
        self.weight = weight

class definition():
    def __init__(self, type, pattern):
        self.type = type
        self.pattern = pattern
        self.regex = re.compile(pattern)

class bridge():
    def __init__(self):
        self.grammars = []

    def sort(self):
        self.grammars.sort(key = lambda grammar: grammar.weight)

    def match(self, definition, sample):
        for i in range(len(sample)):
            if not definition[i].type in sample[i].types:
                return False
            if not definition[i].regex.match(sample[i].value):
                return False
        return True

    def process(self, sentence):
        words = [atom(['word'], word) for word in sentence.split(" ")]
        self.sort()
        current_grammar = 0
        while current_grammar < len(self.grammars):
            for i in range(len(words)):
                grammar = self.grammars[current_grammar]
                if len(grammar.definitions) > len(words) - i:
                    break
                start = i
                end = start + len(grammar.definitions)
                sample = words[start:end]
                if self.match(grammar.definitions, sample):
                    current_grammar = -1
                    result = grammar.value.format(*[atom.value for atom in sample])
                    words[start:end] = [atom(grammar.types, result)]
                    break
            current_grammar += 1
        return words
