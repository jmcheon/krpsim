from Individual import Individual

class Population:

    def __init__(self, population_size, base):
        self.population = []
        self.pool = []
        self.population_size = population_size
        self.stock = base.stock.copy()
        self.process = base.process.copy()
        self.optimize = base.optimize.copy()

    # Generate the initial population of individuals (schedules)
    def generate_population(self):
    
        for _ in range(self.population_size):
            individual = Individual(self.stock, self.process, self.optimize) 
            self.population.append(individual.generate_individual())
    
        return self.population

    def calcuate_fitness(self):
        for i in range(self.population_size):
            self.population[i].calculate_fitness()


    def selection(self):
        max_fitness = 0
        for i in range(self.population_size):
            if self.population[i].fitness > max_fitness:
                max_fitness = self.population[i].fitness

        # Creating a mating pool based on the selection method
