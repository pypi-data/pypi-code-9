from functools import partial
import isbn_validator
import re
import isbnlib

# nosier "/usr/bin/python utils.py"

def is_valid_isbn(isbn):
    return isbn_validator.is_valid_isbn(isbn)

def normalizeISBN(isbn):
    """
    >>> normalizeISBN('978800105473-4')
    '978-80-01-05473-4'

    >>> normalizeISBN('80978800105473-4')
    '80978800105473-4'

    >>> normalizeISBN('988800105473-4')
    '988800105473-4'

    >>> normalizeISBN('978-80-254-94677')
    '978-80-254-9467-7'
    """
    try:
        return isbnlib.mask(isbnlib.canonical(isbn))
    except isbnlib.NotValidISBNError:
        return isbn

    #result =  re.search(r'^(978)(80)(.{7})(.)$', isbn.replace('-',''))
    #formatedISBN = (result and "-".join(result.groups())) or isbn
    #return formatedISBN
    #return isbn

if __name__ == "__main__":
    import doctest
    doctest.testmod()
