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

# print(graph.findShortestPath(0, 2))
# path, weight, distance = graph.findDijkstraShortestPath(0, 2)
# print(f"Кратчайший путь: {path}, Вес: {distance}")

# print(graph.dfs(0,5))
# min((word for word in paths if word), key=len)
# cycles = graph.findCycles()
# for i in cycles:
#     print(i)

graph.info([0,1])

# graphVisualizer(graph.nodesArray)
