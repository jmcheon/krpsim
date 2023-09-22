import numpy as np
import copy, random
import itertools
from Base import Base

class QLearningAgent(Base):

    def __init__(self, num_states=None, num_actions=None, epsilon=0.1, alpha=0.5, gamma=0.9): 
        super().__init__()
        self.num_states = num_states
        self.num_actions = num_actions
        self.q_table = None #np.zeros((num_states, num_actions))
        self.state_mapping = {}
        self.action_mapping = {}
        self.epsilon = epsilon # exploration rate
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor

    def copy(self):
        return copy.copy(self)

    def init_agent(self):
        print('num_states:', 2 ** (len(self.process)))
        print('num_actions:', (len(self.process)))
        #self.print_stocks()
        self.num_states = 2 ** len(self.process)
        self.num_actions = len(self.process)
        #print(self.num_states, self.num_actions)
        self.q_table = np.zeros((self.num_states, self.num_actions))
        self.map_states()
        self.map_actions()
        self.get_degrade_process()
        self.get_max_optimize_need_stocks()

    def set_resources(self, base):
        self.initial_stock = dict(base.initial_stock)
        self.stock = dict(base.stock)
        self.process = dict(base.process)
        self.optimize = list(base.optimize)

    def get_key_from_value(self, dictionary, target_value):
        for key, value in dictionary.items():
            if value == target_value:
                return key
        return None

    def get_reward(self, process_name: str) -> int:
        #print(list(self.process[process_name].result.keys()))
        #print(self.max_optimize_need_stocks)
        if all(elem in list(self.process[process_name].result.keys()) for elem in self.max_optimize_need_stocks):
            return 20
        if process_name in self.degrade:
            return -20
        if process_name == self.max_optimize_process.name:
            #print('Last', process_name)
            return 50
        else:
            return 0

    def map_states(self):
        for i in range(1, len(self.process) + 1):
            for combination in itertools.combinations(self.process, i):
                self.state_mapping[combination] = len(self.state_mapping)
        #print(self.state_mapping)

    def map_actions(self):
        self.action_mapping = {(name): i for i, name in enumerate(self.process)}
        #print(self.action_mapping)

    def epsilon_greedy_policy(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(self.num_actions)
        else:
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        #print(state, action, reward, next_state)
        old_value = self.q_table[state][action]

        next_max_value = np.max(self.q_table[next_state])

        # Bellman equation
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max_value)

        # Update the Q-value with new value for state-action pair
        self.q_table[state][action] = new_value
        #if old_value > 0:
            #print(old_value, new_value)

    def set_q_value(self, state, action, value):
        self.q_table[state][action] = value

    def get_valid_available_process(self, process_lst):
        state_num = self.state_mapping[tuple(process_lst)]
        #print('mapping num:', state_num) 
        action_num = self.epsilon_greedy_policy(self.state_mapping[tuple(process_lst)])

        process_name = self.get_key_from_value(self.action_mapping, action_num)

        while True:

            if process_name not in process_lst:
                self.set_q_value(state_num, action_num, 0)
            else:
                break
            action_num = self.epsilon_greedy_policy(self.state_mapping[tuple(process_lst)])
            process_name = self.get_key_from_value(self.action_mapping, action_num)
        #print(action_num, process_name)
        return action_num, process_name

    def generate_walk(self) -> list:
        walk = []
        v = None
        i = 0
        j = 0
        #while not (self.is_reached_optimizing_process(v) and self.is_optimized()):
        while self.is_optimized() == False:
            #self.print_stocks()
            process_lst = self.get_available_processes()
            #print(process_lst)
            if len(process_lst) == 0:
                print('no more process left')
                # return None
                return walk
            #print(self.degrade)
            #print('process_lst:', process_lst)
            state_num = self.state_mapping[tuple(process_lst)]
            #print('mapping num:', state_num) 
            action_num, process_name = self.get_valid_available_process(process_lst)

            v = process_name
            #print(f'action_num: {action_num}, {process_name}')
            #v = random.choice(process_lst)
            if self.run_process(self.process[v]):
                if v == 'vente_boite':
                    print('adding:', v)
                walk.append(v)
            next_process_lst = self.get_available_processes()
            if len(next_process_lst) == 0:
                print('no more next process left')
                # return None
                return walk
            next_state = self.state_mapping[tuple(next_process_lst)]

            self.update_q_table(state_num, action_num, self.get_reward(process_name) , next_state)
        # print('walk:', walk)
            if i % 10 == 0:
                # self.create_stock_image(v, j)
                j += 1
            i += 1
        print(f'return gen walk: {v}, i: {i}')
        # if i % 10 != 0:
            # self.create_stock_image(v, j)
        # self.save_animated_image(j)
        return walk