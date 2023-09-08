import networkx as nx
import matplotlib.pyplot as plt
import re

# Create an empty directed graph
graph = nx.DiGraph()

# Add nodes and edges to represent resource dependencies
dependencies = [
    'make_sec:(clock:1):(clock:1;second:1):1',
    'make_minute:(second:60):(minute:1):6',
    'make_hour:(minute:60):(hour:1):36',
    'make_day:(hour:24):(day:1):86',
    'make_year:(day:365):(year:1):365',
    'start_dream:(minute:1;clock:1):(dream:1):60',
    'start_dream_2:(minute:1;dream:1):(dream:2):60',
    'dream_minute:(second:1;dream:1):(minute:1;dream:2):1',
    'dream_hour:(second:1;dream:2):(hour:1;dream:2):1',
    'dream_day:(second:1;dream:3):(day:1;dream:3):1',
    'end_dream:(dream:3):(clock:1):60'
]

for dependency in dependencies:
    parts = re.split(r"(?![^()]*\)):", dependency)
    
    process_name = parts[0]
    print(process_name)
    
    # Extract needs and results from the dependency string
    needs_str = parts[1].strip('()')
    results_str = parts[2].strip('()')
    print(needs_str)

   # Split needs and results into individual resources
    needs_parts = needs_str.split(';')
    results_parts = results_str.split(';')
    print(needs_parts)

   # Add nodes for each resource (if not already added)
    for part in (needs_parts + results_parts):
        print(part)
        resource_name, _ = part.split(':')
        graph.add_node(resource_name)

   # Add edges representing dependencies
    for need_part in needs_parts:
        _, need_resource_qty = need_part.split(':')
        for result_part in results_parts:
            result_resource_name, _ = result_part.split(':')
            graph.add_edge(result_resource_name, process_name)

# Print the nodes and edges of the graph
print("Nodes:", list(graph.nodes))
print("Edges:", list(graph.edges))

G = graph
pos = nx.circular_layout(G)

nx.draw(G, pos, with_labels=True, node_color='Orange', font_color='black', font_weight='bold', node_size=1500)
plt.show()
