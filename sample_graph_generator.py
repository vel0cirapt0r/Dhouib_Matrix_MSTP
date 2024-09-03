import random

from decorators import measure_time


@measure_time
def generate_graph(num_nodes=100, num_edges=300):
    # Generate random graph
    graph = {i: {} for i in range(1, num_nodes + 1)}
    for _ in range(num_edges):
        u = random.randint(1, num_nodes)
        v = random.randint(1, num_nodes)
        weight = random.randint(1, 100)  # Random weight for the edge
        graph[u][v] = weight

    return graph
