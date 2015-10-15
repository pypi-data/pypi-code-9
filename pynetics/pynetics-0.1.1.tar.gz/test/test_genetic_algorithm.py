from unittest import TestCase

from pynetics import GeneticAlgorithm, FitnessMethod, SpawningPool
from pynetics.catastrophe import NoCatastrophe
from pynetics.crossover import NoCrossover
from pynetics.ga_list import ListIndividual
from pynetics.mutation import NoMutation
from pynetics.replacement import LowElitism
from pynetics.selection import BestIndividualSelection
from pynetics.stop import StepsNumStopCondition


class DummySpawningPool(SpawningPool):
    """ A spawning pool just for tests. """

    def create(self):
        """ Return one of the individuals in the list, consecutively. """
        l = ListIndividual()
        l.extend('1234567890')
        return l


class DummyFitness(FitnessMethod):
    def perform(self, individual):
        return 1


class TestGeneticAlgorithm(TestCase):
    def test_generations_pass(self):
        """ Generation increment works properly. """
        steps = 10
        ga = GeneticAlgorithm(
            StepsNumStopCondition(steps),
            [
                (100, 50, DummySpawningPool(), DummyFitness())
            ],
            BestIndividualSelection(),
            LowElitism(),
            NoCrossover(2),
            NoMutation(),
            NoCatastrophe(),
            0.75,
            0.1,
        )
        ga.run()
        self.assertEquals(ga.generation, steps)
