from Pillars.Data_Types import Data_Type
from Pillars.Variables import Variable

class Directory_Vars:

    def __init__(self):
        self.directory = {}

    def getVar(self, name: str) -> dict:
        return self.directory[name]

    def appendToDirectory(self, name: str, type: str, addr: int, dims: list = None, r: int = 0):
        self.directory[name] = {
            "type": type,
            "address": addr, 
            "dims": dims,
            "R": R
        }

    def getDirectory(self) -> dict:
        return self.directory

    def showDictionary(self):
        for var in self.directory:
            print(var + ":", self.getVar(var))