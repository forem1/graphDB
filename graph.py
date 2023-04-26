import json


class Graph:
    nodesArray = []

    def __init__(self):
        self.nodesArray = []

    def addNewNode(self, name, data, edges):
        newNode = [
            name,
            data,
            [0, edges]
        ]

        self.nodesArray.append(newNode)

    def saveToFile(self, path):
        with open(path, 'w') as file:
            # print(json.dumps(self.nodesArray))
            file.write(json.dumps(self.nodesArray))
            file.close()

    def readFromFile(self, path):
        with open(path) as f:
            self.nodesArray = json.load(f)

    # Find the smallest edges path
    def findShortestPath(self, startNode, endNode):
        path_list = [[startNode]]
        path_weight_list = []
        path_index = 0
        # To keep track of previously visited nodes
        previous_nodes = [startNode]

        if startNode == endNode:
            return path_list[0]

        while path_index < len(path_list):
            current_path = path_list[path_index]
            last_node = current_path[-1]
            next_nodes = self.nodesArray[last_node][2]

            # Add new paths
            for next_node in next_nodes:

                direction_flag = False
                # Get true node edges in graph
                for absolute_node in self.nodesArray[next_node[0]][2]:
                    # If cross path, skip the way
                    if last_node == absolute_node[0] and absolute_node[1]:
                        direction_flag = True

                # Search goal node
                # if next node is final and direction not to current node or from current to next
                if endNode == next_node[0] and (not direction_flag or next_node[1]):
                    current_path.append(endNode)
                    path_weight_list.append(next_node[2][0])

                    return current_path, path_weight_list, sum(path_weight_list)

                if not next_node[0] in previous_nodes and (not direction_flag or next_node[1]):
                    new_path = current_path[:]
                    new_path.append(next_node[0])
                    path_list.append(new_path)
                    path_weight_list.append(next_node[2][0])
                    # To avoid backtracking
                    previous_nodes.append(next_node[0])
            # Continue to next path in list
            path_index += 1
        # No path is found
        return []

    # Depth-first search
    def dfs(self, start, end, path=[]):
        path = path + [start]

        if start == end:
            return [path]

        paths = []
        for edge in self.nodesArray[start][2]:

            if edge[0] not in path:
                new_paths = self.dfs(edge[0], end, path)
                for p in new_paths:
                    paths.append(p)
        return paths

    # Find the smallest weight path
    def findDijkstraShortestPath(self, start, end):

        nodes = []
        edges = []
        for index, node in enumerate(self.nodesArray):
            nodes.append(index)
            for edge in node[2]:
                edges.append([index, edge[0], edge[2][0]])

        # Create a list to hold the distances between nodes
        distances = [float('inf')] * len(nodes)
        # Set the distance of the starting vertex to 0
        distances[start] = 0

        # Traverse the graph
        for i in range(len(nodes) - 1):
            for j in range(len(edges)):
                # Extract the source, destination, and weight of the edge
                src, dest, weight = edges[j]
                # Update the distance if a shorter path is found
                if distances[src] + weight < distances[dest]:
                    distances[dest] = distances[src] + weight

        # Check if there is a negative cycle
        for i in range(len(edges)):
            src, dest, weight = edges[i]
            if distances[src] + weight < distances[dest]:
                raise ValueError("Negative cycle detected")

        # Return the shortest path from the start to the end vertex
        path = [end]
        weights = []
        while path[-1] != start:
            for i in range(len(edges)):
                src, dest, weight = edges[i]
                if dest == path[-1] and distances[src] + weight == distances[path[-1]]:
                    path.append(src)
                    weights.append(weight)
                    break
        return list(reversed(path)), weights, sum(weights)
