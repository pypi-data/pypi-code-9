import random

from pynetics import UnexpectedClassError


def take_chances(probability=0.5):
    """ Given a probability, the method generates a random value to see if is
        lower or not than that probability.

    :param probability: The value of the probability to beat. Default is 0.5.
    :return: A value of True if the value geneated is bellow the probability
        specified, and false otherwise.
    """
    return random.random() < probability


# Validations
def check_is_instance_of(value, cls):
    """ Checks if a value is instance of a given class.

    If the value is an instance of the class, he method will return the value as
    is. Otherwise, it will raise an error.

    :param value: The value to be checked.
    :param cls: The class to be checked on.
    :return: The value.
    :raises UnexpectedClassError: In case of the value is not an instance of the
        given class.
    """
    if not isinstance(value, cls):
        raise UnexpectedClassError(cls)
    else:
        return value
