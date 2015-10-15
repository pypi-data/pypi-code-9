import abc


class CrossoverMethod(metaclass=abc.ABCMeta):
    """ Defines the behaviour of a genetic algorithm crossover operator. """

    parents_num = None

    def __call__(self, individuals):
        """ Applies the crossover method to the list of individuals.

        :param individuals: The individuals to cross to generate progeny.
        :returns: A list of individuals with characteristics of the parents.
        """
        if len(individuals) != self.get_parents_num():
            raise ValueError('Expected {} individuals but got {}'.format(
                self.get_parents_num(),
                len(individuals)
            ))
        else:
            return self.perform(individuals)

    def get_parents_num(self):
        """ Returns the number of parents expected in the crossover method. """
        return self.parents_num

    @abc.abstractmethod
    def perform(self, individuals):
        """ Algorithm for this crossover method.

        The crossover implementation must be aware of the individual type. Given
        that not all the implementations are the same, not all the crossover
        operations may work.

        :param individuals: The individuals to cross to generate progeny.
        :return: A list of individuals.
        """


class NoCrossover(CrossoverMethod):
    """ A crossover method where no method is applied to the individuals. """

    def __init__(self, parents_num):
        """ Initializes the crossover method,

        :param parents_num: The parents num this crossover method expects.
        """
        self.parents_num = parents_num

    def perform(self, individuals):
        """ Return the same individuals passed as parameter. """
        return individuals
