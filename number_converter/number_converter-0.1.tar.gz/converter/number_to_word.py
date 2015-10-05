from abc import ABCMeta, abstractmethod

class NumberToWord(object):
    """
    Abstract class composed by two methods
    __init__ and convert_to_word
    Both methods are needed when inherited
    from the other classes. 
    Since python doesn't have real abstract
    classes the ABCMeta class is used and
    the decorator abstracmethod.
    __init__ is not an abstract method
    since the other inherited classes must
    have a number and the word representation.
    """
    __metaclass__ = ABCMeta

    def __init__(self, number):
        """
        params: 
            number
        class attributes: 
            self.number, self.word(string)
        note:
            self.number is going to have the type send it
            in the implementation classes.
        """
        self.number = number
        self.word = ''

    @abstractmethod
    def convert_number_to_word(self):
        """
        params:
            None
        note:
            Function to convert the number to it's word
            representation. The implementation it's going
        to be in the inherited classes.
        """
        pass
