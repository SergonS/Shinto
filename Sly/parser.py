import sys
from sly import Parser
from Pillars.Data_Types import Data_Type
from Pillars.Functions import Function
from Pillars.Variables import Variable
from Pillars.Locals import L_Table
from Sly.lexer import ShintoLexer
from Pillars.Directory_Functions import Directory_Func
from Pillars.Directory_Variables import Directory_Vars
from Pillars.QuadManager import QuadOverseer
from Pillars.Constants import C_Table
from Pillars.Globals import G_Table
from VM.Delimitations import Delimitation

### PARSER ###

"""

    Parser that assures valid structure of the input code

"""

class ShintoParser(Parser):
    debugfile = 'parser.out'
    tokens = ShintoLexer.tokens
    ERROR_FLAG = False
    stack_dim = []
    stack_params = []
    stack_vars = []
    stack_gvars = []

    call_params = []
    counter_params = 0
    counter_temp = 0
    counter = 0

    

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/')
    )

    globals = G_Table()
    locals = L_Table()
    constants = C_Table()
    quads = QuadOverseer()
    delimitation = Delimitation()
    dir_functions = Directory_Func()
    dir_vars = Directory_Vars()

    def __init__(self):
        self.scope = "global"
        

    # PROGRAM

    @_('PROG ID check_program ";" gvars store_gvars functions gvars store_gvars main')
    def program(self, x):
        print("VARIABLES DIR:")
        self.dir_vars.showDirectory()
        print()
        print("FUNCTIONS DIR:")
        self.dir_functions.showDirectory()
        print()
        print(self.quads.polish_vector)
        self.quads.addQuad("end", (), (), ())
        pass

    def parseData(self) -> dict:
        data = {
            "Globals": self.globals.getGTable(),
            "Constants": self.constants.getCTable(),
            "Locals": self.locals.getLTable(),
            "Quadruples": self.quads.getQuads()
        }
        return data

    # GLOBAL VARS

    @_('')
    def gvars(self, x):
        pass

    @_('VAR datatype gvarids store_gtype ";" gvars')
    def gvars(self, x):
        pass

    # GVARIDS
    @_('ID "," gvarids')
    def gvarids(self, x):
        self.stack_gvars.append(x[0])
        pass

    @_('ID')
    def gvarids(self, x):
        self.stack_gvars.append(x[0])
        pass

    @_('')
    def store_gvars(self, x):
        if len(self.stack_gvars) > 0:
            self.storeGlobalVars()
        pass
    
    @_('')
    def store_gtype(self, x):
        self.stack_gvars.append(x[-2])
        pass

    # LOCAL VARS

    @_('')
    def vars(self, x):
        pass

    @_('VAR datatype varids store_type ";" vars')
    def vars(self, x):
        pass

    # VARIDS
    @_('ID "," varids')
    def varids(self, x):
        self.stack_vars.append(x[0])
        pass

    @_('ID')
    def varids(self, x):
        self.stack_vars.append(x[0])
        pass

    @_('')
    def store_type(self, x):
        self.stack_vars.append(x[-2])
        pass

    # FUNCTIONS

    @_('')
    def functions(self, x):
        pass

    @_('datatype FUNC ID "(" params ")" store_funcv store_params store_init_quad  "{" vars store_local_vars funcontent "}" close_func functions')
    def functions(self, x):
        pass

    @_('statement funcontent')
    def funcontent(self, x):
        pass

    @_('')
    def funcontent(self, x):
        pass

    # PARAMS

    @_('')
    def params(self, x):
        pass

    @_('ID ":" datatype')
    def params(self, x):
        self.stack_params.append((x[0], x[2]))
        pass

    @_('ID  ":" datatype "," params')
    def params(self, x):
        self.stack_params.append((x[0], x[2]))
        pass

    # MAIN

    @_('FUNC MAIN "(" ")" store_funcm "{" vars store_mainv maincontent "}" ')
    def main(self, x):
        pass

    @_('statement maincontent')
    def maincontent(self, x):
        pass

    @_('')
    def maincontent(self, x):
        pass

    # STATEMENTS

    @_('statement statement')
    def statement(self, x):
        pass

    @_('')
    def statement(self, x):
        pass

    @_('var_assign unload_pv')
    def statement(self, x):
        pass

    @_('expr ";"')
    def statement(self, x):
        pass

    @_('returns unload_pv ";"')
    def statement(self, x):
        pass
    
    @_('ifelse unload_pv')
    def statement(self, x):
        pass

    @_('output unload_pv')
    def statement(self, x):
        pass

    @_('input unload_pv')
    def statement(self, x):
        pass

    @_('loop unload_pv')
    def statement(self, x):
        pass

    # VAR ASSIGN
    
    @_('ID store_oper "=" expr ";"')
    def var_assign(self, x):
        self.storeOperation("=")
        pass
    
    @_('RETURN expr store_rquad')
    def returns(self, x):
        pass

    #IFELSE

    @_('IF "(" expr ")" store_gotof "{" ifelsecont "}" ELSE store_goto "{" ifelsecont "}" store_endif')
    def ifelse(self, x):
        pass

    @_('IF "(" expr ")" store_gotof "{" ifelsecont "}" store_endif')
    def ifelse(self, x):
        pass

    @_('statement ifelsecont')
    def ifelsecont(self, x):
        pass

    @_('')
    def ifelsecont(self, x):
        pass

    # OUTPUT

    @_('OUTPUT "(" expr outex ")" ";"')
    def output(self, x):
        self.storeOperation("output")
        pass

    @_('"," expr outex')
    def outex(self, x):
        self.storeOperation("output")
        pass

    @_('')
    def outex(self, x):
        pass

    # INPUT 

    @_('INPUT "(" ID store_oper ")" ";"')
    def input(self, x):
        self.storeOperation("input")
        pass

    # LOOP
    @_('WHILE store_jump "(" expr ")" store_gotof "{" statement "}" end_loop')
    def loop(self, x):
        pass

    # EXPR

    @_('arexp exprx')
    def expr(self, x):
        pass

    @_('exprop arexp')
    def exprx(self, x):
        print("x[0] at exprop")
        print(x[0])
        self.quads.addOperator(x[0])
        pass

    @_('')
    def exprx(self, x):
        pass

    @_('GOETHAN')
    def exprop(self, x):
        return (">=")

    @_('">"')
    def exprop(self, x):
        return (">")

    @_('LOETHAN')
    def exprop(self, x):
        return ("<=")

    @_('"<"')
    def exprop(self, x):
        return ("<")

    @_('AND')
    def exprop(self, x):
        return ("&&")

    @_('DIFF')
    def exprop(self, x):
        return ("!=")

    @_('EQEQ')
    def exprop(self, x):
        return ("==")

    @_('OR')
    def exprop(self, x):
        return ("||")

    # AREXP

    @_('term')
    def arexp(self, x):
        pass

    @_('term arexpextra')
    def arexp(self, x):
        pass

    @_('"+" term arexpextra')
    def arexpextra(self, x):
        self.storeOperation("+")
        pass

    @_('"-" term arexpextra')
    def arexpextra(self, x):
        self.storeOperation("-")
        pass

    @_('')
    def arexpextra(self, x):
        pass

    # TERM

    @_('factor')
    def term(self, x):
        pass

    @_('factor termx')
    def term(self, x):
        pass

    @_('"*" factor termx')
    def termx(self, x):
        self.storeOperation("*")

    @_('"/" factor termx')
    def termx(self, x):
        self.storeOperation("/")

    @_('')
    def termx(self, x):
        pass

    # FACTOR

    @_('"(" store_op expr ")" store_op')
    def factor(self, x):
        pass

    @_('element')
    def factor(self, x):
        pass

    # ELEMENT

    @_('const store_const')
    def element(self, x):
        pass

    @_('compound store_oper')
    def element(self, x):
        pass

    @_('compoundx')
    def compound(self, x):
        pass

    @_('ID store_oper')
    def compoundx(self, x):
        pass
    
    @_('callfunc store_oper')
    def element(self, x):
        pass
    
    # CONST

    @_('TRUE')
    def const(self, x):
        return ('boolean', x.TRUE)

    @_('FALSE')
    def const(self, x):
        return ('boolean', x.FALSE)

    @_('INT')
    def const(self, x):
        return ('int', x.INT)

    @_('FLOAT')
    def const(self, x):
        return ('float', x.FLOAT)

    @_('STRING')
    def string(self, x):
        return ('string', x.STRING)

    # CALLFUNC
    
    @_('ID verify_func add_fstack "(" callfuncpar ver_params ")" end_fstack store_gosub')
    def callfunc(self, x):
        pass

    @_('expr store_pquad callfuncparx')
    def callfuncpar(self, x):
        pass

    @_('')
    def callfuncpar(self, x):
        pass

    @_('"," callfuncpar')
    def callfuncparx(self, x):
        pass

    @_('')
    def callfuncparx(self, x):
        pass
    

    """
    @_('')
    def xexpr(self, x):
        pass

    @_('"," expr')
    def xexpr(self, x):
        pass
    """
    # DATA TYPE

    @_('D_INT')
    def datatype(self, x):
        return "int"

    @_('D_FLOAT')
    def datatype(self, x):
        return "float"

    @_('D_STRING')
    def datatype(self, x):
        return "string"

    @_('D_BOOL')
    def datatype(self, x):
        return "boolean"

    

    ### Neuralgic Points

    @_('')
    def check_program(self, x):
        self.scope = "global"
        pass

    @_('')
    def store_init_quad(self, x):
        self.dir_functions.getFunc(x[-6]).addIQuad(len(self.quads.getQuads()))
        pass

    @_('')
    def store_funcm(self, x):
        self.scope = "main"
        func = self.createFunction("main", "void")
        func.addIQuad(len(self.quads.getQuads()) + 1)

        addr = self.delimitation.getAddr("global_int") + self.delimitation.getCounter("global_int")
        self.delimitation.verifyDelimitation(addr, "global_int")
        self.delimitation.updateCounter("global_int")
        self.dir_vars.appendToDirectory("main", "void", addr, 0, 0, "global")
        func.addr = addr

        self.dir_functions.addFunc(func)

    @_('')
    def store_funcv(self, x):
        #[-5] name
        #[-7] data_type
        dt = x[-6]
        name = x[-4]
        self.scope = name

        if dt == "int":
            addr = self.delimitation.getAddr("global_int") + self.delimitation.getCounter("global_int")
            self.delimitation.verifyDelimitation(addr, "global_int")

            if self.globals.addInteger(name, addr) == True:
                self.delimitation.updateCounter("global_int")
                self.dir_vars.appendToDirectory(name, dt, addr, 0, 0, "global")

        elif dt == "float":
            addr = self.delimitation.getAddr("global_float") + self.delimitation.getCounter("global_float")
            self.delimitation.verifyDelimitation(addr, "global_float")

            if self.globals.addFloat(name, addr) == True:
                self.delimitation.updateCounter("global_float")
                self.dir_vars.appendToDirectory(name, dt, addr, 0, 0, "global")

        elif dt == "string":
            addr = self.delimitation.getAddr("global_string") + self.delimitation.getCounter("global_string")
            self.delimitation.verifyDelimitation(addr, "global_string")

            if self.globals.addString(name, addr) == True:
                self.delimitation.updateCounter("global_string")
                self.dir_vars.appendToDirectory(name, dt, addr, 0, 0, "global")

        elif dt == "boolean":
            addr = self.delimitation.getAddr("global_boolean") + self.delimitation.getCounter("global_boolean")
            self.delimitation.verifyDelimitation(addr, "global_boolean")

            if self.globals.addBoolean(name, addr) == True:
                self.delimitation.updateCounter("global_boolean")
                self.dir_vars.appendToDirectory(name, dt, addr, 0, 0, "global")
        func = self.createFunction(name, dt)
        func.addr = addr

        self.dir_functions.addFunc(func)

    @_('')
    def store_params(self, x):
        if len(self.stack_params) > 0:
            self.storeParams(x[-5])
        pass

    @_('')
    def store_local_vars(self, x):
        if len(self.stack_vars) > 0:
            self.storeLocalVars(x[-9])
        pass

    @_('')
    def store_mainv(self, x):
        self.quads.finishGoto("goto")
        if len(self.stack_vars) > 0:
            self.storeLocalVars("main")

    @_('')
    def store_op(self, x):
        self.storeOperation(x[-1])
        pass
    
    @_('')
    def store_oper(self, x):
        if self.verifyVar(x[-1]):
            var = self.dir_vars.getVar(x[-1])
            print("STORING " + var.name + " IN POLISH VECTOR")

            if self.verifyFunc(x[-1]) == False:
                print(var.name + " NOT A FUNC")
                self.quads.addOperand(var.addr, var.data_type)
        pass

    @_('')
    def store_const(self, x):
        print("STORING CONSTANT:")
        print(x[-1])
        self.storeConstant(x[-1][0], x[-1][1])
        pass

    @_('')
    def unload_pv(self, x):
        self.quads.unloadPolishVector()
        pass

    @_('')
    def store_rquad(self, x):
        func = self.dir_functions.getFunc(self.scope)

        if func.data_type == "void":
            sys.exit(f'Function {self.scope} is of type void, it cannot have return')
        
        self.quads.addOperand(func.addr, func.data_type)
        #print(str(self.quads.polish_vector) + " at RETYURN")
        self.quads.addOperator("return")
        self.quads.addOperator("endfunc")

        func.returnVar = True
        pass

    @_('')
    def close_func(self, x):
        pass

    @_('')
    def store_endif(self, x):
        self.quads.finishGoto("gotof")
        pass

    @_('')
    def store_pquad(self, x):
        self.quads.unloadPolishVector()

        if self.counter_params < len(self.call_params):
            self.quads.addOperand(self.call_params[self.counter_params].addr, self.call_params[self.counter_params].data_type)
            self.quads.addOperator("params")
            self.counter_params = self.counter_params + 1
        else:
            sys.exit(f'Different number of arguments between call function and the actual function')
        pass

    @_('')
    def ver_params(self, x):
        if self.counter_params < len(self.call_params):
            sys.exit(f'Missing arguments for called function')
        pass

    @_('')
    def verify_func(self, x):
        if self.verifyFunc(x[-1]) == False:
            sys.exit(f'Error: Function {x[-1]} called at line {x.lineno} not previously declared')
        self.createEra(x[-1], self.dir_functions.getFunc(x[-1]))
        pass

    @_('')
    def add_fstack(self, x):
        self.quads.addOperator("(")
        pass

    @_('')
    def end_fstack(self, x):
        self.quads.addOperator(")")
        pass

    @_('')
    def store_gosub(self, x):
        func = self.dir_functions.getFunc(x[-8])

        self.quads.addOperand(func.initQuad, func.name)
        self.quads.addOperator("gosub")

        if func.returnVar:
            var = self.dir_vars.getVar(func.name)

            self.quads.addOperand(var.addr, var.data_type)
            self.quads.addOperator("assignr")
        pass

    @_('')
    def store_gotof(self, x):
        print("STORING GOTOF")
        self.quads.addOperator("gotof")
        pass

    @_('')
    def store_goto(self, x):
        self.quads.finishGoto("goto")
        self.quads.addOperator("goto")
        pass
 
    @_('')
    def store_jump(self, x):
        self.quads.addJump()
        pass

    @_('')
    def end_loop(self, x):
        self.quads.addOperator("gotow")
        pass

    ### Auxiliary Functions

    def storeGlobalVars(self):
        dt = "none"
        for var in reversed(self.stack_gvars):
            if var == "int" or var == "float" or var == "string" or var == "boolean":
                dt = var
            else:
                if dt == "int":
                    addr = self.delimitation.getAddr("global_int") + self.delimitation.getCounter("global_int")
                    self.delimitation.verifyDelimitation(addr, "global_int")

                    if self.globals.addInteger(var, addr) == True:
                        self.delimitation.updateCounter("global_int")
                        self.dir_vars.appendToDirectory(var, dt, addr, 0, 0, "global")

                elif dt == "float":
                    addr = self.delimitation.getAddr("global_float") + self.delimitation.getCounter("global_float")
                    self.delimitation.verifyDelimitation(addr, "global_float")

                    if self.globals.addFloat(var, addr) == True:
                        self.delimitation.updateCounter("global_float")
                        self.dir_vars.appendToDirectory(var, dt, addr, 0, 0, "global")

                elif dt == "string":
                    addr = self.delimitation.getAddr("global_string") + self.delimitation.getCounter("global_string")
                    self.delimitation.verifyDelimitation(addr, "global_string")

                    if self.globals.addString(var, addr) == True:
                        self.delimitation.updateCounter("global_string")
                        self.dir_vars.appendToDirectory(var, dt, addr, 0, 0, "global")

                elif dt == "boolean":
                    addr = self.delimitation.getAddr("global_boolean") + self.delimitation.getCounter("global_boolean")
                    self.delimitation.verifyDelimitation(addr, "global_boolean")

                    if self.globals.addBoolean(var, addr) == True:
                        self.delimitation.updateCounter("global_boolean")
                        self.dir_vars.appendToDirectory(var, dt, addr, 0, 0, "global")
        self.stack_gvars.clear
                    
    def storeLocalVars(self, scope: str):
        dt = "none"
        for var in reversed(self.stack_vars):
            if var == "int" or var == "float" or var == "string" or var == "boolean":
                dt = var
            else:
                if dt == "int":
                    addr = self.delimitation.getAddr("local_int") + self.delimitation.getCounter("local_int")
                    self.delimitation.verifyDelimitation(addr, "local_int")

                    if self.locals.addInteger(var, addr) == True:
                        self.delimitation.updateCounter("local_int")
                        self.dir_vars.appendToDirectory(var, dt, addr, 0, 0, scope)

                elif dt == "float":
                    addr = self.delimitation.getAddr("local_float") + self.delimitation.getCounter("local_float")
                    self.delimitation.verifyDelimitation(addr, "local_float")

                    if self.locals.addFloat(var, addr) == True:
                        self.delimitation.updateCounter("local_float")
                        self.dir_vars.appendToDirectory(var, dt, addr, 0, 0, scope)

                elif dt == "string":
                    addr = self.delimitation.getAddr("local_string") + self.delimitation.getCounter("local_string")
                    self.delimitation.verifyDelimitation(addr, "local_string")

                    if self.locals.addString(var, addr) == True:
                        self.delimitation.updateCounter("local_string")
                        self.dir_vars.appendToDirectory(var, dt, addr, 0, 0, scope)

                elif dt == "boolean":
                    addr = self.delimitation.getAddr("local_boolean") + self.delimitation.getCounter("local_boolean")
                    self.delimitation.verifyDelimitation(addr, "local_boolean")

                    if self.locals.addBoolean(var, addr) == True:
                        self.delimitation.updateCounter("local_boolean")
                        self.dir_vars.appendToDirectory(var, dt, addr, 0, 0, scope)
                newVar = Variable(var, dt, addr, 0, 0, scope)
                self.dir_functions.getFunc(scope).addVar(newVar)
        self.stack_vars.clear()

    def storeParams(self, funcName: str):
        for vars in self.stack_params:
            var = vars[0]
            dt = vars[1]
            addr = -1
            if dt == "int":
                addr = self.delimitation.getAddr("local_int") + self.delimitation.getCounter("local_int")
                self.delimitation.verifyDelimitation(addr, "local_int")

                if self.locals.addInteger(var, addr) == True:
                    self.delimitation.updateCounter("local_int")
                    self.dir_vars.appendToDirectory(var, dt, addr, 0, 0, funcName)

            elif dt == "float":
                addr = self.delimitation.getAddr("local_float") + self.delimitation.getCounter("local_float")
                self.delimitation.verifyDelimitation(addr, "local_float")

                if self.locals.addFloat(var, addr) == True:
                    self.delimitation.updateCounter("local_float")
                    self.dir_vars.appendToDirectory(var, dt, addr, 0, 0, funcName)

            elif dt == "string":
                addr = self.delimitation.getAddr("local_string") + self.delimitation.getCounter("local_string")
                self.delimitation.verifyDelimitation(addr, "local_string")

                if self.locals.addString(var, addr) == True:
                    self.delimitation.updateCounter("local_string")
                    self.dir_vars.appendToDirectory(var, dt, addr, 0, 0, funcName)

            elif dt == "boolean":
                addr = self.delimitation.getAddr("local_boolean") + self.delimitation.getCounter("local_boolean")
                self.delimitation.verifyDelimitation(addr, "local_boolean")

                if self.locals.addBoolean(var, addr) == True:
                    self.delimitation.updateCounter("local_boolean")
                    self.dir_vars.appendToDirectory(var, dt, addr, 0, 0, funcName)
            newVar = Variable(var, dt, addr, 0, 0, funcName)
            self.dir_functions.showDirectory()
            self.dir_vars.appendToDirectory(var, dt, addr, 0, 0, funcName)
            self.dir_functions.getFunc(funcName).addParam(newVar)
        self.stack_params.clear()

    def createFunction(self, funcName: str, data_type: str) -> Function:
        func = Function(funcName, data_type)
        return func

    def createEra(self, name: str, function: Function):
        self.quads.addOperand(name, "")
        self.quads.addOperator("era")

        params = function.params

        for param in params:
            self.call_params.append(params[param])

    def storeOperation(self, operator: str):
        self.quads.addOperator(operator)

    def storeConstant(self, dt_constant: str, val_constant: str):
        if dt_constant == "int":
            addr = self.delimitation.getAddr("constant_int") + self.delimitation.getCounter("constant_int")
            self.delimitation.verifyDelimitation(addr, "constant_int")
            
            if self.constants.addInteger(val_constant, addr) == True:
                self.constants.addInteger(val_constant, addr)
                self.delimitation.updateCounter("constant_int")
                self.quads.addOperand(addr, "int")
            else:
                self.quads.addOperand(self.constants.getInteger(val_constant), "int")

        elif dt_constant == "float":
            addr = self.delimitation.getAddr("constant_float") + self.delimitation.getCounter("constant_float")
            self.delimitation.verifyDelimitation(addr, "constant_float")

            if self.constants.addFloat(val_constant, addr) == True:
                self.delimitation.updateCounter("constant_float")
                self.quads.addOperand(addr, "float")
            else:
                self.quads.addOperand(self.constants.getFloat(val_constant), "float")

        elif dt_constant == "string":
            addr = self.delimitation.getAddr("constant_string") + self.delimitation.getCounter("constant_string")
            self.delimitation.verifyDelimitation(addr, "constant_string")

            if self.constants.addString(val_constant, addr) == True:
                self.delimitation.updateCounter("constant_string")
                self.quads.addOperand(addr, "string")
            else:
                self.quads.addOperand(self.constants.getString(val_constant), "string")
        
        elif dt_constant == "boolean":
            addr = self.delimitation.getAddr("constant_boolean") + self.delimitation.getCounter("constant_boolean")
            self.delimitation.verifyDelimitation(addr, "constant_boolean")

            if self.constants.addBoolean(val_constant, addr) == True:
                self.delimitation.updateCounter("constant_boolean")
                self.quads.addOperand(addr, "boolean")
            else:
                self.quads.addOperand(self.constants.getBoolean(val_constant), "boolean")

    def verifyVar(self, var: str) -> bool:
        return self.dir_vars.hasVar(var)

    def verifyFunc(self, func: str) -> bool:
        return self.dir_functions.hasFunc(func)