# Zackery Ayscue 000901676
class DistancesGraph(object):

    # Initialize the matrix
    def __init__(self, adjMatrix):
        self.adjMatrix = adjMatrix
        self.size = len(adjMatrix)

    # Add edges
    # O(n) = O(1)
    def add_edge(self, v1, v2, weight):
        if v1 == v2:
            self.adjMatrix[v1][v2] = 0
        self.adjMatrix[v1][v2] = weight
        self.adjMatrix[v2][v1] = weight

    # Remove edges
    # O(n) = O(1)
    def remove_edge(self, v1, v2):
        if self.adjMatrix[v1][v2] == 0:
            return
        self.adjMatrix[v1][v2] = -1
        self.adjMatrix[v2][v1] = -1

    # Get Distance
    # O(n) = O(1)
    def get_distance(self, v1, v2):
        return self.adjMatrix[v1][v2]

    # O(n) = O(1)
    def __len__(self):
        return self.size

    # Print the matrix
    # O(n) = O(n*n)
    def print_matrix(self):
        for row in self.adjMatrix:
            for val in row:
                print('{:4}'.format(val)),
            print
