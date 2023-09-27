from Process import Process
import imageio
import copy
import time 
import random
import networkx as nx
import matplotlib.pyplot as plt


class Base:

    def __init__(self):
        # print("Base init()")
        self._initial_stock = {}
        self._stock = {}
        self._process = {}
        self._optimize = []
        self._degrade = []
        self.finite = False
        self.finished = False
        self.next_process_lst = []
        self.max_optimize_process = None
        self.max_optimize_need_stocks = None
        self._graph = nx.DiGraph()
        self._verbose = None

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

    def set_attributes(self, initial_stock, stock, process, optimize):
        self.initial_stock = dict(initial_stock)
        self.stock = dict(stock)
        self.process = dict(process)
        self.optimize = list(optimize)

    def init_stocks(self):
        for stock_name in self.stock.keys():
            self.stock[stock_name] = 0

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
    def degrade(self):
        return self._degrade

    @property
    def graph(self):
        return self._graph

    @property
    def verbose(self):
        return self._verbose

    @initial_stock.setter
    def initial_stock(self, stock):
        # print("setting initial stock")
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

    @degrade.setter
    def degrade(self, degrade):
        if isinstance(degrade, list):
            self._degrade = list(degrade)
        else:
            raise ValueError('Degrade must be a list')

    @graph.setter
    def graph(self, graph):
        if isinstance(graph, nx.DiGraph):
            self._graph = graph
        else:
            raise ValueError('Graph must be an instance of networkx.DiGraph')

    @verbose.setter
    def verbose(self, verbose):
        self._verbose = verbose

    def copy(self):
        return copy.deepcopy(self)

    def print_initial_stocks(self):
        print('---initial stocks---')
        for stock, quantity in self.initial_stock.items():
            print(f'{stock}:{quantity}')
        print('--------------------')

    def print_stocks(self, stock_dict: dict):
        print('--------------')
        for stock, quantity in stock_dict.items():
            print(f'{stock}:{quantity}')
        print('--------------')

    def is_stock_satisfied(self, stock_dict: dict, stock_name: str, quantity: int) -> bool:
        if stock_dict[stock_name] >= quantity:
            return True
        return False

    def is_need_satisfied(self, process: Process) -> bool:
        for stock_name, quantity in process.need.items():
            # print(f'{process.name} stock: {stock}, qty: {quantity}')
            ret = self.is_stock_satisfied(self.stock, stock_name, quantity)
            if ret == False:
                return False
        return True

    def is_optimized(self) -> bool:
        for stock in self.optimize:
            if stock != 'time' and self.stock[stock] > self.initial_stock[stock] and self.finished:
            # if stock != 'time' and self.stock[stock] > self.get_max_optimize_stock_quantity():
            # print(self.get_max_optimize_stock_quantity() + self.initial_stock[stock])
            # if stock != 'time' and self.stock[stock] >= self.get_max_optimize_stock_quantity() + self.initial_stock[stock]:
                return True
        return False

    def is_runnable_next_process(self, stock_dict: dict, process: Process) -> bool:
        stock = dict(stock_dict)
        for stock_name, quantity in process.need.items():
            if self.is_stock_satisfied(stock, stock_name, quantity):
                stock[stock_name] -= quantity
            else:
                return False

        for stock_name, quantity in process.result.items():
            stock[stock_name] += quantity
        process_lst = self.get_available_process_lst()
        if self.is_runnable_next_process == False:
            return False
        return True

    def get_max_optimize_stock_quantity(self) -> int:
        max_quantity = 0
        for process in self.process.values():
            for optimize in self.optimize:
                if optimize != 'time' and optimize in process.result.keys():
                    if max_quantity < process.result[optimize]:
                        max_quantity = process.result[optimize]
        return max_quantity

    def get_max_optimize_process(self) -> object:
        max_quantity = self.get_max_optimize_stock_quantity()
        for process in self.process.values():
            for optimize in self.optimize:
                if optimize != 'time' and optimize in process.result.keys():
                    if max_quantity == process.result[optimize]:
                        self.max_optimize_process = process
                        return process
        return None

    def get_max_optimize_need_stocks(self) -> list:
        if self.max_optimize_process != None:
            process = self.process[self.max_optimize_process]
        else:
            process = self.get_max_optimize_process()
        self.max_optimize_need_stocks = list(process.need.keys())
        # self.max_optimize_need_stocks = process.need.keys()
        # print('optimize need stocks:', self.max_optimize_need_stocks)
        return self.max_optimize_need_stocks

    def get_optimize_process_lst(self) -> list:
        process_lst = []
        for process in self.process.values():
            for optimize in self.optimize:
                if optimize != 'time' and optimize in process.result.keys():
                    process_lst.append(process.name)
        return process_lst

    def get_degrade_process_lst(self) -> list:
        for process in self.process.values():
            for optimize in self.optimize:
                if optimize != 'time' and optimize in process.need.keys():
                    self.degrade.append(process.name)
        return self.degrade

    def get_available_process_lst(self) -> list:
        process_lst = []
        for process in self.process.values():
            if self.is_need_satisfied(process):
                process_lst.append(process.name)
        return process_lst

    def run_process_need(self, stock_dict: dict, process: Process) -> bool:
        need_dict = process.need
        # print(need_dict)
        for stock_name, quantity in need_dict.items():
            # if process.name == 'vente_boite':
            # print('qty:', self.stock[stock])
            if self.is_stock_satisfied(stock_dict, stock_name, quantity):
                stock_dict[stock_name] -= quantity
            else:
                return False

    def run_process_result(self, stock_dict: dict, process: Process) -> bool:
        result_dict = process.result
        # print(result_dict)
        for stock, quantity in result_dict.items():
            if self.verbose:
                # print(self.max_optimize_need_stocks)
                print('result:', stock_dict[stock], 'adding:', quantity)
            stock_dict[stock] += quantity
        return True

    def run_process(self, stock_dict: dict, process: Process) -> bool:
        if self.run_process_need(stock_dict, process) == False:
            return False
        if self.run_process_result(stock_dict, process) == False:
            return False
        if self.verbose:
            print(f'run: ', process.name)
            self.print_stocks(self.stock)
        return True

    def undo_process(self, process: Process):
        need_dict = process.need
        # print(need_dict)
        for stock, quantity in need_dict.items():
            self.stock[stock] += quantity

        result_dict = process.result
        # print(result_dict)
        for stock, quantity in result_dict.items():
            self.stock[stock] -= quantity
        # self.print_stocks()

    def generate_walk(self, inventory, delay) -> list:
        self.walk = []
        stock = dict(self.stock)
        max_cycle = 0
        start_time = time.time()
        while self.is_optimized() == False:
            process_lst = self.get_available_process_lst()
            if len(process_lst) == 0:
                return None
            process_name = random.choice(process_lst)
            if len(self.walk) != 0:
                last_process_name = self.walk[-1]
                if max_cycle < self.process[last_process_name[0]].nb_cycle:
                    max_cycle = self.process[last_process_name[0]].nb_cycle
                self.run_process_need(stock, self.process[process_name])
                if self.is_runnable_next_process(stock, self.process[process_name]) == False:
                    stock = dict(self.stock)
                    self.cycle += int(max_cycle)
                    max_cycle = 0
            elif len(inventory) != 0:
                last_process_name = inventory[-1]
                if max_cycle < self.process[last_process_name[0]].nb_cycle:
                    max_cycle = self.process[last_process_name[0]].nb_cycle
                self.run_process_need(stock, self.process[process_name])
                if self.is_runnable_next_process(stock, self.process[process_name]) == False:
                    stock = dict(self.stock)
                    self.cycle += int(max_cycle)
                    max_cycle = 0
            if self.run_process(self.stock, self.process[process_name]):
                self.walk.append([process_name, self.cycle])
            current_time = time.time()
            self.next_process_lst = self.get_available_process_lst()
            if len(self.next_process_lst) == 0:
                self.finshed = True
                if self.max_optimize_process.name != process_name and process_name not in self.get_optimize_process_lst():
                    self.cycle = 0
                    return None
                else:
                    return self.walk
            if current_time - start_time >= delay:
                break
        return self.walk

    def create_stock_image(self, process_name, i):
        plt.figure(figsize=(10, 6))
        colors = [
            'orange' if stock in self.optimize else 'skyblue' for stock in self.stock.keys()]

        bars = plt.bar(self.stock.keys(), self.stock.values(), color=colors)
        # plt.title(f'Stocks after iteration {i}')
        plt.title(
            f'Stocks after iteration {i * 10}\nCurrent process: {process_name}')
        plt.xlabel('Stock')
        plt.ylabel('Quantity')

        # Rotate x-axis labels
        plt.setp(plt.gca().get_xticklabels(), rotation=45)

        # Add quantity labels on top of each bar
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval,
                     int(yval), va='bottom')  # va: vertical alignment

        plt.tight_layout()
        plt.savefig(f'stock_images/stock_{i}.png')

        # plt.show()
    def save_animated_image(self, i):
        print(f"Creating an animated image... i: {i}")
        images = []
        for i in range(i):
            images.append(imageio.imread(f'stock_images/stock_{i}.png'))
        imageio.mimsave('stocks.gif', images)

    def find_connecting_process(self, process: Process) -> list:
        process_lst = []
        for pro in self.process.values():
            # print(pro.need.keys())
            #if any(elem in list(process.result.keys()) for elem in pro.need.keys()):
            if process.result.keys() == pro.need.keys() and pro != process:
                # if process.result.items() == pro.need.items() and pro != process:
                process_lst.append(pro)
                # print('return:', pro.name)
        return process_lst

    def create_graph(self):
        self.graph.add_node('start')
        for process in self.process.values():
            self.graph.add_edge('start', process.name)
            self.graph.add_edge(process.name, 'start')

        for process in self.process.values():
            process_name, needs, results = process.name, process.need, process.result
            self.graph.add_node(process_name)
            # print(process.result.keys())
            # self.is_need_satisfied(process)
            # for key in process.result.keys():
            # print('key:', key, process.need.keys())
            process_lst = self.find_connecting_process(process)
            # if key in process.need.keys():
            for pro in process_lst:
                if pro != None and pro.name != process_name:
                    # print('name:', pro.name)
                    self.graph.add_edge(process_name, pro.name)

        #print(self.graph.edges())
        return self.graph

    def visualize_graph(self, font_color='black', font_weight='bold', node_size=1500, legend=None):
        node_color = ['green' if node == 'start' else 'red' if node ==
                      'end' else 'Orange' for node in self.graph.nodes()]
        pos = nx.circular_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color=node_color,
                font_color=font_color, font_weight=font_weight, node_size=node_size)

        # edge_labels = {(u,v): f"{self.process[u].result}" for u,v in self.graph.edges()}
        # nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)

        if legend:
            for label, color in legend.items():
                plt.scatter([], [], c=color, label=label, s=node_size)
            plt.legend(scatterpoints=1, frameon=False, labelspacing=1.5)
        plt.show()

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
