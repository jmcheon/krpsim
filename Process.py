
class Process:
    def __init__(self, name, need, result, delay):
        self.name = name
        self._need = {}
        self._result = {} 
        self.delay = delay

        self.add_part(self._need, need)
        self.add_part(self._result, result)

    @property
    def need(self):
        return self._need

    @property
    def result(self):
        return self._result

    def add_part(self, to_dict: dict, part: str) -> bool:
        sub_parts = part.split(";")
        for sub_part in sub_parts:
            sub_sub_parts = sub_part.split(":")
            part_name = sub_sub_parts[0].strip()
            part_quantity = sub_sub_parts[1].strip()
            #print(f'current need: {part_name}:{part_quantity}')
            if len(sub_sub_parts) != 2 \
                or not part_name \
                or not part_quantity.isdigit():
                return False
            to_dict[part_name] = int(part_quantity)
        return True

    def reform_part_string(self, from_dict: dict) -> str:
        part_str = ""
        part_len = len(from_dict.items())
        for index, (key, value) in enumerate(from_dict.items(), start=1):
            part_str += key + ":" + str(value)
            if part_len >= 2 and index != part_len:
                part_str += ";"
        return part_str

    def __str__(self):
        return f"{self.name}:({self.reform_part_string(self.need)}):({self.reform_part_string(self.result)}):{self.delay}"
