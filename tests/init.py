from graph import Graph, Node, Edge
from visualize import graphVisualizer
from time import perf_counter_ns

graph = Graph("test")

# nodeA = graph.addNode(Node(name="1", data={'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}))
# nodeB = graph.addNode(Node(name="2"))
# nodeC = graph.addNode(Node(name="3"))
# nodeD = graph.addNode(Node(name="4"))
# edgeA = graph.addEdge(Edge(fromNode=nodeA, toNode=nodeB, name="AtoB", weight=1))
# edgeB = graph.addEdge(Edge(fromNode=nodeB, toNode=nodeC, name="BtoC", weight=1))
# edgeC = graph.addEdge(Edge(fromNode=nodeC, toNode=nodeD, name="CtoD", weight=1))
# edgeD = graph.addEdge(Edge(fromNode=nodeD, toNode=nodeA, name="DtoA", weight=1))
# edgeE = graph.addEdge(Edge(fromNode=nodeB, toNode=nodeD, name="BtoD", weight=1, directed=False))

nodeA = graph.addNode(Node(name="A"))
nodeB = graph.addNode(Node(name="B"))
nodeC = graph.addNode(Node(name="C"))
nodeD = graph.addNode(Node(name="D"))
nodeE = graph.addNode(Node(name="E"))
nodeF = graph.addNode(Node(name="F"))
nodeG = graph.addNode(Node(name="G"))
nodeH = graph.addNode(Node(name="H"))
nodeI = graph.addNode(Node(name="I"))
nodeJ = graph.addNode(Node(name="J"))
edgeA = graph.addEdge(Edge(fromNode=nodeA, toNode=nodeB, name="AtoB", weight=1))
edgeB = graph.addEdge(Edge(fromNode=nodeB, toNode=nodeC, name="BtoC", weight=1))
edgeC = graph.addEdge(Edge(fromNode=nodeC, toNode=nodeD, name="CtoD", weight=1))
edgeD = graph.addEdge(Edge(fromNode=nodeD, toNode=nodeE, name="DtoE", weight=1))
edgeE = graph.addEdge(Edge(fromNode=nodeE, toNode=nodeF, name="EtoF", weight=1))
edgeF = graph.addEdge(Edge(fromNode=nodeF, toNode=nodeG, name="FtoG", weight=1))
edgeG = graph.addEdge(Edge(fromNode=nodeG, toNode=nodeH, name="GtoH", weight=1))
edgeH = graph.addEdge(Edge(fromNode=nodeH, toNode=nodeA, name="HtoA", weight=1))
edgeI = graph.addEdge(Edge(fromNode=nodeC, toNode=nodeF, name="CtoF", weight=1))
edgeJ = graph.addEdge(Edge(fromNode=nodeF, toNode=nodeB, name="FtoB", weight=3))
edgeK = graph.addEdge(Edge(fromNode=nodeH, toNode=nodeI, name="HtoI", weight=1))
edgeL = graph.addEdge(
    Edge(fromNode=nodeH, toNode=nodeB, name="HtoB", weight=5, directed=False)
)

# for i in range(100):
#     graph.addNode(Node(name=i, data={"key1": "val1"}))
#     if i > 0:
#         graph.addEdge(
#             Edge(
#                 fromNode=graph.nodes[-2],
#                 toNode=graph.nodes[-1],
#                 name=f"edge-{i}",
#                 weight=1,
#             )
#         )

# graph.save_to_file("big.db")

# graph = graph.read_from_file("big.db")
# graph.readFromFile("dataNodes.json")
# graph.readFromFile("threeNodes.json")

start = perf_counter_ns()

# print(graph.findShortestPath(nodeA, nodeI))
# path, weight, distance = graph.findDijkstraShortestPath(nodeA, nodeI)
# print(f"Кратчайший путь: {path}, Вес: {distance}")

# print(len(graph.dfs(nodeA, nodeI)))
# cycles = graph.findCycles()
# for i in cycles:
#     temp = []
#     for j in i:
#         temp.append(graph.findNodeById(j).name)
#     print(temp)

# print(graph.findNodeByName("1").data)
# print(graph.edges)
# transaction = GraphTransaction(graph)
# graphVisualizer(graph)
# transaction.start

# print(nodeA.findKey("key1"))


# graph.print_info()
# graph.getData(1, "productId", 0)

print("ms: " + str((perf_counter_ns() - start) / 1000))

graphVisualizer(graph)

# TODO: проверить отрисовку графа, иногда не рисует стрелки (big.db)
