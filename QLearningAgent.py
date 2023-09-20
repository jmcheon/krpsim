import numpy as np

class QLearningAgent:

    def __init__(self, num_states, num_actions, epsilon=0.1, alpha=0.5, gamma=0.9): 
        self.num_states = num_states
        self.num_actions = num_actions
        self.epsilon = epsilon # exploration rate
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor
        self.q_table = np.zeros((num_states, num_actions))
        self.state_mapping = {}
        self.action_mapping = {}

    def map_states(self):
        for i in range(1, len(self.process) + 1):
            for combination in itertools.combinations(self.process, i):
                self.state_mapping[combination] = len(self.state_mapping)
        #print(self.state_mapping)

    def map_actions(self):
        self.action_mapping = {(name): i for i, name in enumerate(self.process)}

    def epsilon_greedy_policy(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(self.num_actions)
        else:
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        old_value = self.q_table[state][action]

        next_max_value = np.max(self.q_table[next_state])

        # Bellman equation
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max_value)

        # Update the Q-value with new value for state-action pair
        self.q_table[state][action] = new_value

    def generate_walk(self) -> list:
        walk = []
        #while self.is_optimized() == False:
        v = None
        i = 0
        j = 0
        #while not (self.is_reached_optimizing_process(v) and self.is_optimized()):
        while self.is_optimized() == False:
            process_lst = self.get_available_processes()
            #print(process_lst)
            if len(process_lst) == 0:
                print('no more process left')
                # return None
                return walk
            #v = random.choice(process_lst)
            #print('mapping num:', self.state_mapping[tuple(process_lst)], process_lst)
            v = self.agent.epsilon_greedy_policy(self.state_mapping[tuple(process_lst)])
            print(f'v: {v}')
            if self.run_process(self.process[v]):
                if v == 'vente_boite':
                    print('adding:', v)
                walk.append(v)
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
