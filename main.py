import os
import sys
import argparse
from Parser import Parser
from QLearningAgent import QLearningAgent
from Krpsim import Krpsim


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
        input_file = load_file(args.input_filename)

        agent = QLearningAgent()
        parser = Parser(agent)
        parser.parse(input_file)
        agent.initial_stock = agent.stock
        agent.print_initial_stocks()
        agent.init_agent()

        print("\nPrint Base info:\n")
        print(agent)


    krpsim = Krpsim(agent, 0)
    krpsim.optimize()

    # agent.create_graph()
    # agent.visualize_graph()


if __name__ == "__main__":
    main()
