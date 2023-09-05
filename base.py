
class Base:
    stock = {}
    process = {}
    optimize = []

    def add_stock(self, stock_name, quantity):
        if not isinstance(stock_name, str) or not isinstance(quantity, int):
            raise TypeError(f"Invalid type for stock.")
        self.stock[stock_name] = quantity
