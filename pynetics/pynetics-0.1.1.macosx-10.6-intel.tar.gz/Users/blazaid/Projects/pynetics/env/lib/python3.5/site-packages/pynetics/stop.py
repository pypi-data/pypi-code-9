import abc


class StopCondition(metaclass=abc.ABCMeta):
    """ A condition to be met in order to stop the algorithm.

    Although the stop condition is defined as a class, it's enough to provide a
    function that is able to discern whether the time has come to stop (True or
    False) receiving as parameter the population.
    """

    @abc.abstractmethod
    def __call__(self, genetic_algorithm):
        """ Checks if this stop condition is met.

        :param genetic_algorithm: The genetic algorithm where this stop
            condition belongs.
        :return: True if criteria is met, false otherwise.
        """


class StepsNumStopCondition(StopCondition):
    """ If the genetic algorithm has made enough iterations. """

    def __init__(self, steps):
        """ Initializes this function with the number of iterations.

        :param steps: An integer value.
        """
        self.__steps = steps

    def __call__(self, genetic_algorithm):
        """ Checks if this stop criteria is met.

        It will look at the generation of the genetic algorithm. It's expected
        that. If its generation is greater or equal to the specified in
        initialization method, the criteria is met.

        :param genetic_algorithm: The genetic algorithm where this stop
            condition belongs.
        :return: True if criteria is met, false otherwise.
        """
        return genetic_algorithm.generation >= self.__steps
