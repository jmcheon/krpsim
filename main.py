import os, sys, argparse
from Parser import Parser
from Base import Base

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
        parser = Parser()
        parser.parse(input_file)
        #print(base.stock)
        #print(base.process)
        #print(base.optimize)

        print(base)

if __name__ == "__main__":
    main()
