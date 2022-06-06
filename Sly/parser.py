import sys
from sly import Parser
from Pillars.Functions import Function
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
        print(self.quads.polish_vector)
        pass

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

    @_('VAR datatype varids store_type ";" ')
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

    @_('datatype FUNC ID "(" params store_params ")" store_funcv store_init_quad  "{" vars store_local_vars statement "}" functions')
    def functions(self, x):
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

    @_('FUNC MAIN "(" ")" "{" vars statement "}" store_main')
    def main(self, x):
        #self.dir_functions.addFunc("main", "void")
        if len(self.stack_vars) > 0:
            self.storeLocalVars("main")

        func = self.createFunction("main", "void")
        self.dir_functions.addFunc(func)
        pass

    # STATEMENTS

    @_('')
    def statement(self, x):
        pass

    @_('statement statement')
    def statement(self, x):
        pass

    
    @_('var_assign')
    def statement(self, x):
        pass

    @_('expr ";"')
    def statement(self, x):
        pass
    
    """
    # IF FUNCTION

    @_('IF "(" expr ")" store_gotof "{" statement "}" ELSE store_goto "{" statement "}" end_if')
    def statement(self, x):
        pass

    @_('IF "(" expr ")" store_gotof "{" statement "}" end_if')
    def statement(self, x):
        return ('if_stmt', x.condition, ('branch', x.statementA, x.statementB))
    """

    # VAR ASSIGN
    
    @_('ID store_oper "=" expr ";"')
    def var_assign(self, x):
        self.storeOperation("=")
        pass
    
    
    """
    @_('FOR var_assign TO expr THEN statement')
    def statement(self, x):
        return ('for_loop', ('for_loop_setup', x.var_assign, x.expr), x.statement)

    @_('IF condition THEN statement ELSE statement')
    def statement(self, x):
        return ('if_stmt', x.condition, ('branch', x.statementA, x.statementB))

    @_('ID "(" ")"')
    def statement(self, x):
        return ('fun_call', x.ID)
    
    @_('var_assign')
    def statement(self, x):
        return x.var_assign

    # Conditions

    @_('expr EQEQ expr')
    def condition(self, x):
        return ('condition_eqeq', x.expr0, x.expr1)

    """
    """
    @_('expr')
    def statement(self, x):
        return (x.expr)
    """
    
    # EXPR

    @_('arexp arexpx')
    def expr(self, x):
        pass

    @_('arexpxop store_op arexp')
    def arexpx(self, x):
        pass

    @_('')
    def arexpx(self, x):
        pass

    @_('GOETHAN')
    def arexpxop(self, x):
        pass

    @_('">"')
    def arexpxop(self, x):
        pass

    @_('LOETHAN')
    def arexpxop(self, x):
        pass

    @_('"<"')
    def arexpxop(self, x):
        pass

    @_('AND')
    def arexpxop(self, x):
        pass

    @_('DIFF')
    def arexpxop(self, x):
        pass

    @_('EQEQ')
    def arexpxop(self, x):
        pass

    @_('OR')
    def arexpxop(self, x):
        pass

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

    @_('"-" term arexpextra')
    def arexpextra(self, x):
        self.storeOperation("-")

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

    @_('"/" store_op factor termx')
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

    """
    @_('callfunc')
    def compound(self, x):
        pass
    """

    @_('ID')
    def compoundx(self, x):
        pass
    
    """
    @_('callfunc ";"')
    def element(self, x):
        pass
    """
    # CONST

    @_('TRUE store_const')
    def const(self, x):
        return ('boolean', x.TRUE)

    @_('FALSE store_const')
    def const(self, x):
        return ('bool', x.FALSE)

    @_('INT')
    def const(self, x):
        return ('int', x.INT)

    @_('FLOAT store_const')
    def factor(self, x):
        return ('float', x.FLOAT)

    # CALLFUNC
    """
    @_('ID verify_func add_fstack "(" expr xexpr ")" end_fstack store_gosub')
    def callfunc(self, x):
        pass

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
        return "bool"

    

    ### Neuralgic Points

    @_('')
    def store_main(self, x):
        self.quads.finishGoto("gotof")
        #self.dir_functions.addFunc("main", "void")
        pass

    @_('')
    def check_program(self, x):
        pass

    @_('')
    def store_init_quad(self, x):
        self.dir_functions.getFunc(x[-6]).addIQuad(len(self.quads.getQuads()))
        pass

    @_('')
    def store_funcv(self, x):
        #[-5] name
        #[-7] data_type
        dt = x[-7]
        name = x[-5]

        func = self.createFunction(name, dt)
        self.dir_functions.addFunc(func)

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

        elif dt == "bool":
            addr = self.delimitation.getAddr("global_bool") + self.delimitation.getCounter("global_bool")
            self.delimitation.verifyDelimitation(addr, "global_bool")

            if self.globals.addBoolean(name, addr) == True:
                self.delimitation.updateCounter("global_bool")
                self.dir_vars.appendToDirectory(name, dt, addr, 0, 0, "global")

    @_('')
    def store_params(self, x):
        if len(self.stack_params) > 0:
            self.storeParams(x[-3])
        pass

    @_('')
    def store_local_vars(self, x):
        if len(self.stack_vars) > 0:
            self.storeLocalVars(x[-7])
        pass

    @_('')
    def store_op(self, x):
        self.storeOperation(x[-1])
        pass
    
    @_('')
    def store_oper(self, x):
        if self.verifyVar(x[-1]):
            var = self.dir_vars.getVar(x[-1])

            if self.verifyFunc(x[-1]) == False:
                self.quads.addOperand(var.name, var.data_type)
        pass

    @_('')
    def store_const(self, x):
        self.storeConstant(x[-1][0], x[-1][1])
        pass

    @_('')
    def verify_func(self, x):
        if self.verifyFunc(x[-1]) == False:
            sys.exit(f'Error: Function {x[-1]} called at line {x.lineno} not previously declared')
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
        func = self.dir_functions.getFunc(x[8])
        self.quads.addOperand(func.initQuad, x[-8])
        self.quads.addOperator("gosub")

        if func.bReturn:
            var = self
        pass

    @_('')
    def store_gotof(self, x):
        self.quads.addOperator("gotof")
        pass

    @_('')
    def store_goto(self, x):
        self.quads.finishGoto("goto")
        self.quads.addOperator("goto")
        pass

    @_('')
    def end_if(self, x):
        self.quads.finishGoto("gotof")
        pass
 
    ### Auxiliary Functions

    def storeGlobalVars(self):
        dt = "none"
        for var in reversed(self.stack_gvars):
            if var == "int" or var == "float" or var == "string" or var == "bool":
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

                elif dt == "bool":
                    addr = self.delimitation.getAddr("global_bool") + self.delimitation.getCounter("global_bool")
                    self.delimitation.verifyDelimitation(addr, "global_bool")

                    if self.globals.addBoolean(var, addr) == True:
                        self.delimitation.updateCounter("global_bool")
                        self.dir_vars.appendToDirectory(var, dt, addr, 0, 0, "global")
        self.stack_gvars.clear
                    
    def storeLocalVars(self, scope: str):
        dt = "none"
        for var in reversed(self.stack_vars):
            if var == "int" or var == "float" or var == "string" or var == "bool":
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

                elif dt == "bool":
                    addr = self.delimitation.getAddr("local_bool") + self.delimitation.getCounter("local_bool")
                    self.delimitation.verifyDelimitation(addr, "local_bool")

                    if self.locals.addBoolean(var, addr) == True:
                        self.delimitation.updateCounter("local_bool")
                        self.dir_vars.appendToDirectory(var, dt, addr, 0, 0, scope)

        self.stack_vars.clear()

    def storeParams(self, funcName: str):
        for vars in self.stack_params:
            var = vars[0]
            dt = vars[1]
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

            elif dt == "bool":
                addr = self.delimitation.getAddr("local_bool") + self.delimitation.getCounter("local_bool")
                self.delimitation.verifyDelimitation(addr, "local_bool")

                if self.locals.addBoolean(var, addr) == True:
                    self.delimitation.updateCounter("local_bool")
                    self.dir_vars.appendToDirectory(var, dt, addr, 0, 0, funcName)

    def createFunction(self, funcName: str, data_type: str) -> Function:
        func = Function(funcName, data_type)
        
        if len(self.stack_params) > 0:
            for param in self.stack_params:
                func.addParam(self.dir_vars.getVar(param[0]))

        if len(self.stack_vars) > 0:
            for var in self.stack_params:
                func.addParam(self.dir_vars.getVar(var[0]))   

        # Reset params and vars stacks

        self.stack_params.clear()
        self.stack_vars.clear()

        return func

    def storeOperation(self, operator: str):
        self.quads.addOperator(operator)

    def storeConstant(self, dt_constant: str, val_constant: str):
        if dt_constant == "int":
            addr = self.delimitation.getAddr("constant_int") + self.delimitation.getCounter("constant_int")
            self.delimitation.verifyDelimitation(addr, "constant_int")
            
            print("VARIABLE ADDED TO CONSTANTS")
            self.constants.addInteger(val_constant, addr)
            self.delimitation.updateCounter("constant_int")
            self.quads.addOperand(addr, "int")

        elif dt_constant == "float":
            addr = self.delimitation.getAddr("constant_float") + self.delimitation.getCounter("constant_float")
            self.delimitation.verifyDelimitation(addr, "constant_float")

            if self.constants.addFloat(val_constant, addr) == True:
                self.delimitation.updateCounter("constant_float")
                self.quads.addOperand(addr, "float")

        elif dt_constant == "string":
            addr = self.delimitation.getAddr("constant_string") + self.delimitation.getCounter("constant_string")
            self.delimitation.verifyDelimitation(addr, "constant_string")

            if self.constants.addString(val_constant, addr) == True:
                self.delimitation.updateCounter("constant_string")
                self.quads.addOperand(addr, "string")
        
        elif dt_constant == "bool":
            addr = self.delimitation.getAddr("constant_bool") + self.delimitation.getCounter("constant_bool")
            self.delimitation.verifyDelimitation(addr, "constant_bool")

            if self.constants.addBoolean(val_constant, addr) == True:
                self.delimitation.updateCounter("constant_bool")
                self.quads.addOperand(addr, "bool")

    def verifyVar(self, var: str) -> bool:
        return self.dir_vars.hasVar(var)

    def verifyFunc(self, func: str) -> bool:
        return self.dir_functions.hasFunc(func)