from unittest import mock, TestCase
from pynetics.stop import StepsNumStopCondition


class TestStepsNumStopCondition(TestCase):
    """ Test for the stop condition based on number of iterations. """

    def test_criteria_is_not_met_with_fewer_iterations(self):
        stop_condition = StepsNumStopCondition(2)
        genetic_algorithm = mock.Mock()
        genetic_algorithm.generation = 0
        self.assertFalse(stop_condition(genetic_algorithm))
        genetic_algorithm.generation = 1
        self.assertFalse(stop_condition(genetic_algorithm))

    def test_criteria_is_not_met_with_same_or_more_iterations(self):
        genetic_algorithm = StepsNumStopCondition(2)
        population = mock.Mock()
        population.generation = 2
        self.assertTrue(genetic_algorithm(population))
        population.generation = 3
        self.assertTrue(genetic_algorithm(population))
