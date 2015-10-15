from unittest import TestCase, mock

from pynetics import SpawningPool, FitnessMethod, Population, \
    InvalidPopulationSizeError, GeneticAlgorithm
from pynetics.ga_list import ListIndividual


class DummySpawningPool(SpawningPool):
    """ A spawning pool just for tests. """

    def __init__(self, individuals):
        """ Initializes this spawning pool with 10 predefined individuals. """
        self.i = 0
        self.n = len(individuals)
        self.individuals = individuals[:]

    def create(self):
        """ Return one of the individuals in the list, consecutively. """
        if self.i == self.n:
            self.i = 0
        individual = self.individuals[self.i % self.n]
        self.i += 1
        return individual


class DummyFitness(FitnessMethod):
    """ A fitness just for tests. """

    def perform(self, individual):
        """ The more 1 an individual has in its list, the fittest it is. """
        return sum(x for x in individual)


class TestPopulation(TestCase):
    """ Test for populations. """
    # TODO Tests to check that the order of individuals is respected.
    # TODO Tests valid input parameters

    def get_genetic_algorithm(self):
        ga = mock.Mock(spec=GeneticAlgorithm)
        return ga

    def individuals(self, n):
        individuals = []
        for i in range(10):
            individual = ListIndividual()
            for j in range(n):
                individual.append(0 if j <= i else 1)
            individuals.append(individual)
        return individuals

    def test_cannot_initialize_a_population_of_size_0_or_less(self):
        for size in (-1, 0):
            with self.assertRaises(InvalidPopulationSizeError):
                Population(
                    self.get_genetic_algorithm(),
                    size,
                    5,
                    DummySpawningPool(self.individuals(3)),
                    DummyFitness(),
                )

    def test_population_is_created_correctly(self):
        """ Population is created fine when parameters are ok. """
        individuals = self.individuals(10)

        population = Population(
            self.get_genetic_algorithm(),
            10,
            5,
            DummySpawningPool(individuals),
            DummyFitness(),
        )
        for i in individuals:
            self.assertIn(i, population)

    def test_spawns_generates_individuals(self):
        """ Calling spawn actually generates individuals. """
        individuals = self.individuals(10)
        population = Population(
            self.get_genetic_algorithm(),
            len(individuals),
            len(individuals),
            DummySpawningPool(individuals),
            DummyFitness(),
        )
        for i in individuals:
            spawned_individual = population.spawn()
            self.assertIsInstance(spawned_individual, ListIndividual)
            self.assertEquals(i, spawned_individual)

    def test_extend_population_increases_the_size_of_the_population(self):
        size = 5
        individuals = self.individuals(2 * size)
        population = Population(
            self.get_genetic_algorithm(),
            size,
            size - 1,
            DummySpawningPool(individuals[:size]),
            DummyFitness(),
        )
        self.assertEquals(size, len(population))
        for i in individuals[:size]:
            self.assertIn(i, population)
        for i in individuals[size:]:
            self.assertNotIn(i, population)
        population.extend(individuals[size:])
        self.assertEquals(2 * size, len(population))
        for i in individuals:
            self.assertIn(i, population)
