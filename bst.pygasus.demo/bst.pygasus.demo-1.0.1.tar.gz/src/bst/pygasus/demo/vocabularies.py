from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def card_availability(context):
    return SimpleVocabulary([
                            SimpleTerm(0, 'A', 'No Card'),
                            SimpleTerm(1, 'B', '1 Card'),
                            SimpleTerm(2, 'C', '2 Cards'),
                            SimpleTerm(3, 'D', '3 Cards'),
                            SimpleTerm(4, 'E', '4 Cards'),
                            SimpleTerm(5, 'F', '5 Cards')
                            ])
