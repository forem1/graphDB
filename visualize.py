import matplotlib.pyplot as plt
import numpy as np

def graphVisualizer(graph):
    vertices = []
    verticesName = {}
    adjacency_list = {}
    edgesDirected = {}
    for node in graph.nodes:
        vertices.append(node.id)
        verticesName[node.id] = node.name
        adjacency_list[node.id] = []

    for edge in graph.edges:
        adjacency_list[edge.fromNode].append(edge.toNode)
        edgesDirected[edge.toNode] = (edge.directed, edge.name)

    # Создаем графический объект
    fig, ax = plt.subplots()

    # Рисуем вершины
    for i, vertex in enumerate(vertices):
        x, y = np.cos(2 * np.pi * i / len(vertices)), np.sin(2 * np.pi * i / len(vertices))
        ax.plot(x, y, 'o', markersize=40, color='c')
        ax.text(x, y, str(verticesName[vertex]), ha='center', va='center', fontsize=10)

    # Рисуем ребра
    for i, vertex in enumerate(vertices):
        for neighbor in adjacency_list[vertex]:
            j = vertices.index(neighbor)
            if edgesDirected[neighbor][0]:
                i = vertices.index(vertex)
                j = vertices.index(neighbor)
                x1, y1 = np.cos(2 * np.pi * i / len(vertices)), np.sin(2 * np.pi * i / len(vertices))
                x2, y2 = np.cos(2 * np.pi * j / len(vertices)), np.sin(2 * np.pi * j / len(vertices))
                x1 += 0.1 * (x2 - x1)
                y1 += 0.1 * (y2 - y1)
                x2 -= 0.1 * (x2 - x1)
                y2 -= 0.1 * (y2 - y1)
                ax.plot([x1, x2], [y1, y2], color='black', linewidth=1)
                text_x = (x1 + x2) / 2
                text_y = (y1 + y2) / 2
                ax.annotate(edgesDirected[neighbor][1], xy=(x2, y2), xytext=(text_x, text_y), arrowprops=dict(arrowstyle="->"), ha='center', va='center')
            else:
                i = vertices.index(vertex)
                j = vertices.index(neighbor)
                x1, y1 = np.cos(2 * np.pi * i / len(vertices)), np.sin(2 * np.pi * i / len(vertices))
                x2, y2 = np.cos(2 * np.pi * j / len(vertices)), np.sin(2 * np.pi * j / len(vertices))
                x1 += 0.1 * (x2 - x1)
                y1 += 0.1 * (y2 - y1)
                x2 -= 0.1 * (x2 - x1)
                y2 -= 0.1 * (y2 - y1)
                ax.plot([x1, x2], [y1, y2], color='black', linewidth=1)
                text_x = (x1 + x2) / 2
                text_y = (y1 + y2) / 2
                ax.annotate(edgesDirected[neighbor][1], xy=(x2, y2), xytext=(text_x, text_y), ha='center', va='center')
    plt.axis('off')
    plt.autoscale(False)

    plt.xlim(-2, 2)
    plt.ylim(-2, 2)

    # Отображаем граф
    plt.show()