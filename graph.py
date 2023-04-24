class Graph:
    nodesArray = []

    def __init__(self):
        self.nodesArray = []

    def addNewNode(self, name, data, edges):
        newNode = [
            name,
            data,
            edges
        ]

        self.nodesArray.append(newNode)

    def findShortestPath(self, startNode, endNode, weightsOutput=False, weightsSumOutput=False):
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
                # if next node if final and direction not to current node or from current to next
                if endNode == next_node[0] and (not direction_flag or next_node[1]):
                    current_path.append(endNode)
                    path_weight_list.append(next_node[2][0])

                    if weightsSumOutput:
                        return sum(path_weight_list)
                    elif weightsOutput:
                        return path_weight_list
                    else:
                        return current_path

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
