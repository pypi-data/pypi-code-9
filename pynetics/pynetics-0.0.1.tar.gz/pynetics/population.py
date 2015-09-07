import collections.abc


# TODO See collections.abc because maybe there is another more appropiated than Sequence.

class Population(collections.abc.Sequence):
    """ Collection of individuals. """

    def __init__(self, individual, size, maximize_fitness=False):
        """ Initializes the population with as much individuals of type "individual" as "size" parameter points out.

        Because operators requires to know which individual is the fittest, others which is the less fit and others need
        to travel along the collection of individuals in some way or another (e.g. from fittest to less fit), the
        population is always sorted when an access is required. Thus, writing population[0] always returns the fittest
        individual, population[1] the next and so on, until population[-1] which is the less fit.

        :param individual: An example of individual. This individual is not included in the population, but is used as
            a creator of random individuals.
        :param size: The size this population must have.
        :param maximize_fitness: If is True, the fittest individual will be considered the one with a higher fitness()
            value. If is False, the fittest individual will be the one with the lower value in fitness(). It defaults to
            False.
        """
        self.__maximize = maximize_fitness

        self.__individuals = [individual.create() for _ in range(size)]
        for individual in self.__individuals:
            individual.population = self
        self.__sorted = False

    def __sort(self):
        """ Sorts the list of individuals by its fitness. """
        if not self.__sorted:
            self.__individuals.sort(reverse=self.__maximize)
            self.__sorted = True

    def __getitem__(self, index):
        """ Returns the individual located on this position.

        Treat this call as if population were sorted by fitness, from the fittest to the less fit.

        :param index: The index of the individual to recover.
        :return: The individual.
        """
        self.__sort()
        return self.__individuals[index]

    def __setitem__(self, index, individual):
        """ Puts the named individual in the specified position.

        This call will cause a new sorting of the individuals the next time an access is required. This means that is
        preferable to make all the inserts in the population at once instead doing interleaved readings and inserts.

        :param index: The position where to insert the individual.
        :param individual: The individual to be inserted.
        """
        self.__sorted = False
        self.__individuals[index] = individual
        self.__individuals[index].population = self

    def __len__(self):
        """ The size of the population, i.e. the number of individuals the population has.

        :return: An integer with the number of individuals the population has.
        """
        return len(self.__individuals)

    def extend(self, individuals):
        """ Extends the population with a collection of individuals.

        This call will cause a new sorting of the individuals the next time an access is required. This means that is
        preferable to make all the inserts in the population at once instead doing interleaved readings and inserts.

        :param individuals: A collection of individuals to be inserted into the population.
        """
        for individual in individuals:
            individual.population = self
        self.__individuals.extend(individuals)
        self.__sorted = False

    def remove(self, value):
        """ Removes the given individual from the population. """
        self.__individuals.remove(value)

    @property
    def individuals(self):
        return self.__individuals
