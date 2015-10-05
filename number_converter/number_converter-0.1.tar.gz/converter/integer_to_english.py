#!/usr/bin/env python

import sys
from number_to_word import NumberToWord

class IntegerToEnglish(NumberToWord):
    """
    IntegerToEnglish class inherits from abstract class
    NumberToWord and implements the method convert_number_to_word.
    Methods:
        public:
            __init__: Inherited from NumberToWord
            convert_number_to_word: Implemented from NumberToWord
        protected:
            _get_names_less_than_20
            _get_names_of_tens
            _get_names_of_big_numbers
            _get_exponent_value
            _convert_number_less_than_hundred
            _convert_number_to_word: Implemented from NumberToWord
            Note: In python if a method or function starts
                with _ it means it's a protected method.
    """

    def __init__(self, number):
        """
        Constructor of the class. First check if the number is
        of integer or long type if it's not it throws an TypeError. 
        Second checks if the number is bigger than the system
        max integer if is bigger it throws an OverflowError.
        This way if we change from a 64bits system to a 32bits
        system our class is going to work. Although python converts
        automatically to BigIntegers this way we can protect the
        system from really big numbers.
        """
        if type(number) is not int and type(number) is not long:
            raise TypeError('This class is only used with integer numbers')
        
        if number > 0 and number > sys.maxint:
            raise OverflowError('Number to big for the system')

        if number < 0 and number < (sys.maxint-1) * -1:
            raise OverflowError('Number to big for the system')

        super(IntegerToEnglish, self).__init__(number)

    def _get_names_less_than_20(self, number):
        """
        Get the name of the number below than twenty.
        Used an array since the index is the same as
        the number.
        """
        names_list = ['zero', 'one', 'two', 'three',
                'four', 'five', 'six', 'seven',
                'eight', 'nine', 'ten', 'eleven', 'twelve',
                'thirteen', 'fourteen', 'fifteen', 'sixteen',
                'seventeen', 'eighteen', 'nineteen']
        return names_list[number]

    def _get_names_of_tens(self, number):
        """
        Get the names of the tens starting from twenty.
        Used a dictionary. Easier to get the value
        """
        tens_names_dic = {20:'twenty', 30:'thirty', 40:'forty', 
                50:'fifty', 60:'sixty', 70:'seventy', 80:'eighty', 
                90:'ninety'}
        return tens_names_dic[number]

    def _get_names_of_big_numbers(self, exponent):
        """
        Get the names of the big number, starting with
        thousand, millions, billions. The key of the 
        dictionary is the value n of 10 ** n.
        Example: 10 ** 3 = 1000, 10 ** 6 = 10000, etc.
        """
        big_names_dic = {3:'thousand', 6:'million', 9:'billion',
                12:'trillion', 15:'quadrillion', 18:'quintillion'}

        return big_names_dic[exponent]

    def _get_exponent_value(self, number):
        """
        Get the value of the exponent. It adds 3 everytime
        until is greater than the number.
        """
        exponent = 0
        while 10 ** exponent <= number:
            exponent += 3
        return exponent

    def _convert_number_less_than_hundred(self, number):
        """
        Convert the number less than one hundred.
        Check if the modulus of 100 is less than twenty and call
        _get_names_less_than_20. If is bigger is going to call
        _get_names_of_tens and if if the last digit is not zero
        is going to call _get_names_less_than_twenty
        """

        if number % 100 < 20:
            self.word += '{0} '.format(self._get_names_less_than_20(number % 100))
        else:
            self.word += '{0} '.format(self._get_names_of_tens(number / 10 * 10))
            if number % 10 != 0:
                self.word = '{0}-{1} '.format(self.word[:-1], self._get_names_less_than_20(number % 10))

    def _convert_number_less_than_thousand(self, number):
        """
        Convert the number less than one thousand.
        Divide by 100 to get the leftmost digit and call 
        _get_names_less_than_20 since is going to be between 1-9
        Then if the mod of 100 is not zero call less hundred.
        TODO: self.number here is altered. Possible refactor to
            maintain the original value.
        """
        self.word += '{0} hundred '.format(self._get_names_less_than_20(number / 100))
        if number % 100 != 0:
            number %= 100
            self._convert_number_less_than_hundred(number)

    def _convert_number_to_word(self, number):
        """
        Convert integer to english word.
        Values less than 100. DONE
        Values less than 1000. DONE
        Values less than 1000000 DONE
        Values everyone else DONE
        Values negative DONE
        """
        temp_number = number
        if number < 100:
            self._convert_number_less_than_hundred(number)
        elif number < 1000:
            self._convert_number_less_than_thousand(number)
        else:
            exponent = self._get_exponent_value(number)
            while exponent != 0:
                number /= 10 ** (exponent - 3)
                if number > 0 and number < 100:
                    self._convert_number_less_than_hundred(number)
                elif number != 0:
                    self._convert_number_less_than_thousand(number)
                if number > 0 and exponent - 3 > 0:
                    self.word += '{0} '.format(self._get_names_of_big_numbers(exponent-3))
                if temp_number % 10 ** (exponent - 3) != 0:
                    number = temp_number % 10 ** (exponent - 3)
                    exponent -= 3
                else:
                    exponent = 0

    def convert_number_to_word(self):
        """
        This public method checks if the number is negative. If
        its negative it adds Minus and called the protected method 
        _convert_number_to_word with the number * -1. So our 
        original method behaves the same.
        """
        if self.number < 0:
            self.word = 'Minus '
            self._convert_number_to_word(self.number * -1)
        else:
            self._convert_number_to_word(self.number)
        self.word = self.word.strip() # getting rid of the last space
                

if __name__ == '__main__':
    number_to_word = IntegerToEnglish(int(sys.argv[1]))
    number_to_word.convert_number_to_word()
    print number_to_word.word
