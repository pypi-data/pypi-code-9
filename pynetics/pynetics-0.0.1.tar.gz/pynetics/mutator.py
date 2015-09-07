import abc
import random


class Mutator(metaclass=abc.ABCMeta):
    """ Defines the behaviour of a genetic algorithm mutation operator. """

    @abc.abstractmethod
    def __call__(self, individual):
        """ Implementation of the mutation operation.

        The mutation implementation must be aware of the implementation type. Given that not all the implementations are
        the same, not all the mutation operations may work.

        :param individual: a chromosome to mutate.
        :returns: A new mutated individual.
        """
        raise NotImplementedError()


class SwapSingleGeneChromosomeListMutator(Mutator):
    """ The mutated individual is obtained by swapping two random genes.

    The mutated individual is obtained by swapping two random genes as seen in the next example:

    individual : 12345678
    pivot      : 3, 5
    -----------
    mutated    : 12365478
    """

    def __call__(self, individual):
        # TODO TBD
        new_individual = individual.clone()
        genes = random.sample(range(len(new_individual) - 1), 2)
        g1, g2 = genes[0], genes[1]
        new_individual.chromosome[g1], new_individual.genes[g2] = new_individual.genes[g2], new_individual.genes[g1]
        return new_individual


class RandomGeneAlphabetListMutator(Mutator):
    """ The mutated individual is obtained by changing random genes to values belonging to the chromosome's alphabet.

    The mutated chromosome is obtained by changing N random genes as seen in the next example:

    individual : aabbaaba
    alleles    : (a, b, c, d)
    -----------
    mutated    : aabdaabc
    """

    def __call__(self, individual):
        # TODO TBD
        new_individual = individual.clone()
        i = random.choice(range(len(individual)))
        new_individual.chromosome[i] = new_individual.alleles.get()
        return new_individual
