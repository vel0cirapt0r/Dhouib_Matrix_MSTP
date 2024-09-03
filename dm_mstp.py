import numpy as np
from decorators import measure_time, handle_errors


class DMMSTP:
    def __init__(self, graph_data):
        """
        Initialize the DMMSTP class with the graph data.

        Parameters:
        graph_data (dict): A dictionary with 'distance_edges' and optional 'travel_time_edges' as keys.
                           Each value is a dictionary where the keys are node IDs and the values are
                           dictionaries with neighboring node IDs and edge weights.
        """
        self.graph_data = graph_data
        self.matrix, self.node_indices = self._initialize_matrix(graph_data['distance_edges'])
        self.min_columns = self._initialize_min_columns(self.matrix)
        self.mst_path = []
        self.marked_rows = set()
        self.marked_columns = set()

    def _initialize_matrix(self, distance_edges):
        """
        Convert the input graph data into an adjacency matrix.

        Parameters: distance_edges (dict): A dictionary with node IDs as keys and dictionaries of neighboring nodes
        with weights as values.

        Returns:
        np.ndarray: Adjacency matrix representing the graph.
        dict: Mapping from nodes to indices.
        """
        nodes = set()
        for node, neighbors in distance_edges.items():
            nodes.add(node)
            nodes.update(neighbors.keys())

        node_indices = {node: index for index, node in enumerate(nodes)}
        n = len(nodes)

        # Initialize adjacency matrix with infinity (or a large value)
        matrix = np.full((n, n), np.inf)

        # Fill in the adjacency matrix with given edge weights
        for node1, neighbors in distance_edges.items():
            i = node_indices[node1]
            for node2, weight in neighbors.items():
                j = node_indices[node2]
                matrix[i][j] = weight
                matrix[j][i] = weight

        return matrix, node_indices

    def _initialize_min_columns(self, matrix):
        """
        Initialize Min-Columns with the minimum value of each unmarked column.

        Parameters:
        matrix (np.ndarray): The adjacency matrix.

        Returns:
        list: A list of minimum values for each unmarked column.
        """
        min_columns = []
        for col in range(matrix.shape[1]):
            if col not in self.marked_columns:
                # Calculate minimum value in the column ignoring marked rows
                col_min = np.min(matrix[:, col])
                min_columns.append(col_min)
            else:
                min_columns.append(np.inf)  # Marked columns are ignored
        return min_columns

    def _update_min_columns(self):
        """
        Update Min-Columns after marking and dropping elements.

        Returns:
        list: Updated list of minimum values for each unmarked column.
        """
        return self._initialize_min_columns(self.matrix)

    def _select_edge(self):
        """
        Find the highest value in Min-Columns and select the corresponding edge.

        Returns:
        tuple: The selected edge as a tuple (i, j, weight).
        """
        max_value = max(self.min_columns)
        column_index = self.min_columns.index(max_value)

        # Find the corresponding row index in the original matrix
        row_index = np.argmin(self.matrix[:, column_index])

        return row_index, column_index, self.matrix[row_index][column_index]

    def _mark_and_drop(self, selected_edge):
        """
        Mark the rows and columns, drop intersecting elements.

        Parameters:
        selected_edge (tuple): The selected edge (i, j, weight).
        """
        i, j, _ = selected_edge

        # Mark the selected row and column
        self.marked_rows.add(i)
        self.marked_columns.add(j)

        # Drop (set to infinity) all elements in the marked row and column
        self.matrix[i, :] = np.inf
        self.matrix[:, j] = np.inf

    def _generate_mst_output(self):
        """
        Prepare the MST path for output.

        Returns:
        list: MST represented by the original node names.
        """
        inverse_node_indices = {v: k for k, v in self.node_indices.items()}
        mst_output = [(inverse_node_indices[i], inverse_node_indices[j], weight) for i, j, weight in self.mst_path]
        return mst_output

    @measure_time
    @handle_errors
    def run(self):
        """
        Execute the DM-MSTP algorithm to find the Minimum Spanning Tree (MST).

        Returns:
        list: The edges that make up the MST.
        """
        for _ in range(len(self.node_indices) - 1):
            selected_edge = self._select_edge()
            self.mst_path.append(selected_edge)

            self._mark_and_drop(selected_edge)
            self.min_columns = self._update_min_columns()

        return self._generate_mst_output()
