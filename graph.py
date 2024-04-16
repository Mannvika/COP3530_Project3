class Graph:
    def __init__(self, g, v):
        # Graph constructor, takes in matrix and number of vertices
        self.graph = g
        self.num_of_vertices = v

    def find_neighbors(self, vertex):
        # Helper function to find all neighbors to a given vertex
        neighbors = []
        # Loops through each neighbor vertex and adds if an edge exists (1000 means no edge)
        for i in range(len(self.graph[vertex])):
            if self.graph[vertex][i] != 1000:
                neighbors.append(i)
        return neighbors

    def dijkstras(self, subset_amount, song_amount, src_index):
        # Function to find the closest vertices (representing the most similar songs)

        distances = [1e7] * subset_amount # Array storing distances between source and index vertex
        previous = [0] * subset_amount  # Array storing the previous vertex in the path between source and index vertex

        # Set the distance of the source vertex (from the source vertex) to 0
        distances[src_index] = 0

        # Create a queue that contains all the vertex
        queue = list(range(subset_amount))

        # Create an array of the selected vertices
        selected_vertices = []

        # Start a counter to check when we have reached our song amount
        counter = 0

        # While we still have vertices in the queue and have not reached are song limit
        while queue and counter < song_amount:

            # Find the vertex with the least distance to the source vertex
            min_dist = queue[0]
            for vertex in queue:
                if distances[vertex] < distances[min_dist]:
                    min_dist = vertex

            # Remove it from the queue, find its neighbors and relax it
            queue.remove(min_dist)
            neighbors = self.find_neighbors(min_dist)
            for neighbor in neighbors:
                if neighbor in queue:
                    if distances[min_dist] + self.graph[min_dist][neighbor] < distances[neighbor]:
                        distances[neighbor] = distances[min_dist] + self.graph[min_dist][neighbor]
                        previous[neighbor] = min_dist

            # Add it to the list
            if distances[min_dist] != 1e7:
                selected_vertices.append(min_dist)

            # Increment counter
            counter += 1

        # Return array of selected vertices
        return selected_vertices





