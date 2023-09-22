import random, copy

class Individual:

    def __init__(self, agent):
        self.individual = []
        self.fitness = 0
        self.agent = agent.copy()
        self.stock = agent.stock

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, stock):
        if isinstance(stock, dict):
            self._stock = dict(stock)
        else:
            raise ValueError('Stock must be a dictionary')

    def copy(self):
        return copy.copy(self)

    def generate_indi(self):
        pop = []
        if len(self.agent.get_available_processes()) == 0:
        #if self.agent.is_already_optimized():
            #self.agent.print_stocks()
            print('done ...')
            return self

        while len(pop) < 1:
            walk = self.agent.generate_walk()
            if walk == None or len(walk) == 0:
                self.stock = self.agent.stock
                self.agent.stock = self.agent.initial_stock
                #print(len(pop))
                continue
            self.individual.extend(walk)
            print('agent stock')
            self.agent.print_stocks()
            self.stock = self.agent.stock
            self.agent.stock = self.agent.initial_stock
            if self.individual != None and len(self.individual) != 0:
                pop.append(self.individual)
        #print('walk:', pop) # for debugging
        return self

    # Generate an individual (schedule) randomly
    def generate_individual(self) -> 'Individual':
        process_names = list(self.process.keys())

        num_processes = random.randint(1, len(process_names))

        # Randomly select a subset of process names
        selected_process_names = random.sample(process_names, num_processes)

        for process_name in selected_process_names:
            need = self.process[process_name].need
            # random_num = random.randint(1, 10)
            # need = {k: v * random_num for k, v in need.items()}
            # need.values() * random_num
            # print(need, need.values())
            self.individual.append((process_name, need))

        return self

    def calculate_fitness_time(self):
        time_denom = 0
        for process in self.individual:
            time_denom += int(self.agent.process[process].nb_cycle)
        return 1 / time_denom

    def calculate_fitness(self):
        time_applied = False
        for optimize_item in self.agent.optimize:
            if optimize_item == "time" and time_applied == False:
                time_applied = True
                self.fitness += self.calculate_fitness_time()
            else:
                self.fitness += self.stock[optimize_item]
        #print(self.stock)
