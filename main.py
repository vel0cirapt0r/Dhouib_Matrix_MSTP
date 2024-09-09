import argparse
from sample_graph_generator import generate_graph
from graph_parser import GraphParser
from dm_mstp import DMMSTP


def get_user_input_for_graph():
    # Interactive prompt to get graph input from the user
    input_type = input("Choose input type (1: File, 2: Sample Graph, 3: Manual Entry): ")

    if input_type == '1':
        file_path = input("Enter the folder path containing the graph files: ")
        return load_graph_from_file(file_path)
    elif input_type == '2':
        num_nodes = int(input("Enter number of nodes for the sample graph: "))
        num_edges = int(input("Enter number of edges for the sample graph: "))
        print(generate_graph(num_nodes, num_edges))
        return generate_graph(num_nodes, num_edges)
    elif input_type == '3':
        return get_manual_graph_input()
    else:
        print("Invalid option")
        return get_user_input_for_graph()


def load_graph_from_file(folder_path):
    parser = GraphParser()
    return parser.parse(folder_path)


def get_manual_graph_input():
    # Logic for manually entering a graph (example: adjacency list format)
    graph_data = {}
    num_nodes = int(input("Enter number of nodes: "))
    for i in range(num_nodes):
        node = int(input(f"Enter node {i + 1} ID: "))
        neighbors = {}
        num_neighbors = int(input(f"How many neighbors for node {node}? "))
        for _ in range(num_neighbors):
            neighbor = int(input("Enter neighbor ID: "))
            weight = int(input("Enter edge weight: "))
            neighbors[neighbor] = weight
        graph_data[node] = neighbors
    return {'distance_edges': graph_data}


def run_dm_mstp(graph_data):
    dm_mstp = DMMSTP(graph_data)
    return dm_mstp.run()


def main():
    parser = argparse.ArgumentParser(description="Run the DM-MSTP algorithm.")

    # Define arguments
    parser.add_argument('--file', type=str, help="Path to the folder containing graph files")
    parser.add_argument('--sample', action='store_true', help="Generate a sample graph")
    parser.add_argument('--manual', action='store_true', help="Input graph manually")

    # Parse the arguments
    args = parser.parse_args()

    # If no argument provided, ask the user interactively
    if not any(vars(args).values()):
        print("No input provided. Switching to interactive mode.")
        graph_data = get_user_input_for_graph()
    else:
        # If file argument is provided
        if args.file:
            graphs_data = load_graph_from_file(args.file)
            graph_data = graphs_data['distance_edges']
        # If sample graph option is chosen
        elif args.sample:
            num_nodes = int(input("Enter number of nodes for the sample graph: "))
            num_edges = int(input("Enter number of edges for the sample graph: "))
            graph_data = generate_graph(num_nodes, num_edges)
            print("Generated Graph:", graph_data)

        # If manual input option is chosen
        elif args.manual:
            graph_data = get_manual_graph_input()

    # Run the DM-MSTP algorithm
    mst_path = run_dm_mstp(graph_data)
    print("MST Path:", mst_path)


if __name__ == '__main__':
    main()
