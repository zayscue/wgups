# Zackery Ayscue 000901676

# minimum distance value, from the set of vertices
# not yet included in shortest path tree
def min_distance(v, dist, visited):

    # Initilaize minimum distance for next node
    min = float('inf')

    # Search not nearest vertex not in the
    # shortest path tree
    for v in range(v):
        if dist[v] < min and visited[v] == False:
            min = dist[v]
            min_index = v

    return min_index

# Class to represent a complete graph


class CompleteGraph:

    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    # Add edges
    def add_edge(self, u, v, w):
        self.graph[u][v] = w
        self.graph[v][u] = w

    # Remove edges
    def remove_edge(self, v1, v2):
        if self.graph[v1][v2] == 0:
            return
        self.graph[v1][v2] = -1
        self.graph[v2][v1] = -1

    # Get Distance
    def get_distance(self, v1, v2):
        return self.graph[v1][v2]

    # Finds shortest paths from the source to all other nodes in the graph
    def dijkstra(self, src):
        dist = [float('inf')] * self.V

        dist[src] = 0
        visited = [False] * self.V

        for cout in range(self.V):

            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = min_distance(self.V, dist, visited)

            # Put the minimum distance vertex in the
            # shotest path tree
            visited[u] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shotest path tree
            for v in range(self.V):
                if self.graph[u][v] > 0 and visited[v] == False and dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = round(dist[u] + self.graph[u][v], 1)

        return dist

    # Because the is complete graph we can run
    # a optimization algothrim that loops through
    # every node can caculates the shortest path
    # for to every other node
    def optimize(self):
        optimal_distances = []
        for i in range(0, len(self.graph)):
            dist = self.dijkstra(i)
            optimal_distances.append(dist)
        return optimal_distances
