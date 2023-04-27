import matplotlib.pyplot as plt
import numpy as np

def graphVisualizer(graph):
    vertices = []
    adjacency_list = {}
    for index, node in enumerate(graph):
        vertices.append(node[0])
        edges = []
        for edge in node[2]:
            if edge:
                edges.append(str(graph[edge[0]][0]))
        adjacency_list[node[0]] = edges

    # Создаем графический объект
    fig, ax = plt.subplots()



    # Рисуем вершины
    for i, vertex in enumerate(vertices):
        x, y = np.cos(2 * np.pi * i / len(vertices)), np.sin(2 * np.pi * i / len(vertices))
        ax.plot(x, y, 'o', markersize=20, color='c')
        # circle = plt.Circle((x, y), 0.005, color='c')
        # ax.add_patch(circle)
        ax.text(x, y, vertex, ha='center', va='center', fontsize=15)

    # Рисуем ребра
    for i, vertex in enumerate(vertices):
        for neighbor in adjacency_list[vertex]:
            j = vertices.index(neighbor)
            # dx, dy = -0.5, -0.5
            # dx, dy = np.cos(2 * np.pi * i / len(vertices)) - np.cos(2 * np.pi * j / len(vertices)), np.sin(2 * np.pi * i / len(vertices)) - np.sin(2 * np.pi * j / len(vertices))
            # ax.arrow(np.cos(2 * np.pi * j / len(vertices)), np.sin(2 * np.pi * j / len(vertices)), dx, dy, length_includes_head=True, width=0.001, facecolor = 'k', head_width=0.1, head_length=0.1) # color=np.random.rand(3,)
            plt.annotate("", xy=(np.cos(2 * np.pi * j / len(vertices)), np.sin(2 * np.pi * j / len(vertices))), xytext=(np.cos(2 * np.pi * i / len(vertices)), np.sin(2 * np.pi * i / len(vertices))), arrowprops=dict(facecolor='black', width=0.5, headwidth=10, shrink=0.08))
    plt.axis('off')
    plt.autoscale(False)
    # ax.axis("equal")

    plt.xlim(-2, 2)
    plt.ylim(-2, 2)

    # Отображаем граф
    plt.show()