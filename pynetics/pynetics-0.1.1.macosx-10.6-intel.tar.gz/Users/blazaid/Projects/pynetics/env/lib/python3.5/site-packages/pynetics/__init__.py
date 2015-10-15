import abc
import random

from pynetics.exceptions import InvalidPopulationSizeError, \
    UnexpectedClassError, InvalidReplacementRateError
from pynetics.stop import StopCondition
from pynetics.utils import check_is_instance_of, take_chances

__version__ = '0.1.1'


class GeneticAlgorithm:
    """ Base class where the evolutionary algorithm works.

    More than one algorithm may exist so a base class is created for specify the
    contract required by the other classes to work properly.
    """

    def __init__(
            self,
            stop_condition,
            populations_desc,
            select_method,
            replace_method,
            crossover_method,
            mutate_method,
            catastrophe_method,
            p_crossover,
            p_mutation,
    ):
        """ Initializes the genetic algorithm with the defaults.

        The populations_desc param should follow certain rules in order to work
        in the way the genetic algorithm is intended:
        1.  The population size of each of the populations must be greater than
            or equal to 1. If not, there will be nothing to be evolved.
        2.  The replacement rate should be at least 1 (otherwise no individual
            will be replaced) and, at most, the population size (i.e. a total
            replacement also called generational scheme).
        3.  The spawning pool must be an instance of SpawningPool class (or any
            of their subclasses).
        4.  The fitness method must be an instance of FitnessMethod class (or
            any of its subclasses).

        :param stop_condition: The condition to be met in order to stop the
            genetic algorithm.
        :param populations_desc: The description of the populations to
            be created and evolved in this algorithm. It is expected to be a
            list of 4-tuple elements in the form (population_size, replacement
            rate, spawning_pool, fitness_method). For more information in the
            method description.
        :param select_method: The method to be used as selection scheme.
        :param replace_method: The method to be used as replacement scheme.
        :param crossover_method: The method to be used as crossover operator
            scheme.
        :param mutate_method: The method to be used as mutation operator scheme.
        :param catastrophe_method: The method to be used as catastrophe
            operation.
        :param p_crossover: Probability that individuals, after being selected,
            cross each other to produce offspring.
        :param p_mutation: Probability that an individual mutates.
        :raises InvalidPopulationSize: If the size specified in any of the
            population_descriptions is invalid.
        :raises InvalidReplacementRateError: If the replacement rate is lower
            than 1 or higher than population size.
        :raises UnexpectedClassError: If any of the input variables doesn't
            follow the contract required (i.e. doesn't inherit from a predefined
            class).
        """
        self.__stop_condition = check_is_instance_of(
            stop_condition,
            StopCondition
        )
        self.__populations_desc = populations_desc[:]
        self.__select = select_method
        self.__replace = replace_method
        self.__cross = crossover_method
        self.__mutate = mutate_method
        self.__catastrophe = catastrophe_method
        self.__p_crossover = p_crossover
        self.__p_mutation = p_mutation
        self.__generation = 0
        self.__populations = []

    def initialize(self):
        """ Called when starting the genetic algorithm to initialize it. """
        self.__generation = 0
        self.__populations = [
            Population(
                self,
                population_size,
                replacement_rate,
                spawning_pool,
                fitness_method,
            )
            for
            population_size, replacement_rate, spawning_pool, fitness_method
            in self.__populations_desc
            ]

    def run(self):
        """ Runs the simulation.

        The process is as follows: initialize populations and, while the stop
        condition is not met, do a new evolve step. This process relies in the
        abstract method "step".
        """
        self.initialize()
        while not self.__stop_condition(self):
            for population in self.populations:
                offspring = self.__generate_offspring(population)
                self.__replace(population, offspring)
                self.__catastrophe(population)
            self.__generation += 1

    def __generate_offspring(self, population):
        """ Generates an offspring of a population.

        :param population: The population from where obtain the offspring.
        :return: A list of individuals.
        """
        offspring = []
        while len(offspring) < population.replacement_rate:
            # Selection
            individuals = self.__select(
                population,
                self.__cross.get_parents_num()
            )
            # Crossover
            if take_chances(self.__p_crossover):
                progeny = self.__cross(individuals)
            else:
                progeny = individuals
            number_of_individuals_who_fit = min(
                len(progeny),
                population.replacement_rate - len(offspring)
            )
            progeny = random.sample(progeny, number_of_individuals_who_fit)
            # Mutation
            for individual in progeny:
                if take_chances(self.__p_mutation):
                    self.__mutate(individual)
            # Add progeny to the offspring
            offspring.extend(progeny)
        return offspring

    @property
    def generation(self):
        """ Returns the generation of this population. """
        return self.__generation

    @property
    def populations(self):
        """ Returns the populations being evolved. """
        return self.__populations


class Population(list):
    """ Manages a population of individuals. """

    def __init__(
            self,
            genetic_algorithm,
            size,
            replacement_rate,
            spawning_pool,
            fitness_method,
    ):
        """ Initializes the population, filling it with individuals

        Because operators requires to know which individual is the fittest,
        others which is the less fit and others need to travel along the
        collection of individuals in some way or another (e.g. from fittest to
        less fit), the population is always sorted when an access is required.
        Thus, writing population[0] always returns the fittest individual,
        population[1] the next and so on, until population[-1] which is the less
        fit.

        :param genetic_algorithm: The genetic algorithm to which this population
            belongs.
        :param size: The size this population should have.
        :param spawning_pool: The object that generates individuals.
        :param fitness_method: The method to evaluate individuals.
        :raises InvalidPopulationSizeError: If population size is less than 1.
        :raises InvalidReplacementRateError: If the replacement rate is lower
            than 1 or higher than population size.
        :raises UnexpectedClassError: If any of the input variables doesn't
            follow the contract required (i.e. doesn't inherit from a predefined
            class).
        """
        super().__init__()
        if size < 1:
            raise InvalidPopulationSizeError()
        else:
            self.__size = size
        if not 0 < replacement_rate <= size:
            raise InvalidReplacementRateError()
        else:
            self.__replacement_rate = replacement_rate

        self.__genetic_algorithm = check_is_instance_of(
            genetic_algorithm,
            GeneticAlgorithm,
        )
        self.__spawning_pool = check_is_instance_of(
            spawning_pool,
            SpawningPool,
        )
        self.__fitness_method = check_is_instance_of(
            fitness_method,
            FitnessMethod,
        )

        self.__sorted = False
        self.__other_populations = None

        [self.append(self.spawn()) for _ in range(self.__size)]

    def spawn(self):
        """ Spawns a new individual.

        This individual is not attached to this population.

        :return: An individual of the class of the individuals created by the
            spawning pool defined in the initialization.
        """
        return self.__spawning_pool.create()

    def sort(self, *args, **kwargs):
        """ Sorts the list of individuals by its fitness. """
        if not self.__sorted:
            super().sort(key=self.__fitness_method, reverse=True)
            self.__sorted = True

    def __getitem__(self, index):
        """ Returns the individual located on this position.

        Treat this call as if population were sorted by fitness, from the
        fittest to the less fit.

        :param index: The index of the individual to recover.
        :return: The individual.
        """
        self.sort()
        return super().__getitem__(index)

    def __setitem__(self, index, individual):
        """ Puts the named individual in the specified position.

        This call will cause a new sorting of the individuals the next time an
        access is required. This means that is preferable to make all the
        inserts in the population at once instead doing interleaved readings and
        inserts.

        :param index: The position where to insert the individual.
        :param individual: The individual to be inserted.
        """
        self.__sorted = False
        self.__setitem__(index, individual)
        individual.population = self

    def extend(self, individuals):
        """ Extends the population with a collection of individuals.

        This call will cause a new sorting of the individuals the next time an
        access is required. This means that is preferable to make all the
        inserts in the population at once instead doing interleaved readings and
        inserts.

        :param individuals: A collection of individuals to be inserted into the
            population.
        """
        self.__sorted = False
        for individual in individuals:
            individual.population = self
        super().extend(individuals)

    def append(self, individual):
        """ Ads a new element to the end of the list of the population.

        This call will cause a new sorting of the individuals the next time an
        access is required. This means that is preferable to make all the
        inserts in the population at once instead doing interleaved readings and
        inserts.

        :param individual: The individual to be inserted in the population
        """
        self.__sorted = False
        individual.population = self
        super().append(individual)

    @property
    def sorted(self):
        """ Returns if the individuals are sorted by fitness. """
        return self.__sorted

    @property
    def genetic_algorithm(self):
        """ Returns the genetic algorithm to which this population belongs. """
        return self.__genetic_algorithm

    @property
    def replacement_rate(self):
        """ Returns the replacement rate of this population. """
        return self.__replacement_rate

    @property
    def spawning_pool(self):
        """ Returns the genetic algorithm to which this population belongs. """
        return self.__spawning_pool


class Individual(metaclass=abc.ABCMeta):
    """ One of the possible solutions to a problem.

    In a genetic algorithm, an individual is a tentative solution of a problem,
    i.e. the environment where populations of individuals evolve.
    """

    def __init__(self):
        """ Initializes the individual. """
        self.__population = None

    @property
    def population(self):
        """ Returns the population to which this individual belongs. """
        return self.__population

    @population.setter
    def population(self, population):
        """ Sets the population for this individual. """
        self.__population = population


class SpawningPool(metaclass=abc.ABCMeta):
    """ Defines the methods for creating individuals required by population. """

    @abc.abstractmethod
    def create(self):
        """ Creates a new individual randomly.

        :return: A new Individual object.
        """


class FitnessMethod(metaclass=abc.ABCMeta):
    """ Method to estimate how adapted is the individual to the environment. """

    def __call__(self, individual):
        """ Calculates the fitness of the individual.

        This method does some checks and the delegates the computation of the
        fitness to the "perform" method.

        :param individual:
        :return:
        """
        if individual is None:
            raise ValueError('The individual cannot be None')
        else:
            return self.perform(individual)

    @abc.abstractmethod
    def perform(self, individual):
        """ Estimates how adapted is the individual.

        Must return something comparable (in order to be sorted with the results
        of the methods for other fitnesses). It's supposed that, the highest the
        fitness value is, the fittest the individual is in the environment.

        :param individual: The individual to which estimate the adaptation.
        :return: A sortable object.
        """
