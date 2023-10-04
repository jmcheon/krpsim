#  Krpsim - Algorithmic project++
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
- A description of the available stocks in the beginning, in a simple 
	`<stock_name>:<quantity>` format. 
- A process description 
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
