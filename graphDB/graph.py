import pickle
from collections import Counter
from dataclasses import dataclass, field
import json
from uuid import uuid4, UUID
from typing import List, Union

@dataclass
class Edge:
    id:UUID
    fromNode:UUID
    toNode:UUID
    name:str
    data:dict = field(default_factory=dict)
    weight: int = 0
    directed:bool = True

@dataclass
class Node:
    id: UUID
    name:str
    link:str = "" #сейчас строка, но может быть указатель
    data: Union[dict, any] = field(default_factory=dict)


class Graph:
    def __init__(self, name):
        self.name = name
        self.edges = []
        self.nodes = []

    def addNode(self, node: Node):
        self.nodes.append(node)
        return node.id
    def addEdge(self, edge: Edge):
        self.edges.append(edge)
        return edge.id

    def save_to_file(self, path):
        with open(path, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def read_from_file(cls, path):
        with open(path, 'rb') as file:
            return pickle.load(file)

    def print_info(self, value=True):
        if type(value) is UUID:
            for node in self.nodes:
                if node.id == value:
                    print(f"Info about node: {node.name}")
                    print(f"Node id: {str(node.id)}")
                    print(f"Number of incoming edges: {str(sum(1 for edge in self.edges if edge.toNode == value))}")
                    print(f"Number of outgoing edges: {str(sum(1 for edge in self.edges if edge.fromNode == value))}")
                    if type(node.data) is dict:
                        print(f"Number of data values: {str(len(node.data))}")
                    return True

            for edge in self.edges:
                if edge.id == value:
                    print(f"Info about edge: {edge.name}")
                    print(f"Name of outgoing node: {edge.fromNode}")
                    print(f"Name of incoming node: {edge.toNode}")
                    print(f"Edge weight: {edge.weight}")
                    print(f"Is edge directed: {edge.directed}")
                    print(f"Number of data values: {str(len(edge.data))}")
                    return True
            print("Id is not exist")
        elif type(value) is str:
            for node in self.nodes:
                if node.name == value:
                    print(f"Info about node: {node.name}")
                    print(f"Node id: {str(node.id)}")
                    print(f"Number of incoming edges: {str(sum(1 for edge in self.edges if edge.toNode == value))}")
                    print(f"Number of outgoing edges: {str(sum(1 for edge in self.edges if edge.fromNode == value))}")
                    if type(node.data) is dict:
                        print(f"Number of data values: {str(len(node.data))}")
                    return True

            for edge in self.edges:
                if edge.name == value:
                    print(f"Info about edge: {edge.name}")
                    print(f"Name of outgoing node: {edge.fromNode}")
                    print(f"Name of incoming node: {edge.toNode}")
                    print(f"Edge weight: {edge.weight}")
                    print(f"Is edge directed: {edge.directed}")
                    print(f"Number of data values: {str(len(edge.data))}")
                    return True
            print("Name is not exist")
        else:
            print(f"Info about graph: {self.name}")

            #Создаем множество всех возможных рёбер
            all_edges = {(edge.fromNode, edge.toNode) for edge in self.edges}
            all_edges.update({(edge.toNode, edge.fromNode) for edge in self.edges})

            # Считаем количество уникальных рёбер с помощью Counter
            edge_counter = Counter((edge.fromNode, edge.toNode) for edge in self.edges)

            print(f"Number of nodes: {str(len(self.nodes))}")
            print(f"Number of edges: {str(len(self.edges))}")
            print(f"Number of unique edges: {str(len(edge_counter))}")
            # Проверяем, является ли количество рёбер в графе равным количеству возможных рёбер для полного графа
            print(f"Is graph complete: {str(len(all_edges) == len(self.nodes) * (len(self.nodes) - 1))}")


    # --------------------------------------------------------Analysis-------------------------------------------------------
    # Find the smallest edges path
    #FIXME: не работает с неопределенными гранями
    def findShortestPath(self, startNode, endNode, visited=None, path=None):
        if visited is None:
            visited = set()
        if path is None:
            path = [startNode]

        if startNode == endNode:
            return path

        shortest_path = None
        shortest_path_length = float('inf')

        for edge in self.edges:
            if edge.fromNode == startNode and edge.toNode not in visited:
                new_path = path + [edge.toNode]
                new_visited = visited.copy()
                new_visited.add(edge.toNode)
                found_path = self.findShortestPath(edge.toNode, endNode, new_visited, new_path)
                if found_path and len(found_path) < shortest_path_length:
                    shortest_path = found_path
                    shortest_path_length = len(found_path)

            elif not edge.directed and edge.toNode == startNode and edge.fromNode not in visited:
                new_path = path + [edge.fromNode]
                new_visited = visited.copy()
                new_visited.add(edge.fromNode)
                found_path = self.findShortestPath(edge.fromNode, endNode, new_visited, new_path)
                if found_path and len(found_path) < shortest_path_length:
                    shortest_path = found_path
                    shortest_path_length = len(found_path)

        return shortest_path if shortest_path else []

    # Depth-first search
    def dfs(self, start, end, path=None):
        if path is None:
            path = [start]

        if start == end:
            return [path]

        paths = []
        for edge in self.edges:
            if edge.fromNode == start and edge.toNode not in path:
                new_paths = self.dfs(edge.toNode, end, path + [edge.toNode])
                for p in new_paths:
                    paths.append(p)
            elif not edge.directed and edge.toNode == start and edge.fromNode not in path:
                new_paths = self.dfs(edge.fromNode, end, path + [edge.fromNode])
                for p in new_paths:
                    paths.append(p)
        return paths

    # Find all cycles in graph
    def findCycles(self):
        # Создаем список узлов, из которых исходят рёбра
        nodes = [edge.fromNode for edge in self.edges]
        cycles = []

        def dfs(v, visited, path):
            visited[v] = True
            path.append(v)

            # Получаем список смежных узлов из рёбер
            adjacent_nodes = [edge.toNode for edge in self.edges if edge.fromNode == v]

            for neighbor in adjacent_nodes:
                if neighbor not in path:
                    if not visited.get(neighbor, False):
                        dfs(neighbor, visited, path)
                else:
                    # Находим цикл
                    cycle = path[path.index(neighbor):]

                    if cycle not in cycles and len(cycle) >= 3:
                        cycle.append(neighbor)
                        cycles.append(cycle)

            path.pop()
            visited[v] = False

        visited = {}

        # Запускаем поиск в глубину из каждого узла
        for node in nodes:
            dfs(node, visited, [])

        print(len(cycles))
        return cycles

    # Find the smallest weight path
    def findDijkstraShortestPath(self, start, end):
        node_indices = {node.id: index for index, node in enumerate(self.nodes)}
        distances = {node_id: float('inf') for node_id in node_indices}
        distances[start] = 0

        for i in range(len(self.nodes) - 1):
            for edge in self.edges:
                src, dest, weight = edge.fromNode, edge.toNode, edge.weight
                if distances[src] + weight < distances[dest]:
                    distances[dest] = distances[src] + weight
                if not edge.directed and distances[dest] + weight < distances[src]:
                    distances[src] = distances[dest] + weight

        for edge in self.edges:
            src, dest, weight = edge.fromNode, edge.toNode, edge.weight
            if distances[src] + weight < distances[dest]:
                raise ValueError("Negative cycle detected")
            if not edge.directed and distances[dest] + weight < distances[src]:
                raise ValueError("Negative cycle detected")

        path = [end]
        weights = []
        while path[-1] != start:
            for edge in self.edges:
                src, dest, weight = edge.fromNode, edge.toNode, edge.weight
                if dest == path[-1] and distances[src] + weight == distances[path[-1]]:
                    path.append(src)
                    weights.append(weight)
                    break
                if not edge.directed and src == path[-1] and distances[dest] + weight == distances[path[-1]]:
                    path.append(dest)
                    weights.append(weight)
                    break
        return list(reversed(path)), weights, sum(weights)