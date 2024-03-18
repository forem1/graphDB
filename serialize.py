import struct
import uuid

from graph import Node, Edge

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


def serialize_node(node: Node):
    # Convert name to UTF-8 bytes
    name_bytes = node.name.encode("utf-8")
    name_size = len(name_bytes)

    # Convert link to UTF-8 bytes
    link_bytes = node.link.encode("utf-8")
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


def deserialize_node(file) -> Node:
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
        data_value = {
            key.strip("'\""): value.strip("'\" ")
            for key, value in (
                pair.split(":", 1) for pair in data_data.strip("{}").split(",")
            )
        }
    else:
        data_value = file.read(data_size).decode("utf-8")
    return Node(
        id=node_id, name=name_data, link=link_data, primary=primary, data=data_value
    )


def serialize_edge(edge: Edge):
    # Convert name to UTF-8 bytes
    name_bytes = edge.name.encode("utf-8")
    name_size = len(name_bytes)

    data_bytes = str(edge.data).replace(" ", "").encode("utf-8")
    data_size = len(data_bytes)

    # Construct binary structure
    binary_data = struct.pack(
        f"<16s16s16sB{name_size}sh?I{data_size}s",
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


def deserialize_edge(file) -> Edge:
    id_bytes = file.read(16)
    if not id_bytes:
        return None

    node_id = uuid.UUID(bytes=id_bytes)
    from_node_id = uuid.UUID(bytes=file.read(16))
    to_node_id = uuid.UUID(bytes=file.read(16))
    name_size = struct.unpack("B", file.read(1))[0]
    name_data = file.read(name_size).decode("utf-8")
    weight = struct.unpack("h", file.read(2))[0]
    directed = struct.unpack("?", file.read(1))[0]
    data_size = struct.unpack("I", file.read(4))[0]
    data_data = file.read(data_size).decode("utf-8")
    data_value = {
        key.strip("'\""): value.strip("'\" ")
        for key, value in (
            pair.split(":", 1) for pair in data_data.strip("{}").split(",")
        )
    }
    return Edge(
        id=node_id,
        fromNode=from_node_id,
        toNode=to_node_id,
        name=name_data,
        weight=weight,
        directed=directed,
        data=data_value,
    )


def write_node(file: str, nodes, position: int = -1) -> int:
    with open(file, "ab" if position == -1 else "wb") as file:
        if position != -1:
            file.seek(position)
        for node in nodes:
            file.write(serialize_node(node))
        return file.tell()


def read_node(file: str, position: int = -1, elements: int = 0):
    nodes = []
    with open(file, "rb") as file:
        if position != -1:
            file.seek(position)
        while True:
            element = deserialize_node(file)
            if element is None:
                break
            else:
                nodes.append(element)

            elements -= 1
            if elements == 0:
                break
        return nodes


def index_node(file: str, find=True):
    index = {}
    with open(file, "rb") as file:
        while True:
            element = deserialize_node(file)
            if element is None:
                break
            if type(find) is uuid.UUID and element.id == find:
                return file.tell()
            else:
                index[element.id] = file.tell()
        return index


def write_edge(file: str, edges, position: int = -1) -> int:
    with open(file, "ab" if position == -1 else "wb") as file:
        if position != -1:
            file.seek(position)
        for edge in edges:
            file.write(serialize_edge(edge))
        return file.tell()


def read_edge(file: str, position: int = -1, elements: int = 0):
    edges = []
    with open(file, "rb") as file:
        if position != -1:
            file.seek(position)
        while True:
            element = deserialize_edge(file)
            if element is None:
                break
            else:
                edges.append(element)

            elements -= 1
            if elements == 0:
                break
        return edges


def index_edge(file: str, find=True):
    index = {}
    with open(file, "rb") as file:
        while True:
            element = deserialize_edge(file)
            if element is None:
                break
            if type(find) is uuid.UUID and element.id == find:
                return file.tell()
            else:
                index[element.id] = file.tell()
        return index


nodes = [
    Node(name="node1", link="asddsa", primary=True, data={"key1": "value1"}),
    Node(name="node2", link="asddsa", data={"key2": "value2"}),
    Node(name="node3", link="asddsa", data={"key3": "value3"}),
]

edges = [
    Edge(
        name="edge1",
        fromNode=uuid.UUID("96c68acb-e7fc-462b-ac7d-8bd71221a0d3"),
        toNode=uuid.UUID("96c68acb-e7fc-462b-ac7d-81d71221a0d3"),
        weight=123,
        directed=False,
        data={"key1": "value1"},
    ),
    Edge(
        name="edge2",
        fromNode=uuid.UUID("96c68acb-e7fc-462b-ac7d-8bd71221a0d3"),
        toNode=uuid.UUID("96c68acb-e7fc-462b-ac7d-8bd71221a0d3"),
        weight=111,
        directed=True,
        data={"key1": "valufdgdfe1"},
    ),
    Edge(
        name="edge2",
        fromNode=uuid.UUID("96c68acb-e7fc-462b-ac7d-8bd71221a0d3"),
        toNode=uuid.UUID("96c68acb-e7fc-462b-ac7d-8bd71221a0d3"),
        weight=123,
        directed=False,
        data={"key1": "value1"},
    ),
    Edge(
        name="edge3",
        fromNode=uuid.UUID("96c68acb-e7fc-462b-ac7d-8bd71221a0d3"),
        toNode=uuid.UUID("96c68acb-e7fc-462b-ac7d-8bd71221a0d3"),
        weight=123,
        directed=False,
        data={"key1": "value1"},
    ),
]


def main():
    print(write_node("nodes.bin", nodes, position=0))
    read = read_node("nodes.bin")
    print(read)
    print(len(read))
    print(index_node("nodes.bin"))

    print(write_edge("edges.bin", edges, position=0))
    read = read_edge("edges.bin")
    print(read)
    print(len(read))
    print(index_edge("edges.bin"))


if __name__ == "__main__":
    main()
