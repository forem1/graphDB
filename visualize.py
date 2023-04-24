import json
import matplotlib.pyplot as plt
import math
import random

def graphVisualizer(graph):

    nodeList = []

    for i in graph:
        # print(i[0])
        nodeList.append(i[0])

    nodeCoordinates = []

    circle_r = 30

    generatedCircle_r = 2
    collisionShift = 15

    fig, ax = plt.subplots()

    # проходим через все ноды
    for n in range(0, len(nodeList)):
        collision = True

        # Пока сгенерерированная нода пересекается с другими, генерируем новую
        while collision:
            alpha = 2 * math.pi * random.random()
            r = circle_r * math.sqrt(random.random())
            x = r * math.cos(alpha)
            y = r * math.sin(alpha)

            if len(nodeCoordinates) == 0:
                collision = False

            for i in nodeCoordinates:
                if i[0] != x + generatedCircle_r + collisionShift and i[1] != y + generatedCircle_r + collisionShift:
                    collision = False
        nodeCoordinates.append((x, y))
        plt.text(x-generatedCircle_r/2, y-generatedCircle_r/2, nodeList[n], fontsize=14)

    # print(nodeCoordinates)

    # ax.arrow(0, 3, 2, 1, head_width=0.5, head_length=0.5, fc='k', ec='k')

    cnt = 0
    for i in nodeCoordinates:
        circle = plt.Circle(i, generatedCircle_r, color='c')
        ax.add_patch(circle)

        nodeEdges = graph[cnt][2]

        # Add edges between nodes
        if len(nodeEdges) > 0:
            for pointer in nodeEdges:

                if pointer[1]: #Get direction
                    dx = nodeCoordinates[pointer[0]][0] - i[0]
                    dy = nodeCoordinates[pointer[0]][1] - i[1]

                    plt.arrow(i[0], i[1], dx, dy, head_width=0.5, head_length=0.5, color='black')
                else:
                   plt.plot((nodeCoordinates[pointer[0]][0], i[0]), (nodeCoordinates[pointer[0]][1], i[1]))

        cnt += 1

    plt.xlim(-30, 30)
    plt.ylim(-30, 30)
    # plt.axis('off')
    # plt.autoscale(False)
    # ax.axis("equal")

    plt.show()