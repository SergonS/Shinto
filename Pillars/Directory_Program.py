from Pillars.Directory_Functions import Directory_Func
from Pillars.Directory_Variables import Directory_Vars

class Program:
    def __init__(self):
        self.prog_directory = {}
        self.scope_manager = []

    def getProg(self, name: str) -> dict:
        return self.prog_directory[name]

    def addProg(self, name):
        self.prog_directory[name] = {
            "directory_func": Directory_Func(),
            "directory_vars": Directory_Vars()
        }

    def getDirectory(self) -> dict:
        return self.prog_directory

    def addScope(self, scope: str):
        self.scope_manager.append(scope)

    def popScope(self, scope: str):
        self.scope_manager.pop()

    def getCurrentScope(self) -> str:
        return self.scope_manager[-1]

    def getScope(self) -> list:
        return self.scope_manager

    def addNVars(self, counter: dict):
        self.prog_directory["numVars"] = counter