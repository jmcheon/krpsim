import os
import curses
import sys
import argparse
import networkx as nx
import matplotlib.pyplot as plt
from Parser import Parser
from Base import Base
from Individual import Individual
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


    individual = Individual(agent) 
    print('start')
    print('individual.stock:', individual.stock)
    prev_indi = agent.copy()
    prev_indi.init_stocks() 
    indi = individual.copy()
    while indi.stock != prev_indi.stock:
        prev_indi = indi
        new_indi = indi.copy()
        new_indi.agent.stock = indi.stock
        new_indi.agent.initial_stock = indi.stock
        new_indi.generate_indi()
        print('new stock:', new_indi.stock)
        indi = new_indi.copy()
    print('end')

    # agent.create_graph()
    # agent.visualize_graph()


if __name__ == "__main__":
    main()
