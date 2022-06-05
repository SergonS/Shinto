class Variable:
    name: str
    data_type: str
    value: str
    addr: int
    dimensions: int
    spaces: int
    scope: str

    def __init__(self, name: str, data_type: str, value, addr: int, dimensions: int, spaces: int , scope: str):
        self.name = name
        self.data_type = data_type
        self.value = value
        self.addr = addr
        self.dimensions = dimensions
        self.spaces = spaces
        self.scope = scope
