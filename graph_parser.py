import os
import gzip

from decorators import measure_time


class GraphParser:
    def __init__(self):
        pass

    @measure_time
    def parse(self, folder_path):
        coordinate_file, distance_file, travel_time_file = self.find_files(folder_path)
        coordinate_graph = self.parse_coordinate_graph(coordinate_file)
        distance_graph = self.parse_graph_from_file(distance_file)
        travel_time_graph = self.parse_graph_from_file(travel_time_file) if travel_time_file else None

        return self.combine_graphs(coordinate_graph, distance_graph, travel_time_graph)

    def find_files(self, folder_path):
        coordinate_file = None
        distance_file = None
        travel_time_file = None

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if file_name.endswith('.co.gz'):
                coordinate_file = file_path
            elif file_name.endswith('.gr.gz'):
                if 'USA-road-t' in file_name:
                    travel_time_file = file_path
                else:
                    distance_file = file_path

        if coordinate_file is None or distance_file is None:
            raise ValueError("Coordinate or distance file is missing")

        return coordinate_file, distance_file, travel_time_file

    def parse_coordinate_graph(self, file_path):
        graph = {}
        with gzip.open(file_path, 'rt') as f:
            for line in f:
                if line.startswith('v'):
                    parts = line.split()
                    node_id = parts[1]
                    x = int(parts[2])
                    y = int(parts[3])
                    graph[node_id] = (x, y)

        return graph

    def parse_graph_from_file(self, file_path):
        graph = {}
        with gzip.open(file_path, 'rt') as f:
            for line in f:
                if line.startswith('a'):
                    parts = line.split()
                    node_u = int(parts[1])
                    node_v = int(parts[2])
                    weight = int(parts[3])
                    if node_u not in graph:
                        graph[node_u] = {}
                    graph[node_u][node_v] = weight

        return graph

    def combine_graphs(self, coordinate_graph, distance_graph, travel_time_graph):
        combined_graph = {'coordinates': coordinate_graph, 'distance_edges': distance_graph,
                          'travel_time_edges': travel_time_graph}
        return combined_graph

# folder_path = ()
# parser = GraphParser()
# graph = parser.parse(folder_path)
# print(graph)
