import abc


class StopCriteria(metaclass=abc.ABCMeta):
    """ A criteria to be met in order to stop the algorithm. """

    @abc.abstractmethod
    def __call__(self, ga):
        """ Checks if this stop criteria is met.

        :param ga: The genetic algorithm to check.
        :return: True if criteria is met, false otherwise.
        """
        raise NotImplementedError()


class ConvergenceStopCriteria:
    """ Defines a functor that checks the convergence of the population. """

    def __init__(self, epsilon=None):
        """ Initializes this function with an optional epsilon.

        The epsilon will be used as thresshold. If not None, the population converged if the maximum difference between
        fitnesses is lesser or equal to epsilon. If None, all fitnesses must be equal.

        :param epsilon: A float value.
        """
        self.__epsilon = epsilon

    def __call__(self, ga):
        """ Checks if this stop criteria is met.

        It will look at the fitness of both the best and the worst individual of the population. If they are the same or
        at least very close (thats the why of the epsilon param at initialization time), the population converged and
        thus the criteria is met.

        :param ga: The genetic algorithm to check.
        :return: True if criteria is met, false otherwise.
        """
        if self.__epsilon is not None:
            return abs(ga.population[0].fitness() - ga.population[-1].fitness()) <= self.__epsilon
        else:
            return ga.population[0].fitness() == ga.population.fitness()


class IterationStopCriteria:
    """ Defines a functor that checks if the genetic algorithm has made enought iterations. """

    def __init__(self, iterations):
        """ Initializes this function with the number of iterations.

        :param iterations: An integer value.
        """
        self.__iterations = iterations

    def __call__(self, ga):
        """ Checks if this stop criteria is met.

        It will look at the iteration of the genetic algorithm. If it's greater or equal to the specified in
        initialization method, the criteria is met.

        :param ga: The genetic algorithm to check.
        :return: True if criteria is met, false otherwise.
        """
        return ga.iteration >= self.__iterations
