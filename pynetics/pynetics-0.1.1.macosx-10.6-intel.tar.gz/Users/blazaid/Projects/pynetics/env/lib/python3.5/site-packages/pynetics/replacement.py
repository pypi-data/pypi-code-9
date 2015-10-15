import abc


class ReplaceMethod(metaclass=abc.ABCMeta):
    """ Replacement of individuals of the population. """

    def __call__(self, population, offspring):
        """ Performs some checks before applying the replacement method.

        :param population: The population where make the replacement.
        :param offspring: The new population to use as replacement.
        :raises ValueError: If the number of individuals in population is lower
            than the number of individuals in the offspring.
        """
        if len(offspring) > len(population):
            raise ValueError('The offspring is higher than population')
        else:
            return self.perform(population, offspring)

    @abc.abstractmethod
    def perform(self, population, offspring):
        """ It makes the replacement according to the subclass implementation.

        :param population: The population where make the replacement.
        :param offspring: The new population to use as replacement.
        """

class LowElitism(ReplaceMethod):
    """ Low elitism replacement.

    The method will replace the less fit individuals by the ones specified in
    the offspring. This makes this operator elitist, but at least not much.
    Moreover, if offspring size equals to the population size then it's a full
    replacement (i.e. a generational scheme).
    """

    def perform(self, population, offspring):
        """ Removes less fit individuals and then inserts the offspring.

        :param population: The population where make the replacement.
        :param offspring: The new population to use as replacement.
        """
        del population[-len(offspring):]
        population.extend(offspring)


class HighElitism(ReplaceMethod):
    """ Drops the less fit individuals among all (population plus offspring).

    The method will add all the individuals in the offspring to the population,
    removing afterwards those individuals less fit. This makes this operator
    highly elitist but if length os population and offspring are the same, the
    process will result in a full replacement, i.e. a generational scheme of
    replacement.
    """

    def perform(self, population, offspring):
        """ Inserts the offspring in the population and removes the less fit.

        :param population: The population where make the replacement.
        :param offspring: The new population to use as replacement.
        """
        population.extend(offspring)
        del population[-len(offspring):]
