import copy

class Krpsim:
    def __init__(self, agent, delay):
        self.inventory = []
        self.delay = delay
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

    def generate_inventory(self):
        if len(self.agent.get_available_process_lst()) == 0:
        #if self.agent.is_already_optimized():
            #self.agent.print_stocks()
            #print('done ...')
            return self

        while True:
            walk = self.agent.generate_inventory()
            if walk == None or len(walk) == 0:
                self.stock = self.agent.stock
                self.agent.stock = self.agent.initial_stock
                continue
            self.inventory.extend(walk)
            print('agent stock')
            self.agent.print_stocks()
            self.stock = self.agent.stock
            self.agent.stock = self.agent.initial_stock
            if self.inventory != None and len(self.inventory) != 0:
                break
        #print('inventory:', self.inventory) # for debugging
        return self

    def optimize(self):

        print('start')
        print('inventory.stock:', self.stock)
        prev_indi = self.agent.copy()
        prev_indi.init_stocks() 
        indi = self.copy()
        while indi.stock != prev_indi.stock:
            prev_indi = indi
            new_indi = indi.copy()
            new_indi.agent.stock = indi.stock
            new_indi.agent.initial_stock = indi.stock
            new_indi.generate_inventory()
            print('new stock:', new_indi.stock)
            indi = new_indi.copy()
        print('end')
