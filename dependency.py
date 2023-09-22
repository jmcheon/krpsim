import networkx as nx
import matplotlib.pyplot as plt


def visualize_dependency(base):
    # Create a directed graph
    G = nx.DiGraph()

    # Create vertices for resource keys and assign values (quantities)
    for key in base.process:
        need_dict = base.process[key].need
        result_dict = base.process[key].result
        print("need", need_dict)
        print("result", result_dict)
        # Add the resource key as a vertex and assign its value (quantity)
        for resource, quantity in need_dict.items():
            if resource not in G:
                G.add_node(resource, quantity=int(quantity))

        # Add edges for resource to outcome with quantities
        for resource, quantity in need_dict.items():
            for outcome, outcome_quantity in result_dict.items():
                G.add_edge(resource, outcome, quantity=int(outcome_quantity))

    # Draw the graph using NetworkX's built-in drawing functions.
    pos = nx.circular_layout(G)

    # Create a dictionary to store vertex values (resource quantities)
    vertex_values = nx.get_node_attributes(G, 'quantity')

    # Specify the nodelist explicitly
    nodelist = list(G.nodes())

    # Create a dictionary to store edge labels (quantities)
    edge_labels = {(u, v): d['quantity'] for u, v, d in G.edges(data=True)}

    # Print the nodelist and target for debugging
    print("Nodelist:", nodelist)

    nx.draw(G, pos, with_labels=True, nodelist=nodelist, node_size=1500,
            node_color='lightblue', font_size=10, font_color='black')

    # Add vertex values as labels
    nx.draw_networkx_labels(G, pos, labels=vertex_values, font_color='black')

    # Add edge labels
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_color='red')

    plt.show()

# Example usage:
# dependency_graph(base)


def generate_dependency(base):
    graph_dict = {}
    # Create vertices for resource keys and assign values (quantities)
    for key in base.process:
        need_dict = base.process[key].need
        result_dict = base.process[key].result
        # Add the resource key as a vertex and assign its value (quantity)
        graph_dict[tuple(need_dict.items())] = tuple(result_dict.items())

    for input_items, output_items in graph_dict.items():
        input_str = ";".join(
            [f"{stock}:{amount}" for stock, amount in input_items])
        output_str = ";".join(
            [f"{stock}:{amount}" for stock, amount in output_items])
        print(f"({input_str}):({output_str})")

    print(graph_dict)
