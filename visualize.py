from dataclasses import dataclass
from graph import Graph

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class GraphPlot:
    graph: Graph

    def __init__(self):
        self.vertices = []
        self.verticesName = {}
        self.adjacency_list = {}
        self.edgesDirected = {}

    def _prepare_plot(self):
        plt.axis("off")
        plt.autoscale(False)
        plt.xlim(-2, 2)
        plt.ylim(-2, 2)

    def __call__(
        self,
        *args,
        **kwargs,
    ):
        self._prepare_data()
        self._prepare_plot()
        fig, ax = plt.subplots()
        self._draw_vertices(ax)
        self._draw_edges(ax)
        plt.show()

    def _prepare_data(self):
        for node in self.graph.nodes:
            self.vertices.append(node.id)
            self.verticesName[node.id] = node.name
            self.adjacency_list[node.id] = []

        for edge in self.graph.edges:
            self.adjacency_list[edge.fromNode].append(edge.toNode)
            self.edgesDirected[edge.toNode] = (edge.directed, edge.name)

    def _draw_vertices(self, ax):
        for i, vertex in enumerate(self.vertices):
            x, y = np.cos(2 * np.pi * i / len(self.vertices)), np.sin(
                2 * np.pi * i / len(self.vertices)
            )
            ax.plot(x, y, "o", markersize=40, color="c")
            ax.text(
                x,
                y,
                str(self.verticesName[vertex]),
                ha="center",
                va="center",
                fontsize=10,
            )

    def _draw_edges(self, ax):
        for i, vertex in enumerate(self.vertices):
            for neighbor in self.adjacency_list[vertex]:
                i = self.vertices.index(vertex)
                j = self.vertices.index(neighbor)
                x1, y1 = self._get_coords(i)
                x2, y2 = self._get_coords(j)
                shift_x = 0.1 * (x2 - x1)
                x1 += shift_x
                x2 -= shift_x
                shift_y = 0.1 * (y2 - y1)
                y1 += shift_y
                y2 -= shift_y
                ax.plot([x1, x2], [y1, y2], color="black", linewidth=1)
                text_x = (x1 + x2) / 2
                text_y = (y1 + y2) / 2
                if self.edgesDirected[neighbor][0]:
                    ax.annotate(
                        self.edgesDirected[neighbor][1],
                        xy=(x2, y2),
                        xytext=(text_x, text_y),
                        arrowprops=dict(arrowstyle="->"),
                        ha="center",
                        va="center",
                    )
                else:
                    ax.annotate(
                        self.edgesDirected[neighbor][1],
                        xy=(x2, y2),
                        xytext=(text_x, text_y),
                        ha="center",
                        va="center",
                    )

    def _get_coords(self, k):
        return np.cos(2 * np.pi * k / len(self.vertices)), np.sin(
                2 * np.pi * k / len(self.vertices)
        )
