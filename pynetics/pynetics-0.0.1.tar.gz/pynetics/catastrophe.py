import abc


class Catastrophe(metaclass=abc.ABCMeta):
    # TODO TBD
    def __call__(self, population):
        # TODO TBD
        # First we decide which individuals among the population are maintained.
        new_individuals = self.population_to_maintain(population)
        # Second, we generate new individuals until length of population is reached.
        while len(new_individuals) < len(population):
            new_individuals.append(new_individuals[0].create())
        # Finally, generated individuals are the new population
        for i in range(len(population)):
            population[i] = new_individuals[i]

    def population_to_maintain(self, population):
        # TODO TBD
        return []


class PackingCatastrophe(Catastrophe):
    # TODO TBD

    def population_to_maintain(self, population):
        # TODO TBD
        # We get each different individual once.
        population_to_maintain = []
        for individual in population:
            if individual not in population_to_maintain:
                population_to_maintain.append(individual)
        return population_to_maintain


class DoomsdayCatastrophe(Catastrophe):
    # TODO TBD

    def population_to_maintain(self, population):
        # TODO TBD
        # We get the best individual among all the population.
        return [population[0]]
