from graph import Graph
import random
from visualize import graphVisualizer

graph = Graph()

# graph.addNewNode("0", [], [])
# graph.addNewNode("1", [], [])
# graph.addNewNode("2", [], [])

# graph.saveToFile("fiveNodes.json")
graph.readFromFile("fiveNodes.json")

# print(graph.nodesArray[0])

print(graph.findShortestPath(0, 5))
# path, weight, distance = graph.findDijkstraShortestPath(0, 5)
# print(f"Кратчайший путь: {path}, Вес: {distance}")

# paths = graph.dfs(0,5)

# print(paths)
# min((word for word in paths if word), key=len)

# graphVisualizer(graph.nodesArray)
