import abc
from operator import methodcaller
import random


class Selector(metaclass=abc.ABCMeta):
    """ Selection of the fittest individuals among the population. """

    def __init__(self, rep=False):
        """ Initializes this selector.

        :param rep: If repetition of individuals is allowed. If true, there are chances of the same individual be
            selected again. Defaults to False.
        """
        self.__rep = rep

    @abc.abstractmethod
    def __call__(self, population, n=2):
        """ It makes the selection according to the subclass implementation.

        :param n: The number of individuals to return. Defaults to 2.
        :param population: The population from which select the individuals.
        :return: A list of individuals in case of n > 1 or one individual in case of n = 1.
        """
        raise NotImplementedError()

    @property
    def rep(self):
        """ Property that tells whether the same individual can be selected repeatedly.

        :return: A value of True if it can be selected repeatedly, false otherwise.
        """
        return self.__rep


class BestIndividualSelector(Selector):
    """ Selects the best individual among the population. """

    def __call__(self, population, n=2):
        """ The selection is made by getting the bests individuals of all the population.

        If "rep" is activated, the returned individuals will be n times the best individual. If False, the returned
        individuals will be the n best individuals.

        :param n: The number of individuals to return. Defaults to 2.
        :param population: The population from which select the individuals.
        :return: A list of individuals in case of n > 1 or one individual in case of n = 1.
        """
        return [population[0] for _ in range(n)] if self.rep else population[:n] if n > 1 else population[0]


class FitnessProportionateSelector(Selector):
    """ Selects individuals by a probability proportional to their finesses. """

    def __call__(self, population, n=2):
        """ The selection is made by getting randomly the individuals with higher probability those with higher fitness.

        The probability to be selected is proportional to the magnitude of the fitness of the individual among the
        population (i.e. very high fitness implies very high probability to be selected).

        If "rep" is activated, the returned individuals may be repeated.

        :param n: The number of individuals to return. Defaults to 2.
        :param population: The population from which select the individuals.
        :return: A list of individuals in case of n > 1 or one individual in case of n = 1.
        """
        # TODO Implement
        raise NotImplementedError()


class PositionProportionateSelector(Selector):
    """ Selects individuals by a probability proportional to their position in a list ordered by fitness. """

    def __call__(self, population, n=2):
        """ The selection is made by getting randomly the individuals with higher probability those with higher fitness.

        The probability to be selected is proportional to the position of the fitness of the individual among the
        population (i.e. those with better fitness have better positions, but a very high fitness doesn't implies more
        chances to be selected).

        If "rep" is activated, the returned individuals may be repeated.

        :param n: The number of individuals to return. Defaults to 2.
        :param population: The population from which select the individuals.
        :return: A list of individuals in case of n > 1 or one individual in case of n = 1.
        """
        # TODO Implement
        raise NotImplementedError()


class TournamentSelector(Selector):
    """ Selects the best individuals among a random sample of the whole population. """

    def __init__(self, m, rep=False):
        """ Initializes this selector.

        :param m: The size of the random sample of individuals to pick prior to the selection of the fittest.
        :param rep: If repetition of individuals is allowed. If true, there are chances of the same individual be
            selected again. Defaults to False.
        """
        super().__init__(rep)
        self.__m = m

    def __call__(self, population, n=2):
        """ The selection is made by doing as many tournaments as individuals to be selected.

        To do it, a sample of individuals will be selected randomly and, after that, the best individual of the sample
        is then selected.

        If "rep" is activated, the returned individuals may be repeated.

        :param n: The number of individuals to return. Defaults to 2.
        :param population: The population from which select the individuals.
        :return: A list of individuals in case of n > 1 or one individual in case of n = 1.
        """
        individuals = []
        while len(individuals) < n:
            individual = max(random.sample(population, self.__m), key=methodcaller('fitness'))
            if self.rep:
                individuals.append(individual)
            elif individual not in individuals:
                individuals.append(individual)
        return individuals[:n] if n > 1 else individuals[0]


class UniformSelector(Selector):
    """ Selects individuals randomly from the population. """

    def __call__(self, population, n=2):
        """ Selects n individuals randomly from the population following a uniform distribution.

        :param population: The population from which select the individuals.
        :param n: The number of individuals to return. Defaults to 2.
        :return: A tuple of individuals in case of n > 1 or one individual in case of n = 1
        """
        if n > 1:
            return [random.choice(population) for _ in range(n)] if self.rep else random.sample(population, n)
        else:
            return random.choice(population)
