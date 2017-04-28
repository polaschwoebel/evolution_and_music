import random

class Genome():
    
    # Initialise the genome (possibly as random chromosomes)
    def __init__(self, CHROMOSOME_SIZE = 10, randomizeChr = False):
        self.fitness = 0
        self.chromosome = [0] * CHROMOSOME_SIZE
        if randomizeChr:
            # TODO: decide on possible chromosome values
            self.chromosome = [random.randint(0, 1) for c in self.chromosome]  
    
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
    
    # Return the phenotype
    def getPhenotype(self):
        # TODO: decide what the phenotype should be
        return "".join(['a' if c == 0 else 'A' for c in self.chromosome])
    

class GeneticAlgorithm():
        
    # Initialise the genetic algorithm with some default values
    # Create the population of genomes with random chromosomes
    def __init__(self, POPULATION_SIZE = 100, ELITISM_PERCENTAGE = 20, MUTATION_PERCENTAGE = 15):       
        self.population = [Genome(randomizeChr=True) for _ in range(POPULATION_SIZE)]
        self.ELITISM_PERCENTAGE = ELITISM_PERCENTAGE
        self.MUTATION_PERCENTAGE = MUTATION_PERCENTAGE
        self.fittest = [0, 0]
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
        # TODO
        print("Fittest value in generation: " + str(self.fittest))
            
    # Determines whether we have reached peak fitness
    def continueEvolution(self):
        # TODO: Decide how to know when to stop evolution
        self.fittest = [0,0]
        for individual in self.population:
            individual.fitness = individual.getPhenotype().count('a')
            if individual.fitness > self.fittest[0]:
                self.fittest = [individual.fitness, individual.getPhenotype()]
                
            if individual.fitness == 10:
                return False
        return True
    
    # Container function for the reproduction methods
    def reproducePopulation(self):
        offspring = self.selectAndReproduce()
        self.replacePopulation(offspring)
        self.mutatePopulation()
        
    # Choose which of the population to reproduce and return the offspring
    def selectAndReproduce(self):
        # TODO: Decide how to choose the parents
        offspring = list() 
        for i in range(0, len(self.population), 2):
            offspring.extend(self.reproduce(self.population[i], self.population[i+1]))     
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
            
        
    
g = GeneticAlgorithm()