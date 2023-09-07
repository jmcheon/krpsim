import random

class Individual:

    def __init__(self, base):
        self.individual = []
        self.fitness = 0
        self.stock = base.stock.copy()
        self.process = base.process.copy()
        self.optimize = base.optimize.copy()

    # Generate an individual (schedule) randomly
    def generate_individual(self) -> 'Individual':
        process_names = list(self.process.keys())

        num_processes = random.randint(1, len(process_names))

        # Randomly select a subset of process names
        selected_process_names = random.sample(process_names, num_processes)

        for process_name in selected_process_names:
            need = self.process[process_name].need
            # random_num = random.randint(1, 10)
            # need = {k: v * random_num for k, v in need.items()}
            #need.values() * random_num
            #print(need, need.values())
            self.individual.append((process_name, need))

        return self

    def calculate_fitness(self):
        # Define process durations and costs
        process_durations = {
            'achat_materiel': 10,
            'realisation_produit': 30,
            'livraison': 20
        }

        # Initialize stock quantities and time
        stocks = self.stock# {'euro': 10}
        time = 0

        # Execute schedule and update stock quantities and time
        for process_name, needs in self.individual:
            results = self.process[process_name].result

            if all(stock_name in stocks and stocks[stock_name] >= qty for stock_name, qty in needs.items()):
                for stock_name, qty in needs.items():
                    stocks[stock_name] -= qty

                duration = process_durations.get(process_name)
                if duration:
                    time += duration

                for result_name, qty in results.items():
                    stocks[result_name] = stocks.get(result_name, 0) + qty

            else:
                break

        client_content_stock = stocks.get('client_content', 0)
        print(stocks.get('client_content', 0))

        intermediate_resources_score = (stocks.get('materiel', 0) * 2) + (stocks.get('produit', 0) *3)

        self.fitness = client_content_stock *5 + intermediate_resources_score
