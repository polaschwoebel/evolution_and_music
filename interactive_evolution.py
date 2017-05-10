import random
import os
import pyglet
from send_to_pd import send2port
import time


class Genome():

    # Initialise the genome (possibly as random chromosomes)
    def __init__(self, CHROMOSOME_SIZE=10, randomizeChr=False):
        self.fitness = 0
        self.chromosome = [0] * CHROMOSOME_SIZE
        if randomizeChr:
            self.chromosome = [random.randint(0, 128) for c in self.chromosome]

    # Override the comparison function
    def __eq__(self, other):
        return self.fitness == other.fitness

    # Override the print function
    def __repr__(self):
        return str([self.fitness, self.getPhenotype()])

    # Mutate the chromosome
    def mutate(self):
        # TODO: decide how to mutate the chromosome properly
        self.chromosome[random.randint(0, 9)] = random.randint(0, 1)

class interactive_evolution():

    # Initialise the genetic algorithm with some default values
    # Create the population of genomes with random chromosomes
    def __init__(self, POPULATION_SIZE=5, ELITISM_PERCENTAGE=20, MUTATION_PERCENTAGE=15, MAX_GENERATION=5):
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
        # TODO
        print("Fittest individuals in generation: " + str(self.fittest))

    # Helper function to write genotypes to file
    def write_population_to_file(self):
        with open("genotypes/individuals.txt", "w") as file:
            for i, individual in enumerate(self.population):
                file.write(' '.join([str(char) for char in individual.chromosome]) + '\n')
        return

    # Return the phenotype
    def getPhenotypes(self, read_from_file=False):
        if read_from_file:
            files = os.listdir("examples")
            # ATTENTION on file order! make sure file<->genotype indes
            for file in files:
                if file.endswith('.wav'):
                    music = pyglet.resource.media('examples/' + file)
                    music.play()
                    # foo.duration is the song length
                    pyglet.clock.schedule_once(exiter, music.duration)
                    pyglet.app.run()
            return
        else:
            print('Sending genotypes to PD to be played.')
            for individual in self.population:
                send2port(' '.join([str(char) for char in individual.chromosome]))
                time.sleep(5)
            return


    def evaluate_fitness(self):
        self.getPhenotypes()
        best_1 = int(input('Which piece sounded best?'))
        best_2 = int(input('Which second piece did you like?'))
        self.fittest = [best_1, best_2]


    # evaluates fitness and checks whether max generations are reached
    def continueEvolution(self):
        self.fittest = [0,0]
        self.evaluate_fitness()
        self.curr_generation += 1
        if self.curr_generation == self.MAX_GENERATION:
            return False
        return True

    # Container function for the reproduction methods
    def reproducePopulation(self):
        offspring = self.selectAndReproduce()
        self.replacePopulation(offspring)
        self.mutatePopulation()

    # Choose which of the population to reproduce and return the offspring
    def selectAndReproduce(self):
        offspring = self.reproduce(self.population[self.fittest[0]], self.population[self.fittest[1]])
        return offspring

    # Reproduce the parents and return offspring
    def reproduce(self, parent1, parent2):
        # TODO: Decide how to reproduce
        offspring1 = Genome()
        offspring1.chromosome = parent1.chromosome[:5] + parent2.chromosome[5:]
        offspring2 = Genome()
        offspring2.chromosome = parent2.chromosome[:5] + parent1.chromosome[5:]
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
