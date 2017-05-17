import random
import os
import pyglet
from send_to_pd import send2port, send2port_socket
from keypoller import KeyPoller
import time
from evaluation_wheel import transcribe_input
from fitness_function import fit_pca, pca_fitness


class Genome():

    # Initialise the genome (possibly as random chromosomes)
    def __init__(self, CHROMOSOME_SIZE=30, randomizeChr=False):
        self.fitness = 0
        self.chromosome = [0] * CHROMOSOME_SIZE
        if randomizeChr:
            self.chromosome = [random.randint(0, 128) for c in self.chromosome]

    # Override the comparison function
    def __eq__(self, other):
        return self.fitness == other.fitness

    # Override the print function
    def __repr__(self):
        #return str([self.fitness, self.getPhenotype()])
        # individual doesn't have getPhenotype()
        return str(self.fitness)


    # Mutate the chromosome
    def mutate(self):
        # TODO: decide how to mutate the chromosome properly
        self.chromosome[random.randint(0, 9)] = random.randint(0, 1)

class interactive_evolution():

    # Initialise the genetic algorithm with some default values
    # Create the population of genomes with random chromosomes
    def __init__(self, POPULATION_SIZE=5, ELITISM_PERCENTAGE=20, MUTATION_PERCENTAGE=50, MAX_GENERATION=100):
        self.population = [Genome(randomizeChr=True) for _ in range(POPULATION_SIZE)]
        self.ELITISM_PERCENTAGE = ELITISM_PERCENTAGE
        self.MUTATION_PERCENTAGE = MUTATION_PERCENTAGE
        self.fittest = [0, 0]
        self.MAX_GENERATION = MAX_GENERATION
        self.curr_generation = 0
        self.executeEvolution()

    # Run the evolution cycle
    def executeEvolution(self):
        print("Starting evolution...")
        while(self.continueEvolution()):
            self.generateStatistics()
            self.reproducePopulation()
        self.generateStatistics()
        print("Finished evolution")

    # Print info about the generation
    def generateStatistics(self):
        self.write_population_to_file()
        # this doesn't work because we reorder the population list so can't get the index
        #print("Fittest individuals in generation: " +
        #      str([self.population.index(ind) for ind in self.fittest]) + '. Their fitnesses are' + str(self.fittest))
        print('The highest fitnesses in this generation are ' + str(self.fittest))

    # Helper function to write genotypes to file
    def write_population_to_file(self):
        with open("genotypes/individuals.txt", "w") as file:
            for i, individual in enumerate(self.population):
                file.write(' '.join([str(char) for char in individual.chromosome]) + '\n')
        return

    # Return the phenotype
    def getPhenotypes(self):
        human_evaluation = (self.curr_generation % 10 == 0)
        if human_evaluation:
            print('Sending genotypes to PD to be played.')
            for i, individual in enumerate(self.population):
                print('Evaluating individual number %s.' %(i+1))
                #print(' '.join([str(char) for char in individual.chromosome]))
                #send2port(' '.join([str(char) for char in individual.chromosome]))
                send2port_socket(' '.join([str(char) for char in individual.chromosome]))
                fitness = self.keyLogger()
                print(fitness)
                individual.fitness = transcribe_input(fitness)
            return
        else:
            pca, indices = fit_pca(self.population)
            print(pca, indices)
            for individual in self.population:
                individual.fitness = pca_fitness(individual, pca, indices)
                print(individual.fitness)

            return


    def keyLogger(self):
        t = time.time()
        s = ''
        with KeyPoller() as keyPoller:
            # For 5 seconds look for keyboard input
            while time.time() < t + 5.0:
                c = keyPoller.poll()
                if c is not None:
                    s += c
        return s

    def evaluate_fitness(self):
        self.getPhenotypes()
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        #best_1 = int(input('Which piece sounded best?'))
        #best_2 = int(input('Which second piece did you like?'))
        self.fittest = self.population[:2]


    # evaluates fitness and checks whether max generations are reached
    def continueEvolution(self):
        self.fittest = [0,0]
        self.evaluate_fitness()
        self.curr_generation += 1
        if self.curr_generation == self.MAX_GENERATION:
            return False
        return True

    # Container function for the reproduction methods-
    def reproducePopulation(self):
        offspring = self.selectAndReproduce()
        self.replacePopulation(offspring)
        self.mutatePopulation()

    # Choose which of the population to reproduce and return the offspring
    def selectAndReproduce(self):
        offspring = self.reproduce(self.fittest[0], self.fittest[1])
        return offspring

    # Reproduce the parents and return offspring
    def reproduce(self, parent1, parent2):
        # TODO: Decide how to reproduce
        offspring1 = Genome()
        offspring1.chromosome = parent1.chromosome[:7] + parent2.chromosome[7:]
        offspring2 = Genome()
        offspring2.chromosome = parent2.chromosome[:7] + parent1.chromosome[7:]
        return [offspring1, offspring2]

    # Replaces some of the existing population with the offspring
    def replacePopulation(self, offspring):
        # TODO: Decide how to choose the members of the population to be replaced
        # - probably "randomly"/as is in non-interactive setting
        numOffspring = len(offspring)
        self.population = self.population[:-numOffspring] + offspring

    # Go through the whole population and mutate some of them
    def mutatePopulation(self):
        for individual in self.population:
            self.shouldMutate(individual)

    # Mutate an individual in the population
    # Chance of mutation occurring based on mutation percentage
    def shouldMutate(self, individual):
        if random.randint(0, 99) < self.MUTATION_PERCENTAGE:
            individual.mutate()
            return True
        return False


# helper for pyglet (i.o. to play snippets)
def exiter(dt):
    pyglet.app.exit()


def main():
    ia = interactive_evolution()


if __name__ == main():
    main()
