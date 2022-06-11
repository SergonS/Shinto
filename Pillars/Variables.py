from multiprocessing.context import SpawnProcess


class Variable:
    name: str
    data_type: str
    value: str = "Null"
    addr: int
    dimensions: int
    spaces: int
    scope: str

    def __init__(self, name: str, data_type: str, addr: int, dimensions: int, spaces: int , scope: str):
        self.name = name
        self.data_type = data_type
        self.addr = addr
        self.dimensions = dimensions
        self.spaces = spaces
        self.scope = scope

    def __repr__(self) -> str:
        return f'Variable({self.name}, {self.scope}, {self.data_type}, {self.value}, {self.addr})'
