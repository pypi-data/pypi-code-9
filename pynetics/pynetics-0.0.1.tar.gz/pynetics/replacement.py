import abc


class Replacement(metaclass=abc.ABCMeta):
    """ Replacement of individuals of the population. """

    @abc.abstractmethod
    def __call__(self, population, offspring):
        """ It makes the replacement according to the subclass implementation.

        :param population: The population where make the replacement.
        :param offspring: A list of individuals to be inserted in the population.
        """
        raise NotImplementedError()


class LowElitistReplacement(Replacement):
    """ Replacement removing the less fit individuals (from population) and thus inserting the offspring afterwards. """

    def __call__(self, population, offspring):
        """ Removes the less fit individuals from population and inserts the offspring afterwards.

        The number of individuals in the offspring will be the same as the number of individuals to be removed from the
        population BEFORE the insertion of the offspring. This makes this operator elitist, but at least not as much as
        the HighElitistReplacement operator.

        :param population: The population where make the replacement.
        :param offspring: A list of individuals to be inserted in the population.
        """
        population.extend(offspring)
        [population.remove(population[-1]) for _ in offspring]


class HighElitistReplacement(Replacement):
    """ Replacement dropping the less fit individuals among all (those from population plus the offspring). """

    def __call__(self, population, offspring):
        """ Inserts the offspring in the population and removes the less fit.

        The number of individuals in the offspring will be the same as the number of individuals to be removed from the
        population AFTER the insertion of the offspring. This makes this operator highly elitist.

        :param population: The population where make the replacement.
        :param offspring: A list of individuals to be inserted in the population.
        """
        population.extend(offspring)
        [population.remove(population[-1]) for _ in offspring]
