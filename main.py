import os, sys, argparse
from Lexer import Lexer
from Base import Base

def load_file(input_filename: str) -> object:
    if not os.path.exists(input_filename):
        print(f"Error: File '{input_filename}' does not exist.")
        exit()
    input_file = open(input_filename, "r")
    return input_file


def main():
    parser = argparse.ArgumentParser(
        description="krpsim")
    parser.add_argument("input_filename", nargs="?",
                        help="Path to the input file")

    args = parser.parse_args()

    if args.input_filename is None:
        parser.print_help()
        sys.exit(1)

    if args.input_filename:
        base = Base()
        input_file = load_file(args.input_filename)
        lexer = Lexer()
        lexer.check_syntax(input_file)
        all_tokens = lexer.tokenize(input_file)
        #print(lexer.stock)
        #print(base.stock)
        #print(base.process)
        #print(base.optimize)

        print(base)

if __name__ == "__main__":
    main()
