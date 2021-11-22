from Data_Types import Data_Type
from enum import Enum

class Variable(Enum):
    def __init__(self, name: str, data_type: Data_Type, value, address, scope: str):
        self.name = name
        self.data_type = data_type
        self.value = value
        self.address = address
        self.scope = scope
