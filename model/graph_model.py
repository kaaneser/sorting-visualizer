class GraphModel:
    def __init__(self, elements, graph_type, algorithm):
        super().__init__()
        self.elements = elements
        self.graph_type = graph_type
        self.algorithm = algorithm

    def print_info(self):
        print(f"The graph has the elements: {self.elements}\nGraph Type: {self.graph_type}\nAlgorithm: {self.algorithm}")