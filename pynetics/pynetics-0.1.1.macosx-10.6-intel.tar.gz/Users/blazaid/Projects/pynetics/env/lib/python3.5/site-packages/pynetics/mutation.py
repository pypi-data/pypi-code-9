import abc


class MutateMethod(metaclass=abc.ABCMeta):
    """ Defines the behaviour of a genetic algorithm mutation operator. """

    def __call__(self, individual):
        """ Applies the crossover method to the list of individuals.

        :param individual: an individual to mutate.
        :returns: A new mutated individual.
        """
        return self.perform(individual)

    @abc.abstractmethod
    def perform(self, individual):
        """ Implementation of the mutation operation.

        The mutation implementation must be aware of the implementation type.
        Given that not all the implementations are the same, not all the
        mutation operations may work.

        :param individual: an individual to mutate.
        :returns: A new mutated individual.
        """


class NoMutation(MutateMethod):
    """ A mutation method where no method is applied to the individual. """

    def perform(self, individual):
        """ Return the same individual passed as parameter. """
        return individual
