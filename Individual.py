import random
from Base import Base

class Individual(Base):

    def __init__(self):
        self.individual = []
        self.fitness = 0

    # Generate an individual (schedule) randomly
    def generate_individual(self):
        process_names = list(self.process.keys())
    
        num_processes = random.randint(1, len(process_names))
    
        # Randomly select a subset of process names
        selected_process_names = random.sample(process_names, num_processes)
    
        initial_stock_lst = []
        for _, value in self.stock.items():
            if value > 0:
                initial_stock_lst.append(value)
    
        for process_name in selected_process_names:
            self.individual.append((process_name, random.randint(0, initial_stock_lst[0])))
    
        return self.individual
    
    def calcuate_fitness(self):
        pass
