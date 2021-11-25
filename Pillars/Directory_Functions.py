from Pillars.Directory_Variables import Directory_Vars

class Directory_Func:
    
    def __init__(self):
        self.directory = {}
        self.scope_manager = []

    def getFunc(self, name: str) -> dict:
        return self.directory[name]

    def addFunc(self, name: str, data_type: str = "void"):
        if data_type == "void":
            bReturn = True
        else:
            bReturn = False

        self.directory[name] = {
            "DirVars": Directory_Vars(),
            "params": Directory_Vars(),
            "data_type": data_type,
            "bReturn": bReturn
        }

    def getDirectory(self) -> dict:
        return self.directory

    def showDirectory(self):
        for e in self.directory:
            print(e + ": ", self.getFunc(e), self.getFunc(e))
            print("Directory of Variables:")

            self.getFunc(e)["DirVars"].showDirectory()
            self.getFunc(e)["params"].showDirectory()

    def addScope(self, scope: str):
        self.scope_manager.append(scope)

    def popScope(self):
        self.scope_manager.pop()

    def getCurrentScope(self) -> str:
        return self.scope_manager[-1]

    def getScope(self) -> list:
        return self.scope_manager

    def addNVars(self, counter: dict, name: str):
        self.directory[name]["numVars"] = counter

    def addInitialQuad(self, addr: int, name: str):
        self.directory[name]["initialQuad"] = addr