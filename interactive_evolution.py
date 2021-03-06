import random
import os
from send_to_pd import send2port, send2port_socket
from keypoller import KeyPoller
import time
from evaluation_wheel import transcribe_input
from fitness_function import fit_pca, pca_fitness
import pickle


class Genome():

    # Initialise the genome (possibly as random chromosomes)
    def __init__(self, CHROMOSOME_SIZE=73, randomizeChr=False):
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
        self.chromosome[random.randint(0, 7)] = random.randint(0, 128)
        self.chromosome[random.randint(7, 22)] = random.randint(0, 128)
        if random.randint(0, 99) < 20:
            self.chromosome[random.randint(22, 23)] = random.randint(0, 128)
        self.chromosome[random.randint(23, len(self.chromosome) - 1)] = random.randint(0, 128)

class interactive_evolution():

    # Initialise the genetic algorithm with some default values
    # Create the population of genomes with random chromosomes
    def __init__(self, POPULATION_SIZE=5, ELITISM_PERCENTAGE=20, MUTATION_PERCENTAGE=50, MAX_GENERATION=10):
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
            print(self.curr_generation)
            self.generateStatistics(self.curr_generation)
            self.reproducePopulation()
        self.generateStatistics(self.curr_generation)
        print("Finished evolution")

    # Print info about the generation
    def generateStatistics(self, generation):
        self.write_population_to_file(generation)
        # this doesn't work because we reorder the population list so can't get the index
        #print("Fittest individuals in generation: " +
        #      str([self.population.index(ind) for ind in self.fittest]) + '. Their fitnesses are' + str(self.fittest))
        print('The highest fitnesses in this generation are ' + str(self.fittest))

    # Helper function to write genotypes to file
    def write_population_to_file(self, generation):
        all_inds = []
        for i, individual in enumerate(self.population):
            all_inds.append(individual.chromosome)
        with open("genotypes_purely_interactive/individuals_%s.p"%generation, "wb") as file:
            pickle.dump(all_inds, file)

    # Return the phenotype
    def getPhenotypes(self):
        #human_evaluation = (self.curr_generation % 10 == 0)
        human_evaluation = True
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
    def reproduce(self, *parents):
        offspring = []
        for i in range(2):
            child = Genome()
            child.chromosome = random.choice(parents).chromosome[:7] + random.choice(parents).chromosome[7:22] + random.choice(parents).chromosome[22:23] + random.choice(parents).chromosome[23:]
            offspring.append(child)

        genotypes = ["".join([str(c) for c in individual.chromosome]) for individual in self.population]
        for child in offspring:
            while "".join([str(c) for c in child.chromosome]) in genotypes:
                child.mutate()

        return offspring

    # Replaces some of the existing population with the offspring
    def replacePopulation(self, offspring):
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


def main():
    ia = interactive_evolution()


if __name__ == main():
    main()
