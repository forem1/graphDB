import unittest
from graph import Graph, Node, Edge


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph("test")
        self.nodeA = self.graph.addNode(Node(name="A"))
        self.nodeB = self.graph.addNode(Node(name="B"))
        self.nodeC = self.graph.addNode(Node(name="C"))
        self.nodeD = self.graph.addNode(Node(name="D"))
        self.nodeE = self.graph.addNode(Node(name="E"))
        self.nodeF = self.graph.addNode(Node(name="F"))
        self.nodeG = self.graph.addNode(Node(name="G"))
        self.nodeH = self.graph.addNode(Node(name="H"))
        self.nodeI = self.graph.addNode(Node(name="I"))
        self.graph.addEdge(
            Edge(fromNode=self.nodeA, toNode=self.nodeB, name="AtoB", weight=1)
        )
        self.graph.addEdge(
            Edge(fromNode=self.nodeB, toNode=self.nodeC, name="BtoC", weight=1)
        )
        self.graph.addEdge(
            Edge(fromNode=self.nodeC, toNode=self.nodeD, name="CtoD", weight=1)
        )
        self.graph.addEdge(
            Edge(fromNode=self.nodeD, toNode=self.nodeE, name="DtoE", weight=1)
        )
        self.graph.addEdge(
            Edge(fromNode=self.nodeE, toNode=self.nodeF, name="EtoF", weight=1)
        )
        self.graph.addEdge(
            Edge(fromNode=self.nodeF, toNode=self.nodeG, name="FtoG", weight=1)
        )
        self.graph.addEdge(
            Edge(fromNode=self.nodeG, toNode=self.nodeH, name="GtoH", weight=1)
        )
        self.graph.addEdge(
            Edge(fromNode=self.nodeH, toNode=self.nodeA, name="HtoA", weight=1)
        )
        self.graph.addEdge(
            Edge(fromNode=self.nodeC, toNode=self.nodeF, name="CtoF", weight=1)
        )
        self.graph.addEdge(
            Edge(fromNode=self.nodeF, toNode=self.nodeB, name="FtoB", weight=3)
        )
        self.graph.addEdge(
            Edge(fromNode=self.nodeH, toNode=self.nodeI, name="HtoI", weight=1)
        )
        self.graph.addEdge(
            Edge(
                fromNode=self.nodeH,
                toNode=self.nodeB,
                name="HtoB",
                weight=5,
                directed=False,
            )
        )

    def test_find_cycles(self):
        path = self.graph.findCycles()
        self.assertEqual(len(path), 66)

    def test_dfs(self):
        path = self.graph.dfs(self.nodeA, self.nodeI)
        self.assertEqual(len(path), 3)

    def test_find_shortest_path(self):
        path = self.graph.findShortestPath(self.nodeA, self.nodeI)
        self.assertEqual(len(path), 4)

    def test_find_dijkstra_shortest_path(self):
        path, _, weight = self.graph.findDijkstraShortestPath(self.nodeA, self.nodeI)
        self.assertEqual(len(path), 7)
        self.assertEqual(weight, 6)


if __name__ == "__main__":
    unittest.main()
