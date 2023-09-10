from Process import Process
import copy, random
import networkx as nx
import matplotlib.pyplot as plt

class Base:

    def __init__(self):
        #print("Base init()")
        self._initial_stock = {}
        self._stock = {}
        self._process = {}
        self._optimize = []
        self._graph = nx.DiGraph()

    def set_attributes(self, initial_stock, stock, process, optimize, graph):
        self.initial_stock = dict(initial_stock)
        self.stock = dict(stock)
        self.process = dict(process)
        self.optimize = list(optimize)
        self.graph = (graph)

    @property
    def initial_stock(self):
        return self._initial_stock

    @property
    def stock(self):
        return self._stock

    @property
    def process(self):
        return self._process

    @property
    def optimize(self):
        return self._optimize

    @property
    def graph(self):
        return self._graph

    @initial_stock.setter
    def initial_stock(self, stock):
        #print("setting initial stock")
        if isinstance(stock, dict):
            self._initial_stock = dict(stock)
        else:
            raise ValueError('Stock must be a dictionary')

    @stock.setter
    def stock(self, stock):
        if isinstance(stock, dict):
            self._stock = dict(stock)
        else:
            raise ValueError('Stock must be a dictionary')

    @process.setter
    def process(self, process):
        if isinstance(process, dict):
            self._process = dict(process)
        else:
            raise ValueError('Process must be a dictionary')

    @optimize.setter
    def optimize(self, optimize):
        if isinstance(optimize, list):
            self._optimize = list(optimize)
        else:
            raise ValueError('Optimize must be a list')

    @graph.setter
    def graph(self, graph):
        if isinstance(graph, nx.DiGraph):
            self._graph = graph 
        else:
            raise ValueError('Gragph must be an instance of networkx.DiGraph')

    def copy(self):
        return copy.copy(self)

    def print_initial_stocks(self):
        print('---initial stocks---')
        for stock, quantity in self.initial_stock.items():
            print(f'{stock}:{quantity}')
        print('--------------------')

    def print_stocks(self):
        print('--------------')
        for stock, quantity in self.stock.items():
            print(f'{stock}:{quantity}')
        print('--------------')

    def get_available_stocks(self) -> list:
        stock_lst = []
        for stock, quantity in self.stock.items():
            if quantity > 0:
                stock_lst.append(stock)
        return stock_lst

    def get_available_processes(self) -> list:
        process_lst = []
        for process in self.process.values():
            #stock_lst = self.get_available_stocks()
            if self.is_need_satisfied(process):
                process_lst.append(process.name)
        return process_lst

    def is_stock_satisfied(self, stock: str, quantity: int) -> bool:
        if self.stock[stock] >= quantity:
            return True
        return False

    def is_need_satisfied(self, process: Process) -> bool:
        for stock, quantity in process.need.items():
            #print(f'{process.name} stock: {stock}, qty: {quantity}')
            ret = self.is_stock_satisfied(stock, quantity)
            if ret == False:
                return False
        return True

    def is_optimized(self) -> bool:
        #self.print_stocks()
        for stock in self.optimize:
            if stock != 'time' and self.stock[stock] > self.initial_stock[stock]:
                return True
        return False

    def run_process(self, process: Process) -> bool:
        need_dict = process.need
        #print(need_dict)
        for stock, quantity in need_dict.items():
            #if self.is_stock_available(stock, -quantity):
            if self.is_stock_satisfied(stock, quantity):
                self.stock[stock] -= quantity
            else:
                return False


        result_dict = process.result
        #print(result_dict)
        for stock, quantity in result_dict.items():
            self.stock[stock] += quantity
        #self.print_stocks()
        return True

    def generate_walk(self) -> list:
        walk = []
        while self.is_optimized() == False:
            process_lst = self.get_available_processes()
            if len(process_lst) == 0:
                #return None
                return walk
            v = random.choice(process_lst)
            if self.run_process(self.process[v]):
                #print(v)
                walk.append(v)
        #print('walk:', walk)
        return walk

    def find_connecting_process(self, process):
        process_lst = []
        for pro in self.process.values():
            #print(pro.need.keys())
            if process.result.keys() == pro.need.keys() and pro != process:
            #if process.result.items() == pro.need.items() and pro != process:
                process_lst.append(pro)
                #print('return:', pro.name)
        return process_lst

    def create_graph(self):
        self.graph.add_node('start')
        for process in self.process.values():
            self.graph.add_edge('start', process.name)
            self.graph.add_edge(process.name, 'start')

        for process in self.process.values():
            process_name, needs, results = process.name, process.need, process.result
            self.graph.add_node(process_name)
            #print(process.result.keys())
            #self.is_need_satisfied(process)
            #for key in process.result.keys():
            #print('key:', key, process.need.keys())
            process_lst = self.find_connecting_process(process)
            #if key in process.need.keys():
            for pro in process_lst:
                if pro != None:
                    #print('name:', pro.name)
                    self.graph.add_edge(process_name, pro.name)
        return self.graph
    
    def visualize_graph(self, font_color='black', font_weight='bold', node_size=1500, legend=None):
        node_color = ['green' if node == 'start' else 'red' if node == 'end' else 'Orange' for node in self.graph.nodes()]
        pos = nx.circular_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color=node_color, font_color=font_color, font_weight=font_weight, node_size=node_size)

        #edge_labels = {(u,v): f"{self.process[u].result}" for u,v in self.graph.edges()}
        #nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
    
        if legend:
            for label, color in legend.items():
                plt.scatter([], [], c=color, label=label, s=node_size)
            plt.legend(scatterpoints=1, frameon=False, labelspacing=1.5)
        plt.show()


    def add_stock(self, stock_name: str, quantity: int):
        if not isinstance(stock_name, str) or not isinstance(quantity, int):
            raise TypeError(f"Invalid type for stock.")
        self.stock[stock_name] = quantity

    def add_process(self, process_name: str, process: Process):
        if not isinstance(process_name, str) or not isinstance(process, Process):
            raise TypeError(f"Invalid type for process.")
        self.process[process_name] = process

    def add_optimize(self, optimize_name: str):
        if not isinstance(optimize_name, str):
            raise TypeError(f"Invalid type for optimize.")
        if optimize_name not in self.optimize:
            self.optimize.append(optimize_name)

    def __str__(self):
        stock_str = ""
        process_str = ""
        optimize_str = "optimize:("

        for key, value in self.stock.items():
            if value > 0:
                stock_str += key + ":" + str(value) + "\n"

        for key, value in self.process.items():
            process_str += value.__str__() + "\n"

        optimize_len = len(self.optimize)
        for index, elem in enumerate(self.optimize, start=1):
            optimize_str += elem
            if index < optimize_len:
                optimize_str += ";"
        optimize_str += ")"

        return f"{stock_str}\n{process_str}\n{optimize_str}" 
