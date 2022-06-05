from Pillars.Variables import Variable

class Function:
    name: str
    data_type: str
    bReturn: bool = False
    initQuad: int
    params = {}
    vars = {}

    def __init__(self, name: str, data_type: str = "void"):
        self.name = name
        self.data_type = data_type
        
        if data_type != "void":
            self.bReturn = True

    def addParam(self, var: Variable):
        if var.name in self.params:
            print("Parameter already in function")
        else:
            self.params[var.name] = var

    def addVar(self, var: Variable):
        if var.name in self.params:
            print("Variable already in function")
        else:
            self.vars[var.name] = var

    def addIQuad(self, quad: int):
        self.initQuad = quad
        
    def showParams(self):
        if self.params is not None:
            for param in self.params:
                print(param)
    
    def showVars(self):
        if self.vars is not None:
            for var in self.vars:
                print(var)

    