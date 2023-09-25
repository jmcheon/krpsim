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
    argparser.add_argument("delay", nargs="?",
                           help="the waiting time the program will not have to exceed")

    argparser.add_argument("-g", "--graph", action="store_true",
                           help="Visualize the graph")

    argparser.add_argument("-v", "--verbose", action="store_true",
                           help="Visualize the graph")

    args = argparser.parse_args()

    if args.input_filename is None or args.delay is None:
        argparser.print_help()
        sys.exit(1)

    try:
        delay_seconds = int(args.delay)
    except ValueError:
        print(f"Error: '{args.delay}' is not a valid integer for delay")
        sys.exit(1)

    if args.input_filename:
        input_file = load_file(args.input_filename)

        agent = QLearningAgent()
        parser = Parser(agent)
        if parser.parse(input_file) == False:
            sys.exit(1)
        agent.initial_stock = agent.stock
        if args.verbose:
            agent.print_initial_stocks()
        agent.init_agent(args.verbose)

        print(
            f"Nice file! {len(agent.process)} processes, {len(agent.initial_stock)} stocks, {len(agent.optimize)} to optimize")

        if args.verbose:
            print("\nPrint Base info:\n")
            print(agent)

    krpsim = Krpsim(agent, delay_seconds, args.verbose)
    krpsim.optimize()

    if args.graph:
        agent.create_graph()
        agent.visualize_graph()


if __name__ == "__main__":
    main()
