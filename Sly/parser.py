from sly import Parser
from Sly.lexer import ShintoLexer
from Pillars.Directory_Functions import Directory_Func
from Pillars.Directory_Variables import Directory_Vars
from Pillars.QuadManager import QuadOverseer
from Pillars.Constants import C_Table
from VM.Delimitations import Delimitation
from Pillars.Directory_Program import Program
import sys

### PARSER ###

"""

    Parser that assures valid structure of the input code

"""

class ShintoParser(Parser):
    tokens = ShintoLexer.tokens
    ERROR_FLAG = False
    stack_dim = []
    stack_params = []
    stack_vars = []

    call_params = []
    counter_params = 0
    counter = 1

    #precedence = (
     #   ('left', '+', '-'),
      #  ('left', '*', '/'),
       # ('right', 'UMINUS'),           
    #)

    constants = C_Table()
    quads = QuadOverseer()
    delimitation = Delimitation()
    program = Program()

    def __init__(self):
        self.env = {}

    
    @_('PROG ID ";" collection')
    def program(self, x):
        self.program.addProg(x[-1])
        self.program.addScope(x[-1])

    @_('var collection')
    def collection(self, x):
        pass

    @_('function collection')
    def collection(self, x):
        pass

    @_('main')
    def collection(self, x):
        scope = self.program.getCurrentScope()
        fScope = self.program.getProg(scope)["directory_func"].getCurrentScope()

        counter = self.delimitation.getLVarsCounter()
        self.program.getProg(scope)["directory_func"].addNVars(counter, fScope)
        self.program.popScope() 
        pass

    @_('MAIN "(" ")" "{" maina')
    def main(self, x):
        self.quads.finishGoto("gotof")
        self.program.getProg(self.prog.getCurrentScope())["directory_func"].addProg(x[-1])
        self.program.getProg(self.prog.getCurrentScope())["directory_func"].addScope(x[-1])
        self.delimitation.resetL()
        pass

    @_('var maina')
    def maina(self, x):
        pass

    @_('statement maina')
    def maina(self, x):
        pass

    @_('"}"')
    def maina(self, x):
        pass

    @_('VAR type idlist ";"')
    def var(self, x):
        fLength = len(self.program.getProg(self.prog.getCurrentScope())["directory_func"].getScope())
        pScope = self.program.getCurrentScope()

        for e in self.stack_vars:
            # Global
            if fLength == 0:
                if len(self.program.getScope()) == 1:
                    # Add var to globals
                    type = "global_" + x[-1]
                    addr = self.delimitation.getAddr(type) + self.delimitation.getCounter(type)

                    # If array is found
                    if e[1] == True:
                        dimension = e[2]
                        r = self.calcR(dimension)
                        self.delimitation.verifyDelimitation(addr + r, type)
                        self.program.getProg(pScope)["directory_vars"].appendToDictionary(e[0], x[-1], addr, dimension, r - 1)
                        self.delimitation.updateCounter(type, r)
                    # Atomic variable
                    else:
                        self.delimitation.verifyDelimitation(addr, type)
                        self.program.getProg(pScope)["directory_vars"].appendToDictionary(e[0], x[-1], addr)
                        self.delimitation.updateCounter(type)

            # Local    
            else:
                funcScope = self.program.getProg(pScope)["directory_func"].getCurrentScope()
                type = "local_" + x[-1]
                addr = self.delimitation.getAddr(type) + self.delimitation.getCounter(type)

                # If array is found
                if e[1] == True:
                    dimension = e[2]
                    r = self.calcR(dimension)
                    self.delimitation.verifyDelimitation(addr + r, type)
                    self.program.getProg(pScope)["directory_vars"].appendToDictionary(e[0], x[-1], addr, dimension, r - 1)
                    self.delimitation.updateCounter(type, r)                    
                    # Atomic variable
                else:
                    self.delimitation.verifyDelimitation(addr, type)
                    self.program.getProg(pScope)["directory_vars"].appendToDictionary(e[0], x[-1], addr)
                    self.delimitation.updateCounter(type)
            self.stack_vars.clear()
            pass

    @_('ID darr idlistn')
    def idlist(self, x):
        self.stack_vars.append((x[-1], False))

        if x[1] is not None:
            self.stack_dim.append(x[2])
            aTuple = (self.stack_vars[-1][0], True)
            self.stack_vars.pop()
            self.stack_vars.append(aTuple)

        if self.stack_vars[-1][1]:
            bTuple = (self.stack_vars[-1][0], True, self.stack_dim.copy())
            self.stack_vars.pop()
            self.stack_vars.append(bTuple)
            self.stack_dim.clear()
        pass

    @_('"," idlist')
    def idlistn(self, x):
        pass

    @_('')
    def idlistn(self, x):
        pass

    @_('"[" C_INT "]" darra')
    def darr(self, x):
        pass

    @_('')
    def darr(self, x):
        pass

    @_('"[ C_INT "]"')
    def darra(self, x):
        pass

    @_('')
    def darra(self, x):
        pass

    @_('"[" expr "] arra')
    def arr(self, x):
        self.quads.addOperator("(")
        
        self.quads.addOperator(")")

        nameVar = x[-6]
        var = self.verifyVarExists(nameVar, x)
        if var is None:
            nameVar = x[-12]
            var = self.verifyVarExists(nameVar, x)
        if var[2] is None:
            sys.exit(f"{nameVar} is not an array")
        elif len(var[2]) == 1:
            limit = var[2][0]
            self.quads.addOperand(limit, "int")
            self.quads.addOperator("ver")
        elif len(var[2]) == 2:
            if (self.counter < 0):
                self.counter = 1
            limit = var[2][self.counter]
            self.quads.addOperand(limit, "int")
            self.quads.addOperator("ver")
            if self.counter > 0:
                self.generateSD(nameVar, x)
            if self.counter == 0:
                self.generateSDS(nameVar)
            self.counter = -1

        variable = self.verifyVarExists(x[-8], x)
        self.quads.addOperand(var[0], var[1])
        self.quads.addOperator("arrbase")
        pass

    @_('')
    def arr(self, x):
        pass

    @_('"[')
    def arra(self, x):
        self.quads.addOperator("(")
        
        self.quads.addOperator(")")

        nameVar = x[-6]
        var = self.verifyVarExists(nameVar, x)
        if var is None:
            nameVar = x[-12]
            var = self.verifyVarExists(nameVar, x)
        if var[2] is None:
            sys.exit(f"{nameVar} is not an array")
        elif len(var[2]) == 1:
            limit = var[2][0]
            self.quads.addOperand(limit, "int")
            self.quads.addOperator("ver")
        elif len(var[2]) == 2:
            if (self.counter < 0):
                self.counter = 1
            limit = var[2][self.counter]
            self.quads.addOperand(limit, "int")
            self.quads.addOperator("ver")
            if self.counter > 0:
                self.generateSD(nameVar, x)
            if self.counter == 0:
                self.generateSDS(nameVar)
            self.counter = -1
        pass

    @_('')
    def arra(self, x):
        pass

    @_('FUNC ID "(" funca ")" funcb "{" funcc')
    def function(self, x):
        if x[1] == ":":
            x[0] = x[2]
        if x[1] == "":
            x[0] = ""
        
        scope = self.program.getCurrentScope()
        fScope = self.program.getProg(scope)["directory_func"].getCurrentScope()
        for param in self.stack_params:
            name, type = param
            addr = self.delimitation.getAddr("local_" + type) + self.delimitation.getCounter("local_" + type)
            self.delimitation.verifyDelimitation(addr, "local_" + type)
            self.program.getProg(scope)["directory_func"].getFunc(fScope)["params"].appendToDirectory(name, type, addr)
            self.delimitation.updateCounter("local_" + type)
        self.stack_params.clear()
        pass

    @_('params')
    def funca(self, x):
        pass

    @_('')
    def funca(self, x):
        pass

    @_('":" type')
    def funcb(self, x):
        pass

    @_('')
    def funcb(self, x):
        pass

    @_('var funcc')
    def funcc(self, x):
        pass

    @_('statement funcc')
    def funcc(self, x):
        pass

    @_('"}"')
    def funcc(self, x):
        scope = self.program.getCurrentScope()
        fScope = self.program.getProg(scope)["directory_func"].getCurrentScope()

        counter = self.delimitation.getLVarsCounter()
        self.program.getProg(scope)["directory_func"].addNVars(counter, fScope)
        bR = self.program.getProg(scope)["directory_func"].getFunc(fScope)["bReturn"]

        if bR is False:
            sys.exit(f"Return not found for function {fScope}")
        self.program.getProg(scope)["directory_func"].popScope()
        type = self.program.getProg(scope)["directory_func"].getFunc(fScope)["bReturn"]
        self.quads.addOperator("endfunc")
        pass

    @_('type ID paramsa')
    def params(self, x):
        self.stack_params.append((x[-3], x[-1]))
        pass

    @_('"," type ID paramsa')
    def paramsa(self, x):
        self.stack_params.append((x[-3], x[-1]))
        pass

    @_('')
    def paramsa(self, x):
        pass

    @_('ID "(" callfa ")"')
    def callf(self, x):
        found = False
        i_scope = len(self.program.getScope()) - 1
        while i_scope >= 0 and found is False:
            scope = self.program.getScope()[i_scope]
            fDir = self.program.getProg(scope)["directory_func"].getDirectory()
            func = self.verifyFD(fDir, x[-1])
            i_scope = i_scope - 1

            if func is None:
                sys.exit(f"Declaration of function {x[-1]} not found")
        self.createEra(x[-1], func)

        self.quads.addOperator("(")

        if self.counter_params < len(self.call_params):
            sys.exit(f"Missing {len(self.call_params) - self.counter_params} params")

        self.quads.addOperator(")")

        name = x[-8]
        scope = self.program.getCurrentScope()
        fDir = self.program.getProg(scope)["directory_func"].getDirectory()
        func = self.verifyFD(fDir, name)
        quad_s = func["initialQuad"]
        self.quads.addOperand(quad_s, name)
        self.quads.addOperator("gosub")
        if func["data_type"] != "void":
            var = self.program.getProg(scope)["directory_vars"].getVar(name)
            self.quads.addOperand(var["address"], var["type"])
            self.quads.addOperator("assignr")
        pass

    @_('expr callfb')
    def callfa(self, x):
        self.quads.unloadPolishVector()
        if self.counter_params < len(self.call_params):
            self.quads.addOperand(self.call_params[self.counter_params]["address"], self.call_params[self.counter_params]["type"])
            self.quads.addOperator("params")
            self.counter_params = self.counter_params + 1
        else:
            sys.exit(f"Found many params")
        pass

    @_('')
    def callfa(self, x):
        pass

    @_('"," callfa')
    def callfb(self, x):
        pass

    @_('')
    def callfb(self, x):
        pass    

    @_('ID')
    def type(self, x):
        x[0] = x[1]
        pass

    @_('INT')
    def type(self, x):
        x[0] = x[1]
        pass

    @_('FLOAT')
    def type(self, x):
        x[0] = x[1]
        pass

    @_('STRING')
    def type(self, x):
        x[0] = x[1]
        pass

    @_('BOOLEAN')
    def type(self, x):
        x[0] = x[1]
        pass

    @_('assign')
    def statement(self, x):
        self.quads.unloadPolishVector()
        pass

    @_('cond')
    def statement(self, x):
        self.quads.unloadPolishVector()
        pass

    @_('print')
    def statement(self, x):
        self.quads.unloadPolishVector()
        pass

    @_('input')
    def statement(self, x):
        self.quads.unloadPolishVector()
        pass

    @_('return')
    def statement(self, x):
        self.quads.unloadPolishVector()
        pass

    @_('vcall')
    def statement(self, x):
        self.quads.unloadPolishVector()
        pass

    @_('awhile')
    def statement(self, x):
        self.quads.unloadPolishVector()
        pass

    @_('callf ";"')
    def vcall(self, x):
        pass

    @_('ID ";" vcall')
    def vcall(self, x):
        pass

    @_('WHILE "(" expr ")" "{" whilea')
    def awhile(self, x):
        self.quads.addJump()

        self.quads.addOperator("gotof")

        self.quads.addOperator("gotow")
        pass

    @_('statement whilea')
    def whilea(self, x):
        pass

    @_('"}"')
    def whilea(self, x):
        pass

    @_('varc')
    def varcall(self, x):
        if not isinstance(x[-1], str):
            if type(x[-1]).__name__ == "int":
                addr = self.delimitation.getAddr("constant_int") + self.delimitation.getCounter("constant_int")
                self.delimitation.verifyDelimitation(addr, "constant_int")
                added = self.constants.addInteger(str(x[-1]), addr)
                if added == True:
                    self.delimitation.updateCounter("constant_int")
                addr = self.constants.getInteger(str(x[-1]))
            else:
                addr = self.delimitation.getAddr("constant_float") + self.delimitation.getCounter("constant_float")
                self.delimitation.verifyDelimitation(addr, "constant_float")
                added = self.constants.addFloat(str(x[-1]), addr)
                if added == True:
                    self.delimitation.updateCounter("constant_float")
                addr = self.constants.getFloat(str(x[-1]))
            self.quads.addOperand(addr, type(x[-1]).__name__)
        elif isinstance(x[-1], str) and x[-1][0] == '"':
            addr = self.delimitation.getAddr("constant_string") + self.delimitation.getCounter("constant_string")
            self.delimitation.verifyDelimitation(addr, "constant_string")
            added = self.constants.addString(x[-1], addr)
            if added == True:
                self.delimitation.updateCounter("constant_string")
            addr = self.constants.getString(x[-1])
            self.quads.addOperand(addr, "string")
        elif isinstance(x[-1], str) and (x[-1] == 'false' or x[-1] == 'true'):
            addr = self.delimitation.getAddr("constant_boolean") + self.delimitation.getCounter('constant_boolean')
            self.delimitation.verifyDelimitation(addr, "constant_boolean")
            added = self.constants.addBoolean(str(x[-1]), addr)
            if added == True:
                self.delimitation.updateCounter("constant_boolean")
            addr = self.constants.getBoolean(x[-1])
            self.quads.addOperand(addr, "boolean")
        pass

    @_('varcomp')
    def varcall(self, x):
        if x[-1] is None:
            name = x[-2]
        else:
            name = x[-1]
        var = self.verifyVarExists(name, x)

        if var is not None and var[2] is None:
            self.quads.addOperand(var[0], var[1])
        pass

    def calcR(self, dimensions: list) -> int:
        r = 1
        for dim in dimensions:
            r = dim * r
        return r

    def verifyVarExists(self, name, str, x):
        found = False
        i_scope = len(self.program.getScope()) - 1

        while i_scope >= 0 and found is False:
            if name is None:
                found = True
            else:
                scope = self.program.getScope()[i_scope]
                current_prog = self.program.getProg(scope)
                var = self.verifyVarInF(current_prog["directory_func"], name)

                if var is None:
                    dVars = current_prog["directory_vars"]
                    var = self.verifyVTable(dVars, name)
                if var is not None:
                    found = True
                    if self.verifyVarInF(name, current_prog):
                        if var[1] == "void":
                            sys.exit(f"Expression cannot be a void function")
                    else:
                        return var
                else:
                    i_scope = i_scope - 1
        if i_scope < 0 and found is False:
            sys.exit(f"Declaration of variable {name} was not found")

    def verifyVarInF(self, name: str, prog) -> bool:
        if name in prog["directory_func"].getDirectory():
            return True
        else:
            return False

    def verifyVarEF(self, dirF: Directory_Func, name: str) -> tuple:
        i_scope = len(dirF.getScope()) - 1
        while i_scope >= 0:
            fScope = dirF.getScope()[i_scope]
            cFunc = dirF.getFunc(fScope)
            var = self.verifyVTable(cFunc["directory_vars"], name)
            if var is not None:
                return var
            else:
                var = self.verifyVTable(cFunc["params"], name)
                if var is not None:
                    return var
            i_scope = i_scope - 1
        return None

    def verifyVTable(self, dirV: Directory_Vars, name: str) -> tuple:
        if name in dirV.getDirectory():
            var = dirV.getVar(name)
            return var["address"], var["type"], var["dims"]
        else:
            return None

    def verifyFD(self, fDir: dict, name: str):
        if name in fDir:
            return fDir[name]

    def createEra(self, name: str, func: dict):
        self.quads.addOperand(name, "")
        self.quads.addOperator("era")
        params = func["params"].getDirectory()

        for param in params:
            self.call_params.append(params[param])

    def generateSD(self, name: str, x):
        var = self.verifyVarExists(name, x)
        self.quads.addOperand(var[2][0], "int")
        self.quads.addOperator("arrsd")
        pass

    def generateSDS(self, name: str):
        self.quads.addOperator("arrsds")