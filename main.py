import os
import curses
import sys
import argparse
import networkx as nx
import matplotlib.pyplot as plt
from Parser import Parser
from Base import Base
from Population import Population
from QLearningAgent import QLearningAgent


def load_file(input_filename: str) -> object:
    if not os.path.exists(input_filename):
        print(f"Error: File '{input_filename}' does not exist.")
        exit()
    input_file = open(input_filename, "r")
    return input_file


def main():
    argparser = argparse.ArgumentParser(
        description="krpsim")
    argparser.add_argument("input_filename", nargs="?",
                           help="Path to the input file")

    args = argparser.parse_args()

    if args.input_filename is None:
        argparser.print_help()
        sys.exit(1)

    if args.input_filename:
        agent = QLearningAgent()
        input_file = load_file(args.input_filename)
        parser = Parser(agent)
        parser.parse(input_file)
        agent.initial_stock = agent.stock
        agent.print_initial_stocks()
        #agent.set_resources(base)
        agent.init_agent()

        print("\nPrint Base info:\n")
        print(agent)

    # Example usage
    population_size = 2
    population = Population(population_size)
    initial_population = population.generate_population(agent)
    #initial_population[1].agent.create_stock_image(0)
    #sys.exit()

    print("\nInitial Population:\n")
    for i, individual in enumerate(initial_population):
        #print(f"Individual {i+1}: {individual.individual}")
        #individual.calculate_fitness()
        print('start')
        print(individual.stock)
        #print(individual.fitness)
        prev_indi = agent.copy()
        indi = individual.copy()
        while indi.stock != prev_indi.stock:
            prev_indi = indi
            new_indi = indi.copy()
            new_indi.agent.stock = indi.stock
            new_indi.agent.initial_stock = indi.stock
            new_indi.generate_indi()
            #print(f"Individual {i+1}: {individual.individual}")
            print('new stock:', new_indi.stock)
            indi = new_indi.copy()
            #print(indi.fitness)
        print('end')
        if i == 20:
            break

    # agent.create_graph()
    # agent.visualize_graph()

    # agent.create_graph()
    # agent.visualize_graph()


if __name__ == "__main__":
    main()
