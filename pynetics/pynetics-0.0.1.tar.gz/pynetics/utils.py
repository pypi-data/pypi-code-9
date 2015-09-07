import random


def test_chances(probability=0.5):
    """ Given a probability, the method generates a random value to see if is lower or not than that probability.

    :param probability: The value of the probability to beat. Default is 0.5.
    :return: A value of True if the value geneated is bellow the probability specified, and false otherwise.
    """
    return random.random() < probability
