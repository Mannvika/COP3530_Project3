class Graph():
    def __init__(self, g, v):
        self.graph = g
        self.num_of_vertices = v

    def find_neighbors(self, vertex):
        neighbors = []
        for i in range(len(self.graph[vertex])):
            if self.graph[vertex][i] != 1000:
                neighbors.append(i)
        return neighbors

    def dijkstras(self, subset_amount, song_amount, src_index):
        distances = [1e7] * subset_amount
        previous = [0] * subset_amount
        distances[src_index] = 0

        queue = list(range(subset_amount))
        selected_vertices = []

        counter = 0
        while queue and counter < song_amount:
            min_dist = queue[0]
            for vertex in queue:
                if distances[vertex] < distances[min_dist]:
                    min_dist = vertex

            queue.remove(min_dist)
            neighbors = self.find_neighbors(min_dist)
            for neighbor in neighbors:
                if neighbor in queue:
                    if distances[min_dist] + self.graph[min_dist][neighbor] < distances[neighbor]:
                        distances[neighbor] = distances[min_dist] + self.graph[min_dist][neighbor]
                        previous[neighbor] = min_dist

            if distances[min_dist] != 1e7:
                selected_vertices.append(min_dist)

            counter += 1

        return selected_vertices





