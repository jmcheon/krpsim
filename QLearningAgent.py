import numpy as np
import copy
import time
import itertools
from Base import Base


class QLearningAgent(Base):

    def __init__(self, num_states=None, num_actions=None, epsilon=0.1, alpha=0.5, gamma=0.9):
        super().__init__()
        self.walk = []
        self.num_states = num_states
        self.num_actions = num_actions
        self.q_table = None  # np.zeros((num_states, num_actions))
        self.state_mapping = {}
        self.action_mapping = {}
        self.cycle = 0
        self.epsilon = epsilon  # exploration rate
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # discount factor

    def copy(self):
        return copy.deepcopy(self)

    def init_agent(self, verbose):
        if verbose:
            print('num_states:', 2 ** (len(self.process)))
            print('num_actions:', (len(self.process)))
            self.verbose = verbose
        # self.print_stocks(self.stock)
        self.num_states = 2 ** len(self.process)
        self.num_actions = len(self.process)
        self.q_table = np.zeros((self.num_states, self.num_actions))
        self.map_states()
        self.map_actions()
        self.get_degrade_process_lst()
        self.get_max_optimize_need_stocks()

    def set_resources(self, base: Base):
        self.initial_stock = dict(base.initial_stock)
        self.stock = dict(base.stock)
        self.process = dict(base.process)
        self.optimize = list(base.optimize)

    def map_states(self):
        for i in range(1, len(self.process) + 1):
            for combination in itertools.combinations(self.process, i):
                self.state_mapping[combination] = len(self.state_mapping)

    def map_actions(self):
        self.action_mapping = {
            (name): i for i, name in enumerate(self.process)}

    def epsilon_greedy_policy(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(self.num_actions)
        else:
            return np.argmax(self.q_table[state])

    def update_q_table(self, state:int , action: int, reward: int, next_state: int):
        old_value = self.q_table[state][action]

        next_max_value = np.max(self.q_table[next_state])

        # Bellman equation
        new_value = (1 - self.alpha) * old_value + self.alpha * \
            (reward + self.gamma * next_max_value)

        # Update the Q-value with new value for state-action pair
        self.q_table[state][action] = new_value

    def set_q_value(self, state, action, value):
        self.q_table[state][action] = value

    def get_key_from_value(self, dictionary: dict, target_value):
        for key, value in dictionary.items():
            if value == target_value:
                return key
        return None

    def get_reward(self, process_name: str) -> int:
        if len(self.process[process_name].result) == 0:
            return -50
        initial_need_stocks = dict(self.max_optimize_process.need)
        need_stocks = dict(initial_need_stocks)
        for stock_name, quantity in self.max_optimize_process.need.items():
            need_stocks[stock_name] -= self.stock[stock_name]
            if any(qty == 0 for qty in need_stocks.values()):
                return -1

        if self.is_runnable_next_process(self.stock, self.process[process_name]) == False:
            return -100
        if all(elem in list(self.process[process_name].result.keys()) for elem in self.max_optimize_need_stocks):
            return 20
        if process_name in self.degrade:
            return -20
        if process_name == self.max_optimize_process.name:
            return 50
        else:
            return 0

    def get_valid_available_process(self, process_lst: list):
        state_num = self.state_mapping[tuple(process_lst)]
        action_num = self.epsilon_greedy_policy(
            self.state_mapping[tuple(process_lst)])
        process_name = self.get_key_from_value(self.action_mapping, action_num)

        while True:
            if process_name not in process_lst:
                self.set_q_value(state_num, action_num, 0)
            else:
                break
            action_num = self.epsilon_greedy_policy(
                self.state_mapping[tuple(process_lst)])
            process_name = self.get_key_from_value(
                self.action_mapping, action_num)
        return action_num, process_name

    def generate_inventory(self, inventory: list, delay: int) -> list:
        self.walk = []
        stock = dict(self.stock)
        max_cycle = 0
        start_time = time.time()
        while self.is_optimized() == False:
            process_lst = self.get_available_process_lst()
            if len(process_lst) == 0:
                return None
            state_num = self.state_mapping[tuple(process_lst)]
            action_num, process_name = self.get_valid_available_process(
                process_lst)

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

            next_process_lst = self.get_available_process_lst()
            if len(next_process_lst) == 0:
                self.finshed = True
                if self.max_optimize_process.name != process_name and process_name not in self.get_optimize_process_lst():
                    self.cycle = 0
                    return None
                else:
                    return self.walk
            next_state = self.state_mapping[tuple(next_process_lst)]
            self.update_q_table(state_num, action_num,
                                self.get_reward(process_name), next_state)
            if current_time - start_time >= delay:
                break

        return self.walk
