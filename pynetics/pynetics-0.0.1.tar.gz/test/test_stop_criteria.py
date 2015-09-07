from unittest import mock, TestCase, main
from pynetics.stop_criteria import IterationStopCriteria


class TestIterationStopCriteria(TestCase):
    """ Test for the stop critera based on number of iterations. """

    def test_criteria_is_not_met_with_fewer_iterations(self):
        stop_criteria = IterationStopCriteria(2)
        ga = mock.Mock()
        ga.iteration = 0
        self.assertFalse(stop_criteria(ga))
        ga.iteration = 1
        self.assertFalse(stop_criteria(ga))

    def test_criteria_is_not_met_with_same_or_more_iterations(self):
        stop_criteria = IterationStopCriteria(2)
        ga = mock.Mock()
        ga.iteration = 2
        self.assertTrue(stop_criteria(ga))
        ga.iteration = 3
        self.assertTrue(stop_criteria(ga))


class TestConvergenceStopCriteria(TestCase):
    """ Test for the stop critera based on the convergence of the population. """
    # TODO Tests
    pass


if __name__ == '__main__':
    main()
