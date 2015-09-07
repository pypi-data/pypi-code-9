import abc


class Individual(metaclass=abc.ABCMeta):
    # TODO TBD
    def __init__(self):
        # TODO TBD
        self.__population = None

    @abc.abstractmethod
    def create(self):
        """ Creates a new individual of this kind.

        :return: A new Individual object of the subclass.
        """

    @abc.abstractmethod
    def clone(self):
        """ Clones this individual creating a new one looking exactly the same.

        :return: A new Individual object of the subclass.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def fitness(self):
        """ Returns a value indicating how suitable is this individual for the environment.

        :return: A float value indicating the value of fitness.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def phenotype(self):
        # TODO TBD
        raise NotImplementedError()

    def __lt__(self, individual):
        # TODO TBD
        return self.fitness() < individual.fitness()

    @property
    def population(self):
        # TODO TBD
        return self.__population

    @population.setter
    def population(self, population):
        # TODO TBD
        self.__population = population


class ListIndividual(Individual, metaclass=abc.ABCMeta):
    # TODO TBD
    def __init__(self, **kwargs):
        # TODO TBD
        super().__init__()
        self.__size = kwargs['size']
        self.__alleles = kwargs['alleles']
        self.__kwargs = kwargs
        self.__chromosome = [None for _ in range(self.__size)]

    def create(self):
        # TODO TBD
        individual = self.__class__(**self.__kwargs)
        individual.chromosome = [self.__alleles.get() for _ in range(self.__size)]
        return individual

    def clone(self):
        # TODO TBD
        individual = self.__class__(**self.__kwargs)
        individual.chromosome = self.chromosome[:]
        return individual

    def __len__(self):
        return len(self.chromosome)

    def __eq__(self, individual):
        return all(c1 == c2 for (c1, c2) in zip(self.chromosome, individual.chromosome))

    @property
    def chromosome(self):
        # TODO TBD
        return self.__chromosome[:]

    @chromosome.setter
    def chromosome(self, chromosome):
        # TODO TBD
        for i in range(len(chromosome)):
            self.__chromosome[i] = chromosome[i]

    @property
    def alleles(self):
        # TODO TBD
        return self.__alleles
