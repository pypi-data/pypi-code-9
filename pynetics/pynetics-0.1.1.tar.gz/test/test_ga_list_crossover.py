from unittest import TestCase, mock

from pynetics.ga_list import ListIndividual, OnePointCrossover, \
    RandomMaskCrossover, TwoPointCrossover


class ListCrossoverTestCase(TestCase):
    """ Common config for all crossover methods. """

    def setUp(self):
        self.i1, self.i2, self.i3, self.i4 = tuple(
            [ListIndividual() for _ in range(4)]
        )
        self.i1.extend('AAAAAAA')
        self.i2.extend('CCCCCCC')
        self.i3.extend('TTTTTT')

        population = mock.Mock()
        def f():
            l = ListIndividual()
            l.extend('AAAAAAA')
            return l
        population.spawn = f
        self.i1.population = population
        self.i2.population = population
        self.i3.population = population


class TestOnePointCrossover(ListCrossoverTestCase):
    """ Set of tests for one point crossover method. """

    def test_different_lengths_leads_to_an_error(self):
        """ Error when chromosomes has different length. """
        crossover = OnePointCrossover()
        with self.assertRaises(ValueError):
            crossover([self.i1, self.i3])

    def test_crossover_is_performed(self):
        """ Checks that one point crossover works as expected. """
        crossover = OnePointCrossover()
        progeny = crossover([self.i1, self.i2])

        self.assertEqual(len(progeny), 2)
        c1, c2 = progeny[0], progeny[1]
        self.assertEqual(len(c1), len(c2))
        self.assertIsInstance(c1, ListIndividual)
        self.assertIsInstance(c2, ListIndividual)

        for i in range(len(c1)):
            # TODO Not in the mood. Please future me, rewrite it latter
            self.assertTrue(
                c1[i] == self.i1[i] and c2[i] == self.i2[i] or c1[i] == self.i2[
                    i] and c2[i] == self.i1[i])


class TestTwoPointCrossover(ListCrossoverTestCase):
    def test_different_lengths_leads_to_an_error(self):
        """ Error when chromosomes has different length. """
        crossover = TwoPointCrossover()
        with self.assertRaises(ValueError):
            crossover([self.i1, self.i3])

    def test_crossover_is_performed(self):
        """ Checks that one point crossover works as expected. """
        crossover = TwoPointCrossover()
        progeny = crossover([self.i1, self.i2])

        self.assertEqual(len(progeny), 2)
        c1, c2 = progeny[0], progeny[1]
        self.assertEqual(len(c1), len(c2))
        self.assertIsInstance(c1, ListIndividual)
        self.assertIsInstance(c2, ListIndividual)

        for i in range(len(c1)):
            # TODO Not in the mood. Please future me, rewrite it latter
            self.assertTrue(
                c1[i] == self.i1[i] and c2[i] == self.i2[i] or c1[i] == self.i2[
                    i] and c2[i] == self.i1[i])


class TestRandomMaskCrossover(ListCrossoverTestCase):
    def test_different_lengths_leads_to_an_error(self):
        """ Error when chromosomes has different length. """
        crossover = RandomMaskCrossover()
        with self.assertRaises(ValueError):
            crossover([self.i1, self.i3])

    def test_crossover_is_performed(self):
        """ Checks that one point crossover works as expected. """
        crossover = RandomMaskCrossover()
        progeny = crossover([self.i1, self.i2])

        self.assertEqual(len(progeny), 2)
        c1, c2 = progeny[0], progeny[1]
        self.assertEqual(len(c1), len(c2))
        self.assertIsInstance(c1, ListIndividual)
        self.assertIsInstance(c2, ListIndividual)

        for i in range(len(c1)):
            # TODO Not in the mood. Please future me, rewrite it latter
            self.assertTrue(
                c1[i] == self.i1[i] and c2[i] == self.i2[i] or c1[i] == self.i2[
                    i] and c2[i] == self.i1[i])
