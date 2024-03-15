import uuid

from graph import Graph, Node, Edge
from visualize import GraphPlot
from time import perf_counter_ns
import profile

graph = Graph("test")

nodeA = graph.addNode(Node(name="1", data={'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}))
nodeB = graph.addNode(Node(name="2"))
nodeC = graph.addNode(Node(name="3"))
nodeD = graph.addNode(Node(name="4"))
nodeE = graph.addNode(Node(name="5"))
edgeA = graph.addEdge(Edge(fromNode=nodeA, toNode=nodeB, name="AtoB", weight=1))
edgeB = graph.addEdge(Edge(fromNode=nodeB, toNode=nodeC, name="BtoC", weight=1))
edgeC = graph.addEdge(Edge(fromNode=nodeC, toNode=nodeD, name="CtoD", weight=1))
edgeD = graph.addEdge(Edge(fromNode=nodeD, toNode=nodeE, name="DtoE", weight=1))

# graph.save_to_file("big.db")

# graph = graph.read_from_file("big.db")
# graph.readFromFile("dataNodes.json")
# graph.readFromFile("threeNodes.json")

start = perf_counter_ns()

# print(graph.findShortestPath(nodeA, nodeC))
# path, weight, distance = graph.findDijkstraShortestPath(nodeA, nodeC)
# print(f"Кратчайший путь: {path}, Вес: {distance}")

# graph.dfs(nodeA, nodeC)
# min((word for word in paths if word), key=len)
# cycles = graph.findCycles()
# for i in cycles:
#     print(i)

# print(graph.findNodeByName("1").data)
# print(graph.edges)
# transaction = GraphTransaction(graph)
# graphVisualizer(graph)
# transaction.start

# print(nodeA.findKey("key1"))


# graph.print_info()
# graph.getData(1, "productId", 0)

print("ms: "+ str((perf_counter_ns() - start)/1000))

plot = GraphPlot(graph=graph)
plot.draw()

#TODO: проверить отрисовку графа, иногда не рисует стрелки (big.db)
