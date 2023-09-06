import random

class Individual:

    def __init__(self, stock, process, optimize):
        self.individual = []
        self.fitness = 0
        self.stock = stock
        self.process = process
        self.optimize = optimize

    # Generate an individual (schedule) randomly
    def generate_individual(self):
        process_names = list(self.process.keys())
    
        num_processes = random.randint(1, len(process_names))
    
        # Randomly select a subset of process names
        selected_process_names = random.sample(process_names, num_processes)
    
        for process_name in selected_process_names:
            need = self.process[process_name].need
            random_num = random.randint(1, 10)
            need = {k: v * random_num for k, v in need.items()}
            #need.values() * random_num
            #print(need, need.values())
            self.individual.append((process_name, need))
    
        return self.individual
    
    def calcuate_fitness(self):
        pass
