import uuid

from graphDB.graph import Graph, Node, Edge
from visualize import graphVisualizer
from time import perf_counter_ns
import profile

graph = Graph("test")

nodeA = graph.addNode(Node(id=uuid.uuid4(), name="1"))
nodeB = graph.addNode(Node(id=uuid.uuid4(), name="2"))
nodeC = graph.addNode(Node(id=uuid.uuid4(), name="3"))
nodeD = graph.addNode(Node(id=uuid.uuid4(), name="4"))
nodeE = graph.addNode(Node(id=uuid.uuid4(), name="5"))
edgeA = graph.addEdge(Edge(id=uuid.uuid4(), fromNode=nodeA, toNode=nodeB, name="AtoB", weight=1))
edgeB = graph.addEdge(Edge(id=uuid.uuid4(), fromNode=nodeB, toNode=nodeC, name="BtoC", weight=1))
edgeC = graph.addEdge(Edge(id=uuid.uuid4(), fromNode=nodeC, toNode=nodeD, name="CtoD", weight=1))
edgeD = graph.addEdge(Edge(id=uuid.uuid4(), fromNode=nodeD, toNode=nodeE, name="DtoE", weight=1))


# graph.save_to_file("big.db")

# graph = graph.read_from_file("test.txt")
# graph.readFromFile("dataNodes.json")
# graph.readFromFile("threeNodes.json")

# print(graph.nodesArray)

# start = perf_counter_ns()

# print(graph.findShortestPath(nodeA,nodeC))
# path, weight, distance = graph.findDijkstraShortestPath(nodeA,nodeC)
# print(f"Кратчайший путь: {path}, Вес: {distance}")

# print(graph.dfs(nodeA,nodeC))
# min((word for word in paths if word), key=len)
# cycles = graph.findCycles()
# for i in cycles:
#     print(i)

graph.print_info(edgeJ)
# graph.getData(1, "productId", 0)

# print("ms: "+ str((perf_counter_ns() - start)/1000))

graphVisualizer(graph)

#TODO: проверить отрисовку графа, иногда не рисует стрелки (big.db)
