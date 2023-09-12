import random, copy


class Individual:

    def __init__(self, base):
        self.individual = []
        self.fitness = 0
        self.base = base.copy()
        self.stock = {}

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

        while len(pop) < 1:
            self.individual.extend(self.base.generate_walk())
            print('base stock')
            self.base.print_stocks()
            self.stock = self.base.stock
            self.base.stock = self.base.initial_stock
            if self.individual != None and len(self.individual) != 0:
                pop.append(self.individual)
        # print(pop) # for debugging
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
            time_denom += int(self.base.process[process].nb_cycle)
        return 1 / time_denom

    def calculate_fitness(self):
        time_applied = False
        for optimize_item in self.base.optimize:
            if optimize_item == "time" and time_applied == False:
                time_applied = True
                self.fitness += self.calculate_fitness_time()
            else:
                self.fitness += self.stock[optimize_item]
        #print(self.stock)
