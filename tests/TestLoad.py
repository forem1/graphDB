from time import perf_counter_ns

from graph import Graph, Node, Edge
from visualize import GraphPlot
from memory_profiler import profile


@profile
def test_star_graph(node_num):
    graph = Graph("test")

    graph.addNode(Node(name=0))

    for num in range(1, node_num):
        graph.addNode(Node(name=num))
        graph.addEdge(
            Edge(
                fromNode=graph.nodes[0],
                toNode=graph.nodes[-1],
                name=f"edge-{num}",
                weight=1,
            )
        )
    return graph


@profile
def test_binary_tree(levels):
    graph = Graph("test")

    root_node = graph.addNode(Node(name=1))  # Root node

    def create_binary_tree(graph, level, prev_node_id):
        if level == 0:
            return

        left_node_name = f"left_{level}"
        right_node_name = f"right_{level}"

        left_node = Node(name=left_node_name)
        right_node = Node(name=right_node_name)

        graph.addNode(left_node)
        graph.addNode(right_node)

        edge_left = Edge(
            fromNode=prev_node_id,
            toNode=left_node.id,
            name=f"to_{left_node_name}",
        )
        edge_right = Edge(
            fromNode=prev_node_id,
            toNode=right_node.id,
            name=f"to_{right_node_name}",
        )

        graph.addEdge(edge_left)
        graph.addEdge(edge_right)

        create_binary_tree(graph, level - 1, left_node.id)
        create_binary_tree(graph, level - 1, right_node.id)

    create_binary_tree(graph, levels, root_node)

    return graph


@profile
def test_cycle_graph(node_num):
    graph = Graph("test")
    for num in range(node_num):
        graph.addNode(Node(name=num))
        if num > 0:
            graph.addEdge(
                Edge(
                    fromNode=graph.nodes[-2],
                    toNode=graph.nodes[-1],
                    name=f"edge-{num}",
                    weight=1,
                )
            )
    return graph


if __name__ == "__main__":
    start = perf_counter_ns()

    # graph = test_star_graph(100)
    # graph = test_cycle_graph(100)
    # graph = test_binary_tree(4)

    print("ms: " + str((perf_counter_ns() - start) / 1000))

    plot = GraphPlot(graph=graph)
    plot.draw()

# нагрузка
# цикла, звезда, линия,
