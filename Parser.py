import re
from Process import Process


class Parser:

    def __init__(self, base):
        self.base = base

    def is_commentary_line(self, line: str) -> bool:
        return line.startswith("#")

    def is_stock_line(self, line: str) -> bool:
        return self.is_valid_stock_line(line) and not self.is_commentary_line(line)

    def is_process_line(self, line: str) -> bool:
        return self.is_valid_process_line(line) and not self.is_commentary_line(line)

    def is_optimize_line(self, line: str) -> bool:
        return self.is_valid_optimize_line(line) and not self.is_commentary_line(line)
        # return line.startswith("optimize:") and not is_commentary_line(line)

    def is_valid_stock_line(self, line: str) -> bool:
        # print(f"is_valid_stock_line")
        parts = line.split(":")

        if len(parts) != 2:
            return False

        stock_name = parts[0].strip()
        quantity = parts[1]. strip()

        if stock_name not in self.base.stock:
            self.base.add_stock(stock_name, int(quantity))
        if stock_name and quantity.isdigit():
            return True
        return False

    def is_valid_process_line(self, line: str) -> bool:
        parts = re.split(r"(?![^()]*\)):", line)
        # print(parts, len(parts))

        if len(parts) != 4:
            return False

        name = parts[0].strip()
        need = parts[1].strip()
        result = parts[2].strip()
        nb_cycle = parts[3].strip()

        # print(f'need: {need}')

        def is_part_valid(part):
            sub_parts = part.split(";")
            for sub_part in sub_parts:
                sub_sub_parts = sub_part.split(":")
                # print(sub_sub_parts[0].strip())
                stock_name = sub_sub_parts[0].strip()
                stock_quantity = sub_sub_parts[1].strip()
                if len(sub_sub_parts) != 2 \
                        or not stock_name \
                        or not stock_quantity.isdigit():
                    return False
                if stock_name not in self.base.stock:
                    self.base.add_stock(stock_name, 0)
            return True
        # process = Process(name, need[1:-1], result[1:-1], nb_cycle)
        # print(f'process: {process.name} {process.need}, {process.result} {process.nb_cycle}')
        # print(process)

        if len(result) == 0:
            print(f'result: {result}')
            if (name and
                need.startswith("(") and need.endswith(")") and is_part_valid(need[1:-1]) and
                nb_cycle.isdigit()
                ):
                process = Process(name, need[1:-1], result[1:-1], nb_cycle)
                self.base.add_process(name, process)
                # print(process.need, process.result)
                return True
            return False

        # print(name)
        elif (name and
              need.startswith("(") and need.endswith(")") and is_part_valid(need[1:-1]) and
              result.startswith("(") and result.endswith(")") and is_part_valid(result[1:-1]) and
              nb_cycle.isdigit()
              ):
            process = Process(name, need[1:-1], result[1:-1], nb_cycle)
            self.base.add_process(name, process)
            # print(process.need, process.result)
            return True
        return False

    def is_valid_optimize_line(self, line: str) -> bool:
        # print(f"is_valid_optimize_line")
        if not line.startswith("optimize:"):
            return False

        line = line[len("optimize:"):].strip()
        if not (line.startswith("(") and line.endswith(")")):
            return False

        pairs = line[1:-1].split(";")
        # print(pairs)

        for pair in pairs:
            # print(pair)
            if pair != "time" and pair not in self.base.stock:
                return False
            self.base.add_optimize(pair)
        return True

    def parse(self, input_file: object) -> bool:
        stock_section_finished = False
        process_section_finished = False
        optimize_section_finished = False

        for line_number, line in enumerate(input_file, start=1):
            line = line.strip()
            # print(f"current line: {line}")
            if not line or self.is_commentary_line(line):
                continue
            if not stock_section_finished:
                # print(f"stock line checking")
                if self.is_stock_line(line):
                    pass
                elif self.is_process_line(line):
                    stock_section_finished = True
                    pass
                else:
                    print(
                        f"Syntax error in {line_number}: Invalid stock format:")
                    print(f"\t<stock_name>:<quantity>")
                    return False
            elif not process_section_finished:
                # print(f"process line checking")
                if self.is_process_line(line):
                    pass
                elif self.is_optimize_line(line):
                    process_section_finished = True
                    pass
                elif line.startswith("optimize:"):
                    process_section_finished = True
                    print(
                        f"Syntax error in {line_number}: Invalid optimize format:")
                    print(
                        f"\toptimize:(<stock_name>|time[;<stock_name>|time[...]])")
                    return False
                else:
                    print(
                        f"Syntax error in {line_number}: Invalid process format:")
                    print(
                        f"\t<name>:(<need>:<qty>[;<need>:<qty>[...]]):(<result>:<qty>[;<result>:<qty>[...]]):<nb_cycle>")
                    return False
            elif not optimize_section_finished:
                # print(f"optimize line checking")
                if self.is_optimize_line(line):
                    optimize_section_finished = True
                    pass
                else:
                    print(
                        f"Syntax error in {line_number}: Invalid optimize format:")
                    print(
                        f"\toptimize:(<stock_name>|time[;<stock_name>|time[...]])")
                    return False
            else:
                print(
                    f"Syntax error in {line_number}: Invalid content after optimization section.")
                return False
        else:
            print(f"Syntax check passed successfully.")
            print(f"Nice file! ")
        return True

    def __str__(self):
        stock_str = ""
        process_str = ""
        optimize_str = "optimize:("

        for key, value in self.base.stock.items():
            if value > 0:
                stock_str += key + ":" + str(value) + "\n"

        for key, value in self.base.process.items():
            process_str += value.__str__() + "\n"

        optimize_len = len(self.base.optimize)
        for index, elem in enumerate(self.base.optimize, start=1):
            optimize_str += elem
            if index < optimize_len:
                optimize_str += ";"
        optimize_str += ")"

        return f"{stock_str}\n{process_str}\n{optimize_str}"
