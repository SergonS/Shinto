from Pillars.Data_Types import Data_Type
from Pillars.Variables import Variable

class Directory_Vars:

    def __init__(self):
        self.directory = {}

    def getVar(self, name: str) -> Variable:
        return self.directory[name]

    def appendToDirectory(self, name: str, data_type: str, value: int = 0, addr: int = 0, dimensions: list = None, spaces: int = 0):
        self.directory[name] = {
            'var' : Variable(name, Data_Type.strToType(data_type), value, addr, dimensions, spaces)
        }

    def getDirectory(self) -> dict:
        return self.directory

    def showDictionary(self):
        for var in self.directory:
            print(var.data_type + " " + var.name + " at address " + var.addr + " with a value of " + var.value) 