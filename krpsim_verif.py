import os
import sys
import argparse
from Parser import Parser
from QLearningAgent import QLearningAgent
from Krpsim import Krpsim
from Base import Base


def parse_result(input_result: object):
    inventory_begin = False
    inventory = []
    for line_number, line in enumerate(input_result, start=1):
        line = line.strip()
        if inventory_begin and (line.startswith("no more process") or line == "Stock :"):
            return inventory
        if inventory_begin == True:
            inventory.append(line.split(":"))
        if line == "Main walk":
            inventory_begin = True


def load_file(input_filename: str) -> object:
    if not os.path.exists(input_filename):
        print(f"Error: File '{input_filename}' does not exist.")
        exit()
    input_file = open(input_filename, "r")
    return input_file


def check_process_name(inventory, process):
    for item in inventory:
        if item[1] not in process:
            return False
    return True


def print_nice_stock(stock, mark):
    print(f"Stock ({mark}) :")
    for key, value in stock.items():
        print(f" {key} => {value}")


def main():
    argparser = argparse.ArgumentParser(
        description="krpsim")
    argparser.add_argument("file", nargs="?",
                           help="Path to the input file")
    argparser.add_argument("result_to_test", nargs="?",
                           help="Text file containing the krpsim trace")

    args = argparser.parse_args()

    if args.file:
        input_file = load_file(args.file)

        agent = QLearningAgent()
        parser = Parser(agent)
        parser.parse(input_file)
        agent.initial_stock = agent.stock
        agent.print_initial_stocks()

    if args.result_to_test:
        input_result = load_file(args.result_to_test)
        inventory = parse_result(input_result)

    if check_process_name(inventory, agent.process) is False:
        print("Error: process name mismatch.")
        sys.exit(1)

    stock_copy = dict(agent.initial_stock)
    begin_range = 0
    prev_cycle = 0
    for i in range(len(inventory)):
        print("Process", i, ":", inventory[i][1], "/ cycle:", inventory[i][0])
        # print(agent.process[inventory[i][1]].need)
        # agent.run_process_need(stock_copy, agent.process[inventory[i][1]])
        stock_copy = {
            key: stock_copy[key] - agent.process[inventory[i][1]].need.get(key, 0) for key in stock_copy}
        if prev_cycle == int(inventory[i][0]):
            if any(value < 0 for value in stock_copy.values()):
                print(
                    f"Error: Excueted process not valid. -- for Process {i} : {inventory[i][1]}")
                print_nice_stock({
                    key: stock_copy[key] + agent.process[inventory[i][1]].need.get(key, 0) for key in stock_copy}, "before")
                print_nice_stock(stock_copy, "after")
                sys.exit(1)
        else:
            max_cycle = 0
            print(begin_range)

            for j in range(begin_range, i):
                if max_cycle < agent.process[inventory[j][1]].nb_cycle:
                    max_cycle = agent.process[inventory[j][1]].nb_cycle
            for j in range(begin_range, i):
                stock_copy = {
                    key: stock_copy[key] + agent.process[inventory[j][1]].result.get(key, 0) for key in stock_copy}
            if (prev_cycle + max_cycle) != int(inventory[i][0]):
                print(max_cycle, int(inventory[i][0]))
                print("Error: incorrect number of cycle")
                sys.exit(1)
            begin_range = i
            prev_cycle = int(inventory[i][0])
        # total_cycle += 0
        # print(total_cycle)
        # print(stock_copy)


if __name__ == "__main__":
    main()
