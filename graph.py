import json


class Graph:
    graphName = ""
    nodesArray = []

    def __init__(self):
        self.graphName = "test"
        self.nodesArray = []

    # Tools

    def addNewNode(self, name, data, edges):
        newNode = [
            name,
            data,
            edges
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

    def info(self, value):
        if type(value) is int:
            if self.nodesArray[value]:
                print("Info about node: " + str(value))
                print("Node name: " + str(self.nodesArray[value][0]))
                print("Number of edges: " + str(len(self.nodesArray[value][2])))
                print("Number of data values: " + str(len(self.nodesArray[value][1])))
            else: print("Node is not exist")
        elif type(value) is str:
            nodeId = -1
            for index, node in enumerate(self.nodesArray):
                if value in node[0]:
                    nodeId = index
                    break
                if index + 1 == len(self.nodesArray):
                    print("Node is not exist")
                    break

            print("Info about node: " + str(nodeId))
            print("Node id: " + str(nodeId))
            print("Number of edges: " + str(len(self.nodesArray[nodeId][2])))
            print("Number of data values: " + str(len(self.nodesArray[nodeId][1])))

        elif type(value) is list:
            print("Info about edge: " + str(value))

            weight = 0
            for item in self.nodesArray[value[0]][2]:
                if item[0] == value[1]: weight = item[1][0]

            print("Name of start node: " + str(self.nodesArray[value[0]][0]))
            print("Name of destination node: " + str(self.nodesArray[value[1]][0]))
            print("Edge weight: " + str(weight))
            print("Number of data values: " + str(len(self.nodesArray[value[0]][2])-1))
        else:
            print("Info about graph: " + self.graphName)

            numberOfEdges = 0
            isComplite = True
            edges = []
            for index, node in enumerate(self.nodesArray):
                for pointer in node[2]:
                    if pointer:
                        edge = [index, pointer[0]]
                        if edge not in edges and edge.reverse() not in edges:
                            edges.append(edge)
                    numberOfEdges += 1

                if len(node[2]) < 3: isComplite = False

            print("Number of nodes: " + str(len(self.nodesArray)))
            print("Number of edges: " + str(numberOfEdges))
            print("Number of unique edges: " + str(len(edges)))
            print("Is graph complete: " + str(isComplite))


# --------------------------------------------------------Analysis-------------------------------------------------------

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

            # Search goal node
            if endNode == next_node[0]:
                current_path.append(endNode)
                path_weight_list.append(next_node[1][0])

                return current_path, path_weight_list, sum(path_weight_list)

            if not next_node[0] in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node[0])
                path_list.append(new_path)
                path_weight_list.append(next_node[1][0])
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


# Find all cycles in graph
def findCycles(self):
    nodes = []
    cycles = []
    for index, node in enumerate(self.nodesArray):
        edges = []
        for edge in node[2]:
            if edge:
                edges.append(edge[0])
        nodes.append(edges)
    nodes.append([])

    cycles = []

    def dfs(v, visited, path):
        visited[v] = True
        path.append(v)

        for neighbor in nodes[v]:
            if neighbor not in path:
                if not visited[neighbor]:
                    dfs(neighbor, visited, path)
            else:
                cycle = path[path.index(neighbor):]

                if cycle not in cycles and len(cycle) >= 3:
                    cycle.append(neighbor)
                    cycles.append(cycle)

        path.pop()
        visited[v] = False

    n = len(nodes)
    visited = [False] * n

    for i in range(n):
        dfs(i, visited, [])

    print(len(cycles))
    return cycles


# Find the smallest weight path
def findDijkstraShortestPath(self, start, end):
    nodes = []
    edges = []
    for index, node in enumerate(self.nodesArray):
        nodes.append(index)
        for edge in node[2]:
            if edge:
                edges.append([index, edge[0], edge[1][0]])

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
