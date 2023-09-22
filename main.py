import os
import sys
import argparse
import networkx as nx
import matplotlib.pyplot as plt
from Parser import Parser
from Base import Base
from Population import Population
from dependency import generate_dependency, visualize_dependency


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
        base = Base()
        input_file = load_file(args.input_filename)
        parser = Parser(base)
        parser.parse(input_file)
        base.initial_stock = base.stock
        base.print_initial_stocks()
        # base.print_stocks()
        # print(base.stock)
        # print(base.process)
        # print(base.optimize)

        # print("\nPrint Base info:\n")
        # print(base)

    generate_dependency(base)
    # visualize_dependency(base)
    # # Example usage
    # population_size = 10
    # population = Population(population_size)
    # initial_population = population.generate_population(base)

    # print("\nInitial Population:\n")
    # for i, individual in enumerate(initial_population):
    #     # print(f"Individual {i+1}: {individual.individual}")
    #     individual.calculate_fitness()
    #     print(individual.fitness)

    # base.create_graph()
    # base.visualize_graph()

    # base.create_graph()
    # base.visualize_graph()


if __name__ == "__main__":
    main()
