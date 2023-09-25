import copy
import time


class Krpsim:
    def __init__(self, agent, delay, verbose):
        self.inventory = []
        self.delay = delay
        self.agent = agent.copy()
        self.stock = agent.stock
        self.verbose = verbose

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

        while True:
            walk = self.agent.generate_inventory(self.inventory)
            if walk == None or len(walk) == 0:
                self.stock = self.agent.stock
                self.agent.stock = self.agent.initial_stock
                continue
            self.inventory.extend(walk)
            if self.verbose:
                print('agent stock')
                self.agent.print_stocks(self.agent.stock)
            self.stock = self.agent.stock
            self.agent.stock = self.agent.initial_stock
            if self.inventory != None and len(self.inventory) != 0:
                break
        #print('\ninventory:', self.inventory) # for debugging
        return self

    # def print_final_stocks(self, stock: dict):
    #     print("Stock :")
    #     for key, value in stock.items():
    #         print(f" {key} => {value}")

    def optimize(self):
        if self.verbose:
            print('start')
            print('inventory.stock:', self.stock)
        else:
            print("Evaluating ", end='')

        prev_indi = self.agent.copy()
        prev_indi.init_stocks()
        indi = self.copy()

        # for time measurement
        dot_interval = 0.5
        start_time = time.time()
        next_dot_time = start_time + dot_interval

        # for finite checking:
        finite = False
        while indi.stock != prev_indi.stock:
            prev_indi = indi
            new_indi = indi.copy()
            new_indi.agent.stock = indi.stock
            new_indi.agent.initial_stock = indi.stock
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
            elif indi.stock == prev_indi.stock:
                finite = True
                break
        print(" done.")

        print("Main walk")
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

        total_cycle += int(
            self.agent.process[self.inventory[len(self.inventory) - 1][0]].nb_cycle)

        # if finite is True:
        #     microseconds_time = round((current_time - start_time) *
        #                               100000)
        #     print(f"no more process doable at time {microseconds_time}")

        if finite is True:
            print(f"no more process doable at time {total_cycle + 1}")

        print("Stock :")
        for key, value in new_indi.stock.items():
            print(f" {key} => {value}")
        # print_final_stocks(self, new_indi.stock)
