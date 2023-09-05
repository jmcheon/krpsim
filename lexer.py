import re
from base import Base
from process import Process

class Lexer(Base):

    def __init__(self):
        pass

    def is_commentary_line(self, line: str) -> bool:
        return line.startswith("#")
    
    def is_stock_line(self, line: str) -> bool:
        return self.is_valid_stock_line(line) and not self.is_commentary_line(line)
    
    def is_process_line(self, line: str) -> bool:
        return self.is_valid_process_line(line) and not self.is_commentary_line(line)
    
    def is_optimize_line(self, line: str) -> bool:
        return self.is_valid_optimize_line(line) and not self.is_commentary_line(line)
        #return line.startswith("optimize:") and not is_commentary_line(line)
    
    def is_valid_stock_line(self, line: str) -> bool:
        #print(f"is_valid_stock_line")
        parts = line.split(":")
    
        if len(parts) != 2:
            return False
    
        stock_name = parts[0].strip()
        quantity = parts[1]. strip()
    
        if stock_name not in self.stock:
            self.add_stock(stock_name, int(quantity))
        if stock_name and quantity.isdigit():
            return True
        return False
    
    def is_valid_process_line(self, line: str) -> bool:
        parts = re.split(r"(?![^()]*\)):", line)
        #print(parts, len(parts))
    
        if len(parts) != 4:
            return False
    
        name = parts[0].strip()
        need = parts[1].strip()
        result = parts[2].strip()
        nb_cycle = parts[3].strip()

        #print(f'need: {need}')
        
    
        def is_part_valid(part):
            sub_parts = part.split(";")
            for sub_part in sub_parts:
                sub_sub_parts = sub_part.split(":")
                #print(sub_sub_parts[0].strip())
                if len(sub_sub_parts) != 2 \
                    or not sub_sub_parts[0].strip() \
                    or not sub_sub_parts[1].strip().isdigit():
                    return False
                if sub_sub_parts[0].strip() not in self.stock:
                    self.add_stock(sub_sub_parts[0].strip(), 0)
            return True
        process = Process(name, need[1:-1], result[1:-1], nb_cycle)
        #print(f'process: {process.name} {process.need}, {process.result} {process.nb_cycle}')
        print(process)
    
        #print(name)
        if (name and
            need.startswith("(") and need.endswith(")") and is_part_valid(need[1:-1]) and
            result.startswith("(") and result.endswith(")") and is_part_valid(result[1:-1]) and
            nb_cycle.isdigit()
        ):
            return True
        return False
    
    def is_valid_optimize_line(self, line: str) -> bool:
        #print(f"is_valid_optimize_line")
        if not line.startswith("optimize:"):
            return False
    
        line = line[len("optimize:"):].strip()
        if not (line.startswith("(") and line.endswith(")")):
            return False
    
        pairs = line[1:-1].split(";")
        #print(pairs)
    
        for pair in pairs:
            #print(pair)
            if pair == "time":
                continue
            if pair != "time" and pair not in self.stock:
                return False
        return True
    
    def check_syntax(self, input_file: object) -> bool:
        stock_section_finished = False
        process_section_finished = False
        optimize_section_finished = False
    
        for line_number, line in enumerate(input_file, start=1):
            line = line.strip()
            #print(f"current line: {line}")
            if not line or self.is_commentary_line(line):
                continue
            if not stock_section_finished:
                #print(f"stock line checking")
                if self.is_stock_line(line):
                    pass
                elif self.is_process_line(line):
                    stock_section_finished = True
                    pass
                else:
                    print(f"Syntax error in {line_number}: Invalid stock format:")
                    print(f"\t<stock_name>:<quantity>")
                    return False
            elif not process_section_finished:
                #print(f"process line checking")
                if self.is_process_line(line):
                    pass
                elif self.is_optimize_line(line):
                    process_section_finished = True
                    pass
                elif line.startswith("optimize:"):
                    process_section_finished = True
                    print(f"Syntax error in {line_number}: Invalid optimize format:")
                    print(f"\toptimize:(<stock_name>|time[;<stock_name>|time[...]])")
                    return False
                else:
                    print(f"Syntax error in {line_number}: Invalid process format:")
                    print(f"\t<name>:(<need>:<qty>[;<need>:<qty>[...]]):(<result>:<qty>[;<result>:<qty>[...]]):<nb_cycle>")
                    return False
            elif not optimize_section_finished:
                #print(f"optimize line checking")
                if self.is_optimize_line(line):
                    optimize_section_finished = True
                    pass
                else:
                    print(f"Syntax error in {line_number}: Invalid optimize format:")
                    print(f"\toptimize:(<stock_name>|time[;<stock_name>|time[...]])")
                    return False
            else:
                print(f"Syntax error in {line_number}: Invalid content after optimization section.")
                return False
        else:
            print(f"Syntax check passed successfully.")
        return True
    
    def tokenize(self, input_file: object) -> list:
        all_tokens = []
        for line in input_file:
            line = line.split("#")[0].strip()
            tokens = line.split()
            all_tokens.extend(tokens)
            #is_valid_process_line(line)
        return all_tokens
