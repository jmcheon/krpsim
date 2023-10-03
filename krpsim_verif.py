import os
import sys
import argparse
from Parser import Parser
from QLearningAgent import QLearningAgent


def parse_result(input_result: object):
    inventory_begin = False
    inventory = []
    for line_number, line in enumerate(input_result, start=1):
        line = line.strip()
        if inventory_begin and (line.startswith("no more process") or line == "Stock :"):
            break
        if inventory_begin == True:
            inventory.append(line.split(":"))
        if line == "Main walk":
            inventory_begin = True
    result_stock = {}
    for line_number, line in enumerate(input_result):
        parts = line.strip().split(" => ")

        # Check if there are two parts (key and value)
        if len(parts) == 2:
            key, value = parts
            # Convert the value to an integer
            try:
                value = int(value)
            except ValueError:
                # Handle the case where the value is not an integer
                pass
            # Add the key-value pair to the dictionary
            result_stock[key] = value
    return inventory, result_stock


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
        inventory, result_stock = parse_result(input_result)

    if check_process_name(inventory, agent.process) is False:
        print("Error: process name mismatch.")
        sys.exit(1)

    stock_copy = dict(agent.initial_stock)
    begin_range = 0
    prev_cycle = 0
    process_todo = []
    for i in range(len(inventory)):
        print("Process", i, ":", inventory[i][1], "/ cycle:", inventory[i][0])
        if prev_cycle != int(inventory[i][0]):
            if prev_cycle > int(inventory[i][0]):
                print("Error: Cycle number wrong")
                sys.exit(1)
            for j in range(begin_range, i):
                process_todo.append(
                    [agent.process[inventory[j][1]].nb_cycle, inventory[j][1]])
            to_remove = []
            for k in range(len(process_todo)):
                if (agent.process[process_todo[k][1]].nb_cycle + prev_cycle) <= int(inventory[i][0]) and not any(value < 0 for value in {
                        key: stock_copy[key] - agent.process[process_todo[k][1]].need.get(key, 0) for key in stock_copy}.values()):
                    stock_copy = {
                        key: stock_copy[key] - agent.process[process_todo[k][1]].need.get(key, 0) for key in stock_copy}
                    stock_copy = {
                        key: stock_copy[key] + agent.process[process_todo[k][1]].result.get(key, 0) for key in stock_copy}
                    to_remove.append(k)
            flag = False
            for k in reversed(to_remove):
                if (agent.process[process_todo[k][1]].nb_cycle + prev_cycle) == int(inventory[i][0]):
                    flag = True
                process_todo.pop(k)
            if flag == False:
                print("Error: incorrect number of cycle")
                sys.exit(1)
            begin_range = i
            prev_cycle = int(inventory[i][0])
            if any(value < 0 for value in stock_copy.values()):
                print(
                    f"Error: Excueted process not valid.")
                print_nice_stock(stock_copy, "")
                sys.exit(1)

if __name__ == "__main__":
    main()
