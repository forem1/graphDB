import copy
import pickle
from collections import Counter
from dataclasses import dataclass, field
from uuid import uuid4, UUID
from typing import Union, List


@dataclass
class Node:
    name: str
    id: UUID = field(default_factory=uuid4)
    link: str = ""  # сейчас строка, но может быть указатель
    data: Union[dict, any] = field(default_factory=dict)

    def findKey(self, key: str):
        if type(self.data) is dict:
            if key in self.data:
                return self.data.get(key)
        return None

    def findValue(self, value: str):
        if type(self.data) is dict:
            key = {i for i in self.data if self.data[i] == value}
            if key != set():
                return key
        return None


@dataclass
class Edge:
    fromNode: Union[UUID, Node]
    toNode: Union[UUID, Node]
    name: str
    id: UUID = field(default_factory=uuid4)
    data: dict = field(default_factory=dict)
    weight: int = 0
    directed: bool = True

    def __post_init__(self):
        if isinstance(self.toNode, Node):
            self.toNode = self.toNode.id
        if isinstance(self.fromNode, Node):
            self.fromNode = self.fromNode.id

    def findKey(self, key: str):
        if type(self.data) is dict:
            if key in self.data:
                return self.data.get(key)
        return None

    def findValue(self, value: str):
        if type(self.data) is dict:
            key = {i for i in self.data if self.data[i] == value}
            if key != set():
                return key
        return None


class Graph:
    def __init__(self, name):
        self.name = name
        self.edges = []
        self.nodes = []

    def save_to_file(self, path):
        with open(path, "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def read_from_file(cls, path):
        with open(path, "rb") as file:
            return pickle.load(file)

    def print_info(self, value=True):
        if type(value) is UUID:
            for node in self.nodes:
                if node.id == value:
                    print(f"Info about node: {node.name}")
                    print(f"Node id: {str(node.id)}")
                    print(
                        f"Number of incoming edges: {str(sum(1 for edge in self.edges if edge.toNode == value))}"
                    )
                    print(
                        f"Number of outgoing edges: {str(sum(1 for edge in self.edges if edge.fromNode == value))}"
                    )
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
                    print(
                        f"Number of incoming edges: {str(sum(1 for edge in self.edges if edge.toNode == value))}"
                    )
                    print(
                        f"Number of outgoing edges: {str(sum(1 for edge in self.edges if edge.fromNode == value))}"
                    )
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

            # Создаем множество всех возможных рёбер
            all_edges = {(edge.fromNode, edge.toNode) for edge in self.edges}
            all_edges.update({(edge.toNode, edge.fromNode) for edge in self.edges})

            # Считаем количество уникальных рёбер с помощью Counter
            edge_counter = Counter((edge.fromNode, edge.toNode) for edge in self.edges)

            print(f"Number of nodes: {str(len(self.nodes))}")
            print(f"Number of edges: {str(len(self.edges))}")
            print(f"Number of unique edges: {str(len(edge_counter))}")
            # Проверяем, является ли количество рёбер в графе равным количеству возможных рёбер для полного графа
            print(
                f"Is graph complete: {str(len(all_edges) == len(self.nodes) * (len(self.nodes) - 1))}"
            )

    # ----------------------------------------------------------CRUD---------------------------------------------------------

    def addNode(self, node: Node):
        if len(self.nodes) != 0:
            for currNode in self.nodes:
                if currNode.name != node.name:
                    self.nodes.append(node)
                    return node
                else:
                    raise Exception("Node name is exist")
        else:
            self.nodes.append(node)
            return node

    def addEdge(self, edge: Edge):
        if len(self.edges) != 0:
            for currEdge in self.edges:
                if currEdge.name != edge.name:
                    self.edges.append(edge)
                    return edge
                else:
                    raise Exception("Edge name is exist")
        else:
            self.edges.append(edge)
            return edge

    def updateNode(self, currNode: Node, newNode: Node) -> bool:
        for i, node in enumerate(self.nodes):
            if node == currNode:
                self.nodes[i] = newNode
                return True
        return False

    def updateEdge(self, currEdge: Edge, newEdge: Edge) -> bool:
        for i, edge in enumerate(self.edges):
            if edge == currEdge:
                self.edges[i] = newEdge
                return True
        return False

    def deleteNode(self, node: Node) -> bool:
        if not any(
            edge.fromNode == node.id or edge.toNode == node.id for edge in self.edges
        ):
            self.nodes.remove(node)
            return True
        else:
            raise Exception("Node have a edges")

    def deleteEdge(self, edge: Edge) -> bool:
        self.edges.remove(edge)
        return True

    def deleteAllEdges(self, node: Node) -> bool:
        self.edges = [
            edge
            for edge in self.edges
            if edge.toNode != node.id and edge.fromNode != node.id
        ]
        return True

    def findNodeById(self, id: str) -> Node:
        for node in self.nodes:
            if node.id == id:
                return node
        return None

    def findNodeByName(self, name: str) -> Node:
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def findKeyInNodes(self, key: str) -> List:
        values = []
        for node in self.nodes:
            if type(node.data) is dict:
                if key in node.data:
                    values.append([node.id, node.name, node.data.get(key)])
        return values

    def findValueInNodes(self, value: str) -> List:
        keys = []
        for node in self.nodes:
            if type(node.data) is dict:
                key = {i for i in node.data if node.data[i] == value}
                if key != set():
                    keys.append([node.id, node.name, key])
        return keys

    # --------------------------------------------------------Analysis-------------------------------------------------------
    # Find the smallest edges path
    def findShortestPath(
        self,
        startNode: Union[Node, UUID],
        endNode: Union[Node, UUID],
        visited=None,
        path=None,
    ):
        startNode = startNode.id if type(startNode) == Node else startNode
        endNode = endNode.id if type(endNode) == Node else endNode

        if visited is None:
            visited = set()
        if path is None:
            path = [startNode]

        if startNode == endNode:
            return path

        shortest_path = None
        shortest_path_length = float("inf")

        for edge in self.edges:
            if edge.fromNode == startNode and edge.toNode not in visited:
                new_path = path + [edge.toNode]
                new_visited = visited.copy()
                new_visited.add(edge.toNode)
                found_path = self.findShortestPath(
                    edge.toNode, endNode, new_visited, new_path
                )
                if found_path and len(found_path) < shortest_path_length:
                    shortest_path = found_path
                    shortest_path_length = len(found_path)

            elif (
                not edge.directed
                and edge.toNode == startNode
                and edge.fromNode not in visited
            ):
                new_path = path + [edge.fromNode]
                new_visited = visited.copy()
                new_visited.add(edge.fromNode)
                found_path = self.findShortestPath(
                    edge.fromNode, endNode, new_visited, new_path
                )
                if found_path and len(found_path) < shortest_path_length:
                    shortest_path = found_path
                    shortest_path_length = len(found_path)

        return shortest_path if shortest_path else []

    # Depth-first search
    def dfs(self, start: Union[Node, UUID], end: Union[Node, UUID], path=None):
        start = start.id if type(start) == Node else start
        end = end.id if type(end) == Node else end

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
            elif (
                not edge.directed and edge.toNode == start and edge.fromNode not in path
            ):
                new_paths = self.dfs(edge.fromNode, end, path + [edge.fromNode])
                for p in new_paths:
                    paths.append(p)
        return paths

    # Find all cycles in graph
    def findCycles(self):
        # Создаем список всех узлов графа
        nodes = set()
        for edge in self.edges:
            nodes.add(edge.fromNode)
            nodes.add(edge.toNode)

        cycles = []

        def dfs(v, visited, path):
            visited[v] = True
            path.append(v)

            # Получаем список смежных узлов из рёбер
            adjacent_nodes = set()
            for edge in self.edges:
                if edge.fromNode == v:
                    adjacent_nodes.add(edge.toNode)
                elif edge.toNode == v and not edge.directed:
                    adjacent_nodes.add(edge.fromNode)

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

        return cycles

    # Find the smallest weight path
    def findDijkstraShortestPath(
        self, start: Union[Node, UUID], end: Union[Node, UUID]
    ):
        start = start.id if type(start) == Node else start
        end = end.id if type(end) == Node else end

        node_indices = {node.id: index for index, node in enumerate(self.nodes)}
        distances = {node_id: float("inf") for node_id in node_indices}
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
                if (
                    not edge.directed
                    and src == path[-1]
                    and distances[dest] + weight == distances[path[-1]]
                ):
                    path.append(dest)
                    weights.append(weight)
                    break
        return list(reversed(path)), weights, sum(weights)
