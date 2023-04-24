from graph import Graph
import random
from visualize import graphVisualizer

graph = Graph()

# 0
graph.addNewNode("1", [], [[1, True, [1]], [4, False, [2]]])

# 1
graph.addNewNode("2", [], [[0, False, [3]], [2, False, [4]], [4, False, [5]]])

# 2
graph.addNewNode("3", [], [
    [
        1,
        False,
        [6]
    ],
    [
        3,
        False,
        [7]
    ]
])

# 3
graph.addNewNode("4", [], [
    [
        2,
        False,
        [8]
    ],
    [
        4,
        False,
        [9]
    ],
    [
        5,
        False,
        [10]
    ]
])

# 4
graph.addNewNode("5", [], [
    [
        0,
        False,
        [11]
    ],
    [
        1,
        False,
        [12]
    ],
    [
        3,
        True,
        [13]
    ]
])

# 5
graph.addNewNode("6", [], [
    [
        3,
        False,
        [14]
    ]
])

# graph.addNewNode("0", [], [
#     [
#         1,
#         False,
#         [0]
#     ]
# ])
#
# graph.addNewNode("0", [], [
#     [
#         0,
#         False,
#         [0]
#     ]
# ])


print(graph.findShortestPath(5, 0, True, True))
# graphVisualizer(graph.nodesArray)
