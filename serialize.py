import os
import struct
import uuid
from dataclasses import dataclass
from typing import List, Union, Dict, Optional

from graph import Node, Edge, Graph

"""
    Node:
    id: UUID узла, занимает 16 байт
    name_size: размер имени в байтах (uint8)
    name_data: данные имени в формате UTF-8 строка
    link_size: размер ссылки в байтах (uint8)
    link_data: данные ссылки в формате UTF-8 строки
    primary: первична ли нода (True - если да, False - если нет)
    data_type: тип данных (True - если data это словарь, False - если data это произвольный тип)
    data_size: размер данных в байтах (uint64)
    data_value: данные, либо словарь, либо произвольный тип
"""
"""
    Edge:
    id: UUID узла, занимает 16 байт
    from_node: UUID источника, занимает 16 байт
    to_node: UUID приёмника, занимает 16 байт
    name_size: размер имени в байтах (uint8)
    name_data: данные имени в формате UTF-8 строка
    weight: вес грани (int16)
    directed: ориентация грани (True - если грань ориентированная, False - если грань не ориентированная)
    data_size: размер данных в байтах (uint32)
    data_value: данные в словаре
"""

class Serialize:
    def _serialize_node(self, node: Node) -> bytes:
        # Convert name to UTF-8 bytes
        name_bytes = str(node.name).encode("utf-8")
        name_size = len(name_bytes)

        # Convert link to UTF-8 bytes
        link_bytes = str(node.link).encode("utf-8")
        link_size = len(link_bytes)

        # Determine data type (1 for dictionary, 0 for other types)
        data_type = isinstance(node.data, dict)

        data_bytes = str(node.data).replace(" ", "").encode("utf-8")
        data_size = len(data_bytes)

        # Construct binary structure
        binary_data = struct.pack(
            f"<16sB{name_size}sB{link_size}s??Q{data_size}s",
            node.id.bytes,
            name_size,
            name_bytes,
            link_size,
            link_bytes,
            node.primary,
            data_type,
            data_size,
            data_bytes,
        )

        return binary_data

    def _deserialize_node(self, file) -> Optional[Node]:
        id_bytes = file.read(16)
        if not id_bytes:
            return None

        node_id = uuid.UUID(bytes=id_bytes)
        name_size = struct.unpack("B", file.read(1))[0]
        name_data = file.read(name_size).decode("utf-8")
        link_size = struct.unpack("B", file.read(1))[0]
        link_data = file.read(link_size).decode("utf-8")
        primary = struct.unpack("?", file.read(1))[0]
        data_type = struct.unpack("?", file.read(1))[0]
        data_size = struct.unpack("Q", file.read(8))[0]
        if data_type:
            data_data = file.read(data_size).decode("utf-8")
            data_value = (
                {}
                if data_data == "{}"
                else {
                    key.strip("'\""): value.strip("'\" ")
                    for key, value in (
                        pair.split(":", 1) for pair in data_data.strip("{}").split(",")
                    )
                }
            )
        else:
            data_value = file.read(data_size).decode("utf-8")
        return Node(
            id=node_id, name=name_data, link=link_data, primary=primary, data=data_value
        )

    def _serialize_edge(self, edge: Edge) -> bytes:
        # Convert name to UTF-8 bytes
        name_bytes = str(edge.name).encode("utf-8")
        name_size = len(name_bytes)

        data_bytes = str(edge.data).replace(" ", "").encode("utf-8")
        data_size = len(data_bytes)

        # Construct binary structure
        binary_data = struct.pack(
            f"<16s16s16sB{name_size}sH?I{data_size}s",
            edge.id.bytes,
            edge.fromNode.bytes,
            edge.toNode.bytes,
            name_size,
            name_bytes,
            edge.weight,
            edge.directed,
            data_size,
            data_bytes,
        )

        return binary_data

    def _deserialize_edge(self, file) -> Optional[Edge]:
        id_bytes = file.read(16)
        if not id_bytes:
            return None

        edge_id = uuid.UUID(bytes=id_bytes)
        from_node_id = uuid.UUID(bytes=file.read(16))
        to_node_id = uuid.UUID(bytes=file.read(16))
        name_size = struct.unpack("B", file.read(1))[0]
        name_data = file.read(name_size).decode("utf-8")
        weight = struct.unpack("h", file.read(2))[0]
        directed = struct.unpack("?", file.read(1))[0]
        data_size = struct.unpack("I", file.read(4))[0]
        data_data = file.read(data_size).decode("utf-8")
        data_value = (
            {}
            if data_data == "{}"
            else {
                key.strip("'\""): value.strip("'\" ")
                for key, value in (
                    pair.split(":", 1) for pair in data_data.strip("{}").split(",")
                )
            }
        )
        return Edge(
            id=edge_id,
            fromNode=from_node_id,
            toNode=to_node_id,
            name=name_data,
            weight=weight,
            directed=directed,
            data=data_value,
        )

    def _pass_zero_bytes(self, file):
        while True:
            byte = file.read(1)
            if not byte:
                break
            if byte != b"\x00":
                file.seek(-1, 1)
                break
        return file

    def write_nodes(self, filename: str, nodes: List[Node], position: int = -1) -> int:
        with open(filename, "ab" if position == -1 else "r+b") as file:
            if position != -1:
                file.seek(position)
            for node in nodes:
                file.write(self._serialize_node(node))
            return file.tell()

    def read_nodes(self, filename: str, position: int = -1, elements: int = 0) -> List[Node]:
        nodes = []
        with open(filename, "rb") as file:
            if position != -1:
                file.seek(position)
            while True:
                file = self._pass_zero_bytes(file)
                element = self._deserialize_node(file)
                if element is None:
                    break
                else:
                    nodes.append(element)

                elements -= 1
                if elements == 0:
                    break
            return nodes

    def index_nodes(self, filename: str, find: Optional[uuid.UUID] = None) -> Union[int, Dict[uuid.UUID, int]]:
        index = {}
        with open(filename, "rb") as file:
            while True:
                file = self._pass_zero_bytes(file)
                element_start = file.tell()  # Запоминаем начало структуры
                element = self._deserialize_node(file)
                if element is None:
                    break
                if find and element.id == find:
                    return element_start
                else:
                    index[element.id] = (element_start, file.tell())
            return index

    def delete_node(self, filename: str, find: Union[int, uuid.UUID]):
        index = self.index_nodes(filename)

        start = 0
        end = 0

        if isinstance(find, int):
            start = find
            end = min({value[0] for value in index.values() if value[0] > find}, default=None)
        elif isinstance(find, uuid.UUID) and find in index:
            start = index[find][0]
            end = index[find][1]

        with open(filename, "r+b") as file:  # Открываем файл для чтения и записи
            file.seek(start)

            if end is not None:
                interval_size = end - start
            else:
                file.seek(0, 2)  # Переходим в конец файла
                file_size = file.tell()  # Получаем текущий размер файла
                interval_size = file_size - start

            for _ in range(interval_size):
                file.write(struct.pack("B", 0))

    def defragment_nodes(self, filename: str):
        index = self.index_nodes(filename)

        output_filename = f"temp_{filename}"
        with open(filename, "rb") as input_file:
            with open(output_filename, "wb") as output_file:
                for start, end in index.values():
                    input_file.seek(start)
                    output_file.write(input_file.read(end - start))

        os.remove(filename)
        os.rename(output_filename, filename)

    def write_edges(self, filename: str, edges: List[Edge], position: int = -1) -> int:
        with open(filename, "ab" if position == -1 else "r+b") as file:
            if position != -1:
                file.seek(position)
            for edge in edges:
                file.write(self._serialize_edge(edge))
            return file.tell()

    def read_edges(self, filename: str, position: int = -1, elements: int = 0) -> List[Edge]:
        edges = []
        with open(filename, "rb") as file:
            if position != -1:
                file.seek(position)
            while True:
                element = self._deserialize_edge(file)
                if element is None:
                    break
                else:
                    edges.append(element)
                elements -= 1
                if elements == 0:
                    break
            return edges

    def index_edges(self, filename: str, find: Optional[uuid.UUID] = None) -> Union[int, Dict[uuid.UUID, int]]:
        index = {}
        with open(filename, "rb") as file:
            while True:
                file = self._pass_zero_bytes(file)
                element_start = file.tell()  # Запоминаем начало структуры
                element = self._deserialize_edge(file)
                if element is None:
                    break
                if find and element.id == find:
                    return element_start
                else:
                    index[element.id] = (element_start, file.tell())
            return index

    def delete_edge(self, filename: str, find: Union[int, uuid.UUID]):
        index = self.index_edges(filename)

        start = 0
        end = 0

        if isinstance(find, int):
            start = find
            end = min({value[0] for value in index.values() if value[0] > find}, default=None)
        elif isinstance(find, uuid.UUID) and find in index:
            start = index[find][0]
            end = index[find][1]

        with open(filename, "r+b") as file:  # Открываем файл для чтения и записи
            file.seek(start)

            if end is not None:
                interval_size = end - start
            else:
                file.seek(0, 2)  # Переходим в конец файла
                file_size = file.tell()  # Получаем текущий размер файла
                interval_size = file_size - start

            for _ in range(interval_size):
                file.write(struct.pack("B", 0))

    def defragment_edges(self, filename: str):
        index = self.index_edges(filename)

        output_filename = f"temp_{filename}"
        with open(filename, "rb") as input_file:
            with open(output_filename, "wb") as output_file:
                for start, end in index.values():
                    input_file.seek(start)
                    output_file.write(input_file.read(end - start))

        os.remove(filename)
        os.rename(output_filename, filename)


    def write_graph(self, graph: Graph, path: str):
        if not os.path.exists(path):
            os.makedirs(path)

        self.write_nodes(os.path.join(path, "nodes"), graph.nodes)
        self.write_edges(os.path.join(path, "edges"), graph.edges)

    def read_graph(self, graph: Graph, path: str):
        if not os.path.isdir(path):
            raise Exception(f"The path {path} is not a directory")

        nodes_file_path = os.path.join(path, "nodes")
        edges_file_path = os.path.join(path, "edges")

        if os.path.exists(nodes_file_path):
            graph.nodes = self.read_nodes(nodes_file_path)
        else:
            raise Exception(f"Nodes file not found at {nodes_file_path}")

        if os.path.exists(edges_file_path):
            graph.edges = self.read_edges(edges_file_path)
        else:
            raise Exception(f"Edges file not found at {edges_file_path}")


# nodes = [
#     Node(
#         id=uuid.UUID("7944f8b4-04a6-43d2-b253-46c61fec2e8d"),
#         name="node1",
#         link="asddsa",
#         primary=True,
#         data={"key1": "value1"},
#     ),
#     Node(
#         id=uuid.UUID("e134f354-3283-4f0b-94d9-fec9fcd737c2"),
#         name="node2",
#         link="asddsa",
#         data={"key2": "value2"},
#     ),
#     Node(
#         id=uuid.UUID("602ffb44-fa16-460b-a24d-fadff449dc08"),
#         name="node3",
#         link="asddsa",
#         data={"key3": "value3"},
#     ),
#     Node(
#         id=uuid.UUID("602ffb44-fa16-463b-a24d-fadff449dc08"),
#         name="node4",
#         link="asddsa",
#         data={"key3": "value3"},
#     ),
# ]
#
# edges = [
#     Edge(
#         id=uuid.UUID("602ffb44-fa16-463b-a24d-fadff449dc08"),
#         name="edge1",
#         fromNode=uuid.UUID("96c68acb-e7fc-462b-ac7d-8bd71221a0d3"),
#         toNode=uuid.UUID("96c68acb-e7fc-462b-ac7d-81d71221a0d3"),
#         weight=123,
#         directed=False,
#         data={"key1": "value1"},
#     ),
#     Edge(
#         id=uuid.UUID("602ffb44-fa16-463b-a24d-fadff449dc09"),
#         name="edge2",
#         fromNode=uuid.UUID("96c68acb-e7fc-462b-ac7d-8bd71221a0d3"),
#         toNode=uuid.UUID("96c68acb-e7fc-462b-ac7d-8bd71221a0d3"),
#         weight=111,
#         directed=True,
#         data={"key1": "value1"},
#     ),
#     Edge(
#         id=uuid.UUID("602ffb44-fa16-463b-a24d-fadff449dc10"),
#         name="edge2",
#         fromNode=uuid.UUID("96c68acb-e7fc-462b-ac7d-8bd71221a0d3"),
#         toNode=uuid.UUID("96c68acb-e7fc-462b-ac7d-8bd71221a0d3"),
#         weight=123,
#         directed=False,
#         data={"key1": "value1"},
#     ),
#     Edge(
#         id=uuid.UUID("602ffb44-fa16-463b-a24d-fadff449dc11"),
#         name="edge3",
#         fromNode=uuid.UUID("96c68acb-e7fc-462b-ac7d-8bd71221a0d3"),
#         toNode=uuid.UUID("96c68acb-e7fc-462b-ac7d-8bd71221a0d3"),
#         weight=123,
#         directed=False,
#         data={"key1": "value1"},
#     ),
# ]
#
#
# def main():
#     # write = write_nodes("nodes.bin", nodes, position=0)
#     # read = read_nodes("nodes.bin")
#     # delete_node("nodes.bin", find=56)
#     # read = read_nodes("nodes.bin")
#     # # print(write)
#     # print(read)
#     # print(len(read))
#     # defragment_nodes("nodes.bin")
#     # print(index_nodes("nodes.bin"))
#
#     print(write_edges("edges.bin", edges, position=0))
#     # read = read_edges("edges.bin")
#     # print(read)
#     # print(len(read))
#     print(index_edges("edges.bin"))
#     delete_edge("edges.bin", find=uuid.UUID("602ffb44-fa16-463b-a24d-fadff449dc09"))
#     print(index_edges("edges.bin"))
#     defragment_edges("edges.bin")
#     print(index_edges("edges.bin"))
#
#
# if __name__ == "__main__":
#     main()
