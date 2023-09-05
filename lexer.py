import os, argparse, sys, re

def load_file(input_filename: str) -> object:
    if not os.path.exists(input_filename):
        print(f"Error: File '{input_filename}' does not exist.")
        exit()
    input_file = open(input_filename, "r")
    return input_file


def is_commentary_line(line: str) -> bool:
    return line.startswith("#")

def is_stock_line(line: str, stock_lst: list) -> bool:
    return is_stock_line_valid(line, stock_lst) and not is_commentary_line(line)

def is_process_line(line: str, stock_lst: list) -> bool:
    return is_process_line_valid(line, stock_lst) and not is_commentary_line(line)

def is_optimize_line(line: str, stock_lst: list) -> bool:
    return is_optimize_line_valid(line, stock_lst) and not is_commentary_line(line)
    #return line.startswith("optimize:") and not is_commentary_line(line)

def is_stock_line_valid(line: str, stock_lst: list) -> bool:
    #print(f"is_stock_line_valid")
    parts = line.split(":")

    if len(parts) != 2:
        return False

    stock_name = parts[0].strip()
    quantity = parts[1]. strip()

    if stock_name not in stock_lst:
        stock_lst.append(stock_name)
    if stock_name and quantity.isdigit():
        return True
    return False

def is_process_line_valid(line: str, stock_lst: list) -> bool:
    parts = re.split(r"(?![^()]*\)):", line)
    #print(parts, len(parts))

    if len(parts) != 4:
        return False

    name = parts[0].strip()
    need = parts[1].strip()
    result = parts[2].strip()
    nb_cycle = parts[3].strip()

    def is_part_valid(part):
        sub_parts = part.split(";")
        for sub_part in sub_parts:
            sub_sub_parts = sub_part.split(":")
            #print(sub_sub_parts[0].strip())
            if len(sub_sub_parts) != 2 \
                or not sub_sub_parts[0].strip() \
                or not sub_sub_parts[1].strip().isdigit():
                return False
            if sub_sub_parts[0].strip() not in stock_lst:
                stock_lst.append(sub_sub_parts[0].strip())
        return True

    #print(name)
    if (name and
        need.startswith("(") and need.endswith(")") and is_part_valid(need[1:-1]) and
        result.startswith("(") and result.endswith(")") and is_part_valid(result[1:-1]) and
        nb_cycle.isdigit()
    ):
        return True
    return False

def is_optimize_line_valid(line: str, stock_lst: list) -> bool:
    #print(f"is_optimize_line_valid")
    if not line.startswith("optimize:"):
        return False

    line = line[len("optimize:"):].strip()
    pairs = line[1:-1].split(";")
    #print(pairs)
    #print(stock_lst)

    for pair in pairs:
        #print(pair)
        if "time" == pair:
            continue
        if pair != "time" and pair not in stock_lst:
            return False
    return True

def check_syntax(input_file: object):
    stock_section_finished = False
    process_section_finished = False
    optimize_section_finished = False
    stock_lst = []

    for line_number, line in enumerate(input_file, start=1):
        line = line.strip()
        #print(f"current line: {line}")
        if not line or is_commentary_line(line):
            continue
        if not stock_section_finished:
            #print(f"stock line checking")
            if is_stock_line(line, stock_lst):
                pass
            elif is_process_line(line, stock_lst):
                stock_section_finished = True
                pass
            else:
                print(f"Syntax error in {line_number}: Invalid stock format:")
                print(f"\t<stock_name>:<quantity>")
                break
        elif not process_section_finished:
            #print(f"process line checking")
            if is_process_line(line, stock_lst):
                pass
            elif is_optimize_line(line, stock_lst):
                process_section_finished = True
                pass
            else:
                print(f"Syntax error in {line_number}: Invalid process format:")
                print(f"\t<name>:(<need>:<qty>[;<need>:<qty>[...]]):(<result>:<qty>[;<result>:<qty>[...]]):<nb_cycle>")
                break
        elif not optimize_section_finished:
            #print(f"optimize line checking")
            if is_optimize_line(line, stock_lst):
                optimize_section_finished = True
                pass
            else:
                print(f"Syntax error in {line_number}: Invalid optimize format:")
                print(f"\toptimize:(<stock_name>|time[;<stock_name>|time[...]])")
                break
        else:
            print(f"Syntax error in {line_number}: Invalid content after optimization section.")
    else:
        print(f"Syntax check passed successfully.")



def tokenize(input_file: object) -> list:
    all_tokens = []
    for line in input_file:
        line = line.split("#")[0].strip()
        tokens = line.split()
        all_tokens.extend(tokens)
        #is_process_line_valid(line)
    return all_tokens

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="krpsim.")
    parser.add_argument("input_filename", nargs="?",
                        help="Path to the input file")

    args = parser.parse_args()

    if args.input_filename is None:
        parser.print_help()
        sys.exit(1)

    input_file = load_file(args.input_filename)
    check_syntax(input_file)
    all_tokens = tokenize(input_file)
