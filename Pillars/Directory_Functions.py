from Pillars.Directory_Variables import Directory_Vars
from Pillars.Functions import Function

class Directory_Func:
    
    def __init__(self):
        self.directory = {}

    def getFunc(self, name: str) -> Function:
        return self.directory[name]

    def addFunc(self, function: Function):
        self.directory[function.name] = function

    def getDirectory(self) -> dict:
        return self.directory

    def showDirectory(self):
        if self.directory is not None:
            for func in self.directory:
                print("Function " + self.directory[func].name + " of type " + self.directory[func].data_type)

    def hasFunc(self, name: str) -> bool:
        hasKey = False

        if name in self.directory:
            hasKey = True
        
        return hasKey