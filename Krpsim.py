import copy
import time


class Krpsim:
    def __init__(self, agent, delay, verbose, random=False):
        self.inventory = []
        self.delay = delay
        self.agent = agent.copy()
        self.stock = (agent.stock)
        self.verbose = verbose
        self.random = random

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

    def generate_inventory(self):
        if len(self.agent.get_available_process_lst()) == 0:
            # if self.agent.is_already_optimized():
            # self.agent.print_stocks(self.agent.stock)
            # print('done ...')
            return self
        i = 0

        while True and i < 1000:
            if self.random == False:
                walk = self.agent.generate_inventory(self.inventory, self.delay)
            else:
                walk = self.agent.generate_walk(self.inventory, self.delay)
            if walk == None or len(walk) == 0:
                self.stock = self.agent.stock
                #self.agent.print_stocks(self.stock)
                self.agent.stock = self.agent.initial_stock
                #self.inventory.clear()
                i += 1
                #break
                continue
            self.inventory.extend(walk)
            if self.verbose:
                print('agent stock')
                self.agent.print_stocks(self.agent.stock)
            self.stock = self.agent.stock
            self.agent.stock = self.agent.initial_stock
            if self.inventory != None and len(self.inventory) != 0:
                #print('break')
                break
        #self.agent.print_stocks(self.stock)
        if i >= 1000:
            #print('f', self.agent.walk)
            self.inventory.clear()
            self.inventory = list(self.agent.walk)
        #print('\ninventory:', self.inventory) # for debugging
        return self

    # def print_final_stocks(self, stock: dict):
    #     print("Stock :")
    #     for key, value in stock.items():
    #         print(f" {key} => {value}")
    def run(self):
        if self.verbose:
            print('start')
            print('inventory.stock:', self.stock)
        else:
            print("Evaluating ", end='')
        stock = self.optimize(True)
        print(" done.")
        if self.agent.finite and 'time' in self.agent.optimize:
            stock = self.optimize_time(stock)
        self.print_trace(stock)

    def optimize(self, time_optimized):
        prev_indi = self.agent.copy()
        prev_indi.init_stocks()
        indi = self.copy()

        # for time measurement
        dot_interval = 0.5
        start_time = time.time()
        next_dot_time = start_time + dot_interval

        # for finite checking:
        self.agent.finite = False
        while indi.stock != prev_indi.stock:
            prev_indi = indi
            new_indi = indi.copy()
            new_indi.agent.stock = dict(indi.stock)
            new_indi.agent.initial_stock = dict(indi.stock)
            new_indi.generate_inventory()
            if self.verbose:
                print('new stock:', new_indi.stock)
            indi = new_indi.copy()

            current_time = time.time()
            if current_time >= next_dot_time:
                print('.', end='', flush=True)
                next_dot_time = current_time + dot_interval

            if current_time - start_time >= self.delay:
                break
            elif indi.stock == prev_indi.stock or len(indi.agent.get_available_process_lst()) == 0:
                print(len(indi.agent.get_available_process_lst()))
                self.agent.finite = True
                #print(self.agent.finite)
                break
        self.inventory = list(new_indi.inventory)
        #if time_optimized:
            #self.stock = dict(new_indi.stock)
        return dict(new_indi.stock)

    def optimize_time(self, stock):
        #print('time in optimize')
        min_total_cycle = float('inf')
        inventory = []
        time_stock = []
        for i in range(80):
            time_optimized = False
            if len(self.inventory) != 0:
                total_cycle = self.inventory[-1][1]
                #print(f'{(self.inventory)} {total_cycle}')
                total_cycle += int(
                self.agent.process[self.inventory[len(self.inventory) - 1][0]].nb_cycle)
            else:
                total_cycle = float('inf')
            print(f'{(self.inventory)} {total_cycle}')
            #print(f'time: {total_cycle}')
            if min_total_cycle > total_cycle:
                min_total_cycle = total_cycle
                inventory = list(self.inventory)
                time_optimized = True
                time_stock = dict(stock)
                print('\t\t', min_total_cycle, total_cycle, time_stock)
                #print('inv:', inventory)
            elif min_total_cycle == total_cycle:
                for optimize in self.agent.optimize:
                    if optimize != 'time':
                        print(optimize, time_stock, stock, total_cycle)
                    if optimize != 'time' and time_stock[optimize] < stock[optimize]:
                        inventory = list(self.inventory)
                        time_stock = dict(stock)
            self.agent.cycle = 0
            self.inventory.clear()
            stock = self.optimize(time_optimized)
        self.inventory.clear()
        self.inventory = list(inventory)
        return time_stock
        #print(f'optimized time: {min_total_cycle}')


    def print_trace(self, stock):
        print("Main walk")
        #print(self.inventory)
        #print(self.agent.print_stocks(self.agent.stock))
        if len(self.inventory) != 0:
            total_cycle = self.inventory[-1][1]
        else:
            total_cycle = 0
        biggest_cycle = 0
        item_before = None
        stock_copy = self.stock
        #print(self.inventory[0])
        for item in self.inventory:
            # print(stock_copy)
            # print(self.agent.process[item].nb_cycle)
            # stock_copy = {
            #     key: stock_copy[key] - self.agent.process[item].need.get(key, 0) for key in stock_copy}
            # if item_before != None and self.agent.process[item].need.keys() != self.agent.process[item_before].need.keys():
            #     total_cycle += biggest_cycle
            # item_before = item

            # print("b4", stock_copy)
            # print(self.agent.process[item].nb_cycle)
            stock_copy2 = {
                key: stock_copy[key] - self.agent.process[item[0]].need.get(key, 0) for key in stock_copy}
            # print("after", stock_copy2)
            if item_before != None and self.agent.process[item[0]].need.keys() != self.agent.process[item_before].need.keys():
                pass
                #total_cycle += biggest_cycle
            elif any(value < 0 for value in stock_copy2.values()):
                pass
                #total_cycle += biggest_cycle

            stock_copy = {
                key: stock_copy[key] - self.agent.process[item[0]].need.get(key, 0) for key in stock_copy}
            stock_copy = {
                key: stock_copy[key] + self.agent.process[item[0]].result.get(key, 0) for key in stock_copy}
            # print("final", stock_copy)
            if (int(self.agent.process[item[0]].nb_cycle) > biggest_cycle):
                biggest_cycle = int(self.agent.process[item[0]].nb_cycle)
            print(f"{item[1]}:{item[0]}")
            item_before = item[0]

        if len(self.inventory) != 0:
            total_cycle += int(
            self.agent.process[self.inventory[len(self.inventory) - 1][0]].nb_cycle)

        # if finite is True:
        #     microseconds_time = round((current_time - start_time) *
        #                               100000)
        #     print(f"no more process doable at time {microseconds_time}")

        if self.agent.finite is True:
            print(f"no more process doable at time {total_cycle + 1}")

        print("Stock :")
        for key, value in stock.items():
            print(f" {key} => {value}")
        # print_final_stocks(self, new_indi.stock)
