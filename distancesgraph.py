class DistancesGraph(object):

    # Initialize the matrix
    def __init__(self, adjMatrix):
        self.adjMatrix = adjMatrix
        self.size = len(adjMatrix)

    # Add edges
    def add_edge(self, v1, v2, weight):
        if v1 == v2:
            self.adjMatrix[v1][v2] = 0
        self.adjMatrix[v1][v2] = weight
        self.adjMatrix[v2][v1] = weight

    # Remove edges
    def remove_edge(self, v1, v2):
        if self.adjMatrix[v1][v2] == 0:
            return
        self.adjMatrix[v1][v2] = -1
        self.adjMatrix[v2][v1] = -1

    # Get Distance
    def get_distance(self, v1, v2):
        return self.adjMatrix[v1][v2]

    def __len__(self):
        return self.size

    # Print the matrix
    def print_matrix(self):
        for row in self.adjMatrix:
            for val in row:
                print('{:4}'.format(val)),
            print
