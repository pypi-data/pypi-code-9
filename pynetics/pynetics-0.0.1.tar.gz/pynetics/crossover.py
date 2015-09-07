import abc
import random
from pynetics.utils import test_chances


class Crossover(metaclass=abc.ABCMeta):
    """ Defines the behaviour of a genetic algorithm crossover operator. """

    @abc.abstractmethod
    def __call__(self, i1, i2):
        """ Implementation of the crossover operation.

        The crossover implementation must be aware of the individual type. Given that not all the implementations are
        the same, not all the crossover operations may work.

        :param i1: An individual to cross.
        :param i2: Another individual to cross.
        :returns: Two individuals with characteristics of both parents.
        """
        raise NotImplementedError()


class OnePointCrossover(Crossover):
    """ Child individuals are constructed by mixing the parents using one random pivot point.

    This crossover implementation works only with individuals of type ListIndividual.
    """

    def __call__(self, i1, i2):
        """ The offspring is obtained mixing the parents with one pivot point crossover.

        One example:

        parents : aaaaaaaa, bbbbbbbb
        pivot   : 3
        -----------
        childs  : aaabbbbb, bbbaaaaa

        :param i1:
        :param i2:
        :return:
        """
        # TODO TBD
        child1, child2 = i1.clone(), i2.clone()

        pivot = random.randint(0, min(len(i1), len(i2)) - 1)
        child1.chromosome = i2.chromosome[:pivot] + i1.chromosome[pivot:]
        child2.chromosome = i1.chromosome[:pivot] + i2.chromosome[pivot:]
        return child1, child2


class TwoPointCrossover(Crossover):
    """ Crossover subclass where childs are constructed by mixing the parents
    using two random pivot points.

    The childs are obtained mixing the parents with two pivot points crossover,
    as seen in the next example:

    parents : aaaaaaaa, bbbbbbbb
    pivot   : 3, 5
    -----------
    childs  : aaabbaaa, bbbaabbb
    """

    def __call__(self, i1, i2):
        child1, child2 = i1.clone(), i2.clone()

        pivots = random.sample(range(min(len(i1), len(i2)) - 1), 2)
        p, q = min(pivots[0], pivots[1]), max(pivots[0], pivots[1])
        child1.chromosome = i2.chromosome[:p] + i1.chromosome[p:q] + i2.chromosome[q:]
        child2.chromosome = i1.chromosome[:p] + i2.chromosome[p:q] + i1.chromosome[q:]
        return child1, child2


class RandomMaskCrossover(Crossover):
    # TODO TBD
    """

    parents     : aaaaaaaa, bbbbbbbb
    random mask : 00100110
    -----------
    childs      : aabaabba, bbabbaab
    """

    def __call__(self, i1, i2):
        child1, child2 = i1.clone(), i2.clone()
        for i in range(len(i1)):
            if test_chances(.5):
                child1.chromosome[i] = i1.chromosome[i]
                child2.chromosome[i] = i2.chromosome[i]
            else:
                child1.chromosome[i] = i2.chromosome[i]
                child2.chromosome[i] = i1.chromosome[i]
        return child1, child2


class GeneralizedCrossover(Crossover):
    # TODO TBD
    """
    NOTE: Works only for individuals with list chromosomes of binary alleles. Ok, may work for other individuals with
    list chromosomes, but the results may be strange (and perhaps better!)
    """

    def __call__(self, i1, i2):
        # Obtain the crossover range (as integer values)
        a = int(''.join([str(b1 & b2) for (b1, b2) in zip(i1.chromosome, i2.chromosome)]), 2)
        b = int(''.join([str(b1 | b2) for (b1, b2) in zip(i1.chromosome, i2.chromosome)]), 2)

        # Get the children (as integer values)
        c = random.randint(a, b)
        d = b - (c - a)

        # Convert to chromosomes and we're finish
        child1, child2 = i1.clone(), i2.clone()
        child1.chromosome = [int(x) for x in bin(c)[2:]]
        child2.chromosome = [int(x) for x in bin(d)[2:]]
        return child1, child2


class MorphologicalCrossover(Crossover):
    # TODO TBD
    # TODO Let's see if it's possible to export diversity calc. to the population to mprove the performance.
    """
    NOTE: Works only for individuals with list chromosomes of real interval alleles.
    NOTE: The value of each gene must be normalized.
    """

    def __init__(self, a=-.001, b=-.133, c=.54, d=.226):
        self.__a = a
        self.__b = b
        self.__c = c
        self.__d = d

        self.__calc_1 = (b - a) / c
        self.__calc_2 = d / (1 - c)
        self.__calc_3 = self.__calc_2 * -c

    def __call__(self, i1, i2):
        child1, child2 = i1.clone(), i2.clone()
        for g in range(len(i1.chromosome)):
            genes_in_position_g = [i.chromosome[g] for i in i1.population.individuals]
            diversity = max(genes_in_position_g) + min(genes_in_position_g)

            phi = self.__phi(diversity)
            lower_bound = min(i1.chromosome[g], i2.chromosome[g]) + phi
            upper_bound = max(i1.chromosome[g], i2.chromosome[g]) - phi

            child1.chromosome[g] = random.uniform(lower_bound, upper_bound)
            child2.chromosome[g] = upper_bound - (child1.chromosome[g] - lower_bound)
        return child1, child2

    def __phi(self, x):
        return self.__calc_1 * x + self.__a if x <= self.__c else self.__calc_2 * x + self.__calc_3
