from Process import Process
import networkx as nx
import matplotlib.pyplot as plt

class Base:

    def __init__(self):
        self._stock = {}
        self._process = {}
        self._optimize = []
        self.graph = nx.DiGraph()

    def set(self, stock, process, optimize, graph):
        self.stock(stock)
        self.process(process)
        self.optimize(optimize)
        #self.graph(graph)
        self.graph = graph

    @property
    def stock(self):
        return self._stock

    @property
    def process(self):
        return self._process

    @property
    def optimize(self):
        return self._optimize

    @stock.setter
    def stock(self, stock):
        self.stock = stock

    @process.setter
    def process(self, process):
        self.process = process

    @optimize.setter
    def optimize(self, optimize):
        self.optimize = optimize 

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

    def find_process(self, key):
        process_lst = []
        for process in self.process.values():
            #print('curr process:', process.name, 'key:', key)
            for pro in self.process.values():
                #print(pro.need.keys())
                #if key in pro.need.keys() and len(pro.need.keys()) == 1 and pro != process:
                if key in pro.need.keys() and pro != process:
                    process_lst.append(pro)
                    #print('return:', pro.name)
        return process_lst

    def create_graph(self):
        for process in self.process.values():
            process_name, needs, results = process.name, process.need, process.result
            self.graph.add_node(process_name)
            #print(process.result.keys())
            self.is_need_satisfied(process)
            for key in process.result.keys():
                #print('key:', key, process.need.keys())
                process_lst = self.find_process(key)
                #if key in process.need.keys():
                for pro in process_lst:
                    if pro != None:
                        #print('name:', pro.name)
                        self.graph.add_edge(process_name, pro.name)
        return self.graph
    
    def visualize_graph(self, font_color='black', font_weight='bold', node_size=1500, legend=None):
        pos = nx.circular_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='Orange', font_color=font_color, font_weight=font_weight, node_size=node_size)
        edge_labels = {(u,v): f"{self.process[u].result}" for u,v in self.graph.edges()}
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
