import abc

from pynetics import take_chances


# TODO I'm not proud of this methods. I think they performance may be improved.

class CatastropheMethod(metaclass=abc.ABCMeta):
    """ Defines the behaviour of a genetic algorithm catastrophe operator.

    It's expected that this operator keep track of when to act, since it will be
    called every step of the algorithm after replacement operation.
    """

    def __call__(self, population):
        """ Tries to apply the catastrophic operator to the population.

        This method does some checks and the delegates the application of the
        catastrophic operator to the "perform" method.

        :param population: The population where apply the catastrophic method.
        """
        if population is None:
            raise ValueError('The population cannot be None')
        else:
            return self.perform(population)

    @abc.abstractmethod
    def perform(self, population):
        """ Implementation of the catastrophe operation.

        :param population: the population which may suffer the catastrophe
        """


class NoCatastrophe(CatastropheMethod):
    """ A catastrophe method where nothing happens. """

    def perform(self, population):
        """ It's a wonderful world and nothing happens.

        :param population: The poppulation where nothing happens. Ever.
        """
        pass


class ProbabilityBasedCatastrophe(CatastropheMethod, metaclass=abc.ABCMeta):
    """ Base class for some bundled probability based catastrophe methods.

    This method will have a probability to be triggered. Is expected this
    probability to be very little.
    """

    def __init__(self, probability):
        """ Initializes this catastrophe method.

        :param probability: The probability fot the catastrophe to happen.
        """
        self.__probability = probability

    def perform(self, population):
        if take_chances(self.__probability):
            self.perform_catastrophe()

    @abc.abstractmethod
    def perform_catastrophe(self, population):
        """ Returns a list of the individuals to remove from population.

        :param population: The population from where extract individuals.
        :return: The individuals to retain after the catastrophe application.
        """


class PackingByProbability(ProbabilityBasedCatastrophe):
    """ Replaces all repeated individuals maintaining only one copy of each. """

    def perform_catastrophe(self, population):
        """ Replaces all repeated individuals by new ones.

        :param population: The population where apply the catastrophe.
        """
        visited_individuals = []
        for i in range(len(population)):
            if population[i] in visited_individuals:
                population[i] = population.spawn()
            visited_individuals.append(population[i])


class DoomsdayByProbability(ProbabilityBasedCatastrophe):
    """ Replaces all but the best individual. """

    def perform_catastrophe(self, population):
        """ Replaces all the individuals but the best.

        :param population: The population where apply the catastrophe.
        """
        for i in range(1, len(population)):
            population[i] = population.spawning_pool.create()
