import abc
import operator
import random


class SelectionMethod(metaclass=abc.ABCMeta):
    """ Selection of the fittest individuals among the population.

    The selection method is defined as a class. However, it is enough to provide
    as a selection method a function that receives a village and a number of
    individuals, and returns a sample of individuals of that size from the given
    population.
    """

    def __init__(self, rep=False):
        """ Initializes this selector.

        :param rep: If repetition of individuals is allowed. If true, there are
            chances of the same individual be selected again. Defaults to False.
        """
        self.__rep = rep

    def __call__(self, population, n):
        """ Makes some checks to the configuration before delegating selection.

        After checking the parameters, the selection is performed by perform
        method.

        :param population: The population from which select the individuals.
        :param n: The number of individuals to return.
        :return: A list of individuals.
        :raises ValueError: If length of the population is smaller than the
            number of individuals to select and the repetition parameter is set
            to False (i.e. the same Individual cannot be selected twice or more
            times).
        """
        if not self.rep and len(population) < n:
            raise ValueError()
        else:
            return self.perform(population, n)

    @abc.abstractmethod
    def perform(self, population, n):
        """ It makes the selection according to the subclass implementation.

        :param population: The population from which select the individuals.
        :param n: The number of individuals to return.
        :return: A list of n individuals.
        """

    @property
    def rep(self):
        """ Returns if the same individual can be selected repeatedly. """
        return self.__rep


class BestIndividualSelection(SelectionMethod):
    """ Selects the best individuals among the population. """

    def perform(self, population, n):
        """ Gets the top n individuals out of all the population.

        If "rep" is activated, the returned individuals will be n times the best
        individual. If False, the returned individuals will be the top n
        individuals.

        :param population: The population from which select the individuals.
        :param n: The number of individuals to return.
        :return: A list of n individuals.
        """
        return [population[0] for _ in range(n)] if self.rep else population[:n]


class ProportionalToPositionSelection(SelectionMethod):
    """ Selects individuals randomly proportionally to their position. """

    def perform(self, population, n):
        """ Gets randomly the individuals, giving more probability to those in
        first positions of the population, i.e. those fittest.

        The probability to be selected is proportional to the position of the
        fitness of the individual among the population (i.e. those with better
        fitness have better positions, but a very high fitness doesn't implies
        more chances to be selected).

        If "rep" is activated, the returned individuals may be repeated.

        :param n: The number of individuals to return.
        :param population: The population from which select the individuals.
        :return: A list of n individuals.
        """
        # TODO Implement
        raise NotImplementedError()


class TournamentSelection(SelectionMethod):
    """ Selects best individuals of a random sample of the whole population. """

    def __init__(self, m, rep=False):
        """ Initializes this selector.

        :param m: The size of the random sample of individuals to pick prior to
            the selection of the fittest.
        :param rep: If repetition of individuals is allowed. If true, there are
            chances of the same individual be selected again. Defaults to False.
        """
        super().__init__(rep)
        self.__m = m

    def perform(self, population, n):
        """ Gets the best individuals from a random sample of the population.

        To do it, a sample of individuals will be selected randomly and, after
        that, the best individual of the sample is then selected. This process
        (i.e. extract sample and the get best individual from sample) is done
        as many times as individuals to be selected.

        If "rep" is activated, the returned individuals may be repeated.

        :param n: The number of individuals to return.
        :param population: The population from which select the individuals.
        :return: A list of n individuals.
        """
        individuals = []
        while len(individuals) < n:
            sample = random.sample(population, self.__m)
            individual = max(sample, key=operator.methodcaller('fitness'))
            if not self.rep or individual not in individuals:
                individuals.append(individual)
        return individuals


class UniformSelection(SelectionMethod):
    """ Selects individuals randomly from the population. """

    def perform(self, population, n):
        """ Selects n individuals randomly from the population.

        The selection is done by following a uniform distribution along the
        entire population.

        :param population: The population from which select the individuals.
        :param n: The number of individuals to return.
        :return: A list of n individuals.
        """
        if self.rep:
            return [random.choice(population) for _ in range(n)]
        random.sample(population, n)
