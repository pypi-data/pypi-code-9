from pynetics.population import Population
from pynetics.utils import test_chances


class GeneticAlgorithm:
    # TODO TBD
    def __init__(
            self,
            individual,
            population_size,
            f_selection,
            f_replacement,
            f_stop_criteria,
            f_crossover=None,
            f_mutation=None,
            f_catastrophe=None,
            p_crossover=.9,
            p_mutation=.1,
            maximize_fitness=False,
            p_catastrophe=.0,
    ):
        # TODO TBD
        self.__population = Population(individual, population_size, maximize_fitness=maximize_fitness)
        self.__f_selection = f_selection
        self.__f_crossover = f_crossover
        self.__f_mutation = f_mutation
        self.__f_replacement = f_replacement
        self.__f_stop_criteria = f_stop_criteria
        self.__f_catastrophy = f_catastrophe
        self.__p_crossover = p_crossover
        self.__p_mutate = p_mutation
        self.__p_catastrophe = p_catastrophe

        self.__iteration = 0
        self.__p_catastrophe_accum = .0

    def evolve(self):
        # TODO TBD
        self.__iteration = 0
        self.__p_catastrophe_accum = .0
        while not self.__f_stop_criteria(self):
            self.step()
            print('{} ({:.2f} -->\t{}'.format(self.iteration, self.population[0].fitness(), self.population[0]))
            self.__iteration += 1

    def step(self):
        # TODO TBD
        previous_fitness = self.population[0].fitness()

        # Selection
        p1, p2 = self.__f_selection(self.population, n=2)
        # Crossover
        if self.__f_crossover and test_chances(self.__p_crossover):
            c1, c2 = self.__f_crossover(p1, p2)
        else:
            c1, c2 = p1.clone(), p2.clone()
        # Mutation
        if self.__f_mutation:
            if test_chances(self.__p_mutate):
                c1 = self.__f_mutation(c1)
            if test_chances(self.__p_mutate):
                c2 = self.__f_mutation(c2)
        # Replacement
        self.__f_replacement(self.population, [c1, c2])
        # Catastrophy
        if self.__f_catastrophy and test_chances(self.__p_catastrophe_accum):
            self.__f_catastrophy(self.population)
            self.__p_catastrophe_accum = .0

        # TODO Quizá mejor mirar esto con la biodiversidad y no con el fitness
        self.__p_catastrophe_accum = self.__p_catastrophe_accum + self.__p_catastrophe if self.population[
                                                                                              0].fitness() == previous_fitness else .0

    @property
    def population(self):
        return self.__population

    @property
    def iteration(self):
        return self.__iteration
