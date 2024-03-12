from graphDB.graph import Graph
from visualize import graphVisualizer
from time import perf_counter_ns
import profile

graph = Graph()

# graph.addNewNode("0", [], [])
# graph.addNewNode("1", [], [])
# graph.addNewNode("2", [], [])

# graph.saveToFile("fiveNodes.json")

# graph.readFromFile("fiveNodes.json")
graph.readFromFile("dataNodes.json")
# graph.readFromFile("threeNodes.json")

# print(graph.nodesArray)

start = perf_counter_ns()

# print(graph.findShortestPath(0, 5))
# path, weight, distance = graph.findDijkstraShortestPath(0, 2)
# print(f"Кратчайший путь: {path}, Вес: {distance}")

# print(graph.dfs(0,5))
# min((word for word in paths if word), key=len)
# cycles = graph.findCycles()
# for i in cycles:
#     print(i)

# graph.info(1)
graph.getData(1, "productId", 0)

print("ms: "+ str((perf_counter_ns() - start)/1000))

graphVisualizer(graph.nodesArray)
