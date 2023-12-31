
#  krpsim - Algorithmic project++
>*_Summary: This project may be an algorithmic project, an operational research project, an AI project as well as an industrial project... As you like._*

| Requirements | Skills |
|--------------|--------|
| - `python3.7`<br> - `numpy`<br> - `networkx`<br> - `matplotlib`<br>  | - `Adaptation & creativity`<br> - `Group & interpersonal`<br> - `Algorithms & AI` |

## Usage
```
usage: main.py [-h] [-g] [-v] [-r] [input_filename] [delay]

Krpsim program to optimize the performance of a process chain(graph) using
Q-Learning, maximizing a result or reducing the timeframe as much as possible.

positional arguments:
  input_filename  Path to the input file
  delay           the waiting time the program will not have to exceed

optional arguments:
  -h, --help      show this help message and exit
  -g, --graph     Visualize the graph
  -v, --verbose   Print stock changes
  -r, --random    Optimize randomly without Q-Learning
```


## Resources (Configuration files)

There are 6 given files to optimize
- Ikea
- Inception
- Pomme
- Recre
- Steak
- Simple

and two additional new files
- Workout
- Life

#### File format
In a configuration file, there are initial stocks, processes and optimize section.

The file format containing the process: 
- A # to start each commentary line. 
- A description of the available stocks in the beginning, in a simple </br>
	`<stock_name>:<quantity>` format. 
- A process description </br>
	`<name>:(<need>:<qty>[;<need>:<qty>[...]]):(<result>:<qty>[;<result>:<qty>[...]]):<nb_cycle> `</br>
A process can start as soon as the stocks allow it. This can happen several times in the same cycle. 
- One line only to indicate the elements that would need optimizing containing the key word time : </br>
`optimize:(<stock_name>|time[;<stock_name>|time[...]])`

**Each process can be considered as an action that consumes certain stocks and produces resulting stocks**

There are possible situations in a given configuration file:

- Dead branches that consumes any resources and cripples or stops the goal's achievement
- Loops where certain processes have loops to execute one another
- Blocking situations, occurences where no process can be executed
- Self-sustained

The input files can be separated in two categories, one that ends anyway once resources have been consumed, and another that can run forever.

stop: Ikea, Simple, Steak, Workout</br>
non-stop: Inception, Pomme, Recre, Life

## Implementation
![Krpsim_class_diagram](https://github.com/jmcheon/krpsim/assets/40683323/a0682967-845f-43bb-ae3e-d9aee1caa839)
### Algorithms
- random Walk
- Q-Learning
#### Walk
A walk is a sequence of vertices and edges in a graph that starts at a vertex, follows a series of edges and ends at another vertex.

In a graph where vertices are processes and edges are the connections resulting stocks of a process to need stocks of another process, we can find a walk for every iteration based on the available process list at the moment. It chooses **randomly** from the list and executes it, updates current stock quantities. When the available process list is empty where no process can be executed with the current stocks, it ends the iteration and returns the found walk which is a process chain(list).

#### Q-Leanring
Q-learning is a model-free reinforcement learning algorithm for solving problems where an agent learns to make decisions by interacting with an environment. It is particularly well-suited for problems where the agent must make a sequence of decisions to maximize a culmulative **reward**.

1. **Agent**: The learner or decision-maker that interacts with the environment.
2. **Environment**: The external system or world with which the agent interacts. It provides feedbacks to the agent based on its actions.
3. **State($s$)**: A representation of the current situation or the configuration of the environment.
4. **Action($a$)**: The set of choices or decisions that the agent can make in a given state.
5. **Reward($r$)**: A numerical value that the environment provides to the agent after each action.
It represent the immediate benefit or cost of taking a specific action in a particular state.
6. **Policy($\pi$)**: A strategy or set of rules that the agent uses to decide which action to take in each state.
7. **Q-Value($Q$)**: The expected cumulative reward that the agent can obtain by taking a particular action in a specific state and following a policy $\pi$. It is the function of both the state($s$) and the action($a$).

The goal of Q-learning is to learn the optimal Q-Values for each state-action pair, which enables the agent to make decisions that maximize the cumulative reward over time.
Q-Values are updated iteratively using the following formula:
$$Q(s_t, a_t) = (1 - α)Q(s_t, a_t) + α * [r_t + γ * max(Q(s_{t+1}, a))]$$

##### Define spaces for Q-Learning

To define spaces for Q-Learning, it is necessary to define 3 spaces: state space, action space, and reward space and they should be discrete, not continuous.

##### State space

An available process set is a set of elements, which are processes that can be executed based on the stock quantities in this case.

The possible number of the available process sets for the given input resource, is $2^n$, where $n$ is the number of processes. So, when the number of processes is 18, there can be $2^{18}$ number of combinations of processes that are the available process sets.

so, we can define state space as sets of available processes
##### Action space

Since the number of processes in a configuration file is defined, the action space can be defined as processes

##### Reward space

For reward that the agent obtains after taking an action in a state, can be negative as a penalty or positive as a reward.

- Penalty
	- processes that block the goal's achievement: -100
	- processes only consuming stocks: -50
	- processes that consume the optimize stocks: -20
- Reward
	- process that optimizes the optimize stock: +50
	- processes resulting in stocks that are needed for processes resulting in the optimize stocks: +20
##### [Reward function](QLearningAgent.py)
```python
def  get_reward(self, process_name: str) -> int:
	if  len(self.process[process_name].result) ==  0:
		return  -50
	initial_need_stocks  =  dict(self.max_optimize_process.need)
	need_stocks  =  dict(initial_need_stocks)
	for  stock_name, quantity  in  self.max_optimize_process.need.items():
		need_stocks[stock_name] -=  self.stock[stock_name]
		if  any(qty  ==  0  for  qty  in  need_stocks.values()):
			return  -1

	if  self.is_runnable_next_process(self.stock, self.process[process_name]) == False:
		return  -100
	if  all(elem  in  list(self.process[process_name].result.keys()) for  elem  in  self.max_optimize_need_stocks):
		return  20
	if  process_name  in  self.degrade:
		return  -20
	if  process_name  ==  self.max_optimize_process.name:
		return  50
	else:
		return  0
```

#### Examples based on algorithms
##### Pomme
```
#  krpsim tarte aux pommes
#
four:10
euro:10000
#
buy_pomme:(euro:100):(pomme:700):200
buy_citron:(euro:100):(citron:400):200
buy_oeuf:(euro:100):(oeuf:100):200
buy_farine:(euro:100):(farine:800):200
buy_beurre:(euro:100):(beurre:2000):200
buy_lait:(euro:100):(lait:2000):200
#
separation_oeuf:(oeuf:1):(jaune_oeuf:1;blanc_oeuf:1):2
reunion_oeuf:(jaune_oeuf:1;blanc_oeuf:1):(oeuf:1):1
do_pate_sablee:(oeuf:5;farine:100;beurre:4;lait:5):(pate_sablee:300;blanc_oeuf:3):300
do_pate_feuilletee:(oeuf:3;farine:200;beurre:10;lait:2):(pate_feuilletee:100):800
do_tarte_citron:(pate_feuilletee:100;citron:50;blanc_oeuf:5;four:1):(tarte_citron:5;four:1):60
do_tarte_pomme:(pate_sablee:100;pomme:30;four:1):(tarte_pomme:8;four:1):50
do_flan:(jaune_oeuf:10;lait:4;four:1):(flan:5;four:1):300
do_boite:(tarte_citron:3;tarte_pomme:7;flan:1;euro:30):(boite:1):1
vente_boite:(boite:100):(euro:55000):30
vente_tarte_pomme:(tarte_pomme:10):(euro:100):30
vente_tarte_citron:(tarte_citron:10):(euro:200):30
vente_flan:(flan:10):(euro:300):30
#do_benef:(euro:1):(benefice:1):0
#

#optimize:(benefice)
optimize:(euro)
```
<div align="center">
	
|Stock changes using random walk|
| --- |
| <img src="pomme_walk.gif" alt="Alt Text" width="800" height="400"> |
</div>


The main problem is that the stock that has to be optimized is the same as the initial given stock(`euro`) so it is necessary to buy ingredients to earn more euros.

By implementing the algorithm to find a walk that is a sequence of vertices in a graph, it chooses randomly a process that is runnable at the moment in the available process list according to current stock quantities.

In this case, it chooses to buy more ingredients which consumes more euros than making more money, so along the iteration the amount of ingredients increases whereas the euro decreases and in the end, the `vente_boite` process is executed and it gains 55,000 euros.

Eventually, it sells 100 `boite` to earn 55,000 euro and it buys all the unnecessary ingredients then sells 100 `boite` again so the amount of stock `euro` can't exceed more than 56,000 euro (it sells `tarte_pomme` or `tarte_citron`, which are the intermediate results for acquiring a `boite`, so it can be more than 55,000 euro)




##### Result using random walk
```
> python3 main.py resources/pomme 30 -r
Syntax check passed successfully.
Nice file! 18 processes, 16 stocks, 1 to optimize
Evaluating . done.
Main walk
Stock :
 four => 10
 euro => 120
 pomme => 9981960
 citron => 5255100
 oeuf => 1327021
 farine => 0
 beurre => 33311038
 lait => 33376104
 jaune_oeuf => 2
 blanc_oeuf => 6
 pate_sablee => 7790600
 pate_feuilletee => 1421500
 tarte_citron => 2
 tarte_pomme => 12
 flan => 4
 boite => 76
 ```

##### Result using Q-learning
```
> python3 main.py resources/pomme 30
Syntax check passed successfully.
Nice file! 18 processes, 16 stocks, 1 to optimize
Evaluating . done.
Main walk
Stock :
 four => 10
 euro => 2445370
 pomme => 4658705
 citron => 578150
 oeuf => 37735
 farine => 100
 beurre => 3193498
 lait => 3157117
 jaune_oeuf => 1665
 blanc_oeuf => 88999
 pate_sablee => 991800
 pate_feuilletee => 0
 tarte_citron => 2
 tarte_pomme => 8591
 flan => 429
 boite => 41
```
