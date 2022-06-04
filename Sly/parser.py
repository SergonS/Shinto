import operator
from sly import Parser
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

    @_('PROG ID check_program ";" gvars store_gvars functions main')
    def program(self, x):
        print(self.stack_gvars)
        self.dir_vars.showDirectory()
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

    @_('datatype FUNC ID "(" params ")" "{" vars statement "}" functions')
    def functions(self, x):
        self.storeLocalVars(x[2])
        pass

    # PARAMS

    @_('')
    def params(self, x):
        pass

    # MAIN

    @_('FUNC MAIN "(" ")" "{" vars statement "}" store_main')
    def main(self, x):
        self.storeLocalVars("main")
        pass


    @_('')
    def statement(self, x):
        pass

    """
    @_('FOR var_assign TO expr THEN statement')
    def statement(self, x):
        return ('for_loop', ('for_loop_setup', x.var_assign, x.expr), x.statement)

    @_('IF condition THEN statement ELSE statement')
    def statement(self, x):
        return ('if_stmt', x.condition, ('branch', x.statementA, x.statementB))

    @_('FUNC ID "(" ")" ARROW statement')
    def statement(self, x):
        return ('fun_def', x.ID, x.statement)

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

    # Variable Assignment

    
    @_('ID "=" expr')
    def var_assign(self, x):
        return ('var_assign', x.ID, x.expr)

    @_('ID "=" STRING')
    def var_assign(self, x):
        return ('var_assign', x.ID, x.STRING)

    """

    @_('expr')
    def statement(self, x):
        return (x.expr)
    
    # EXPR

    @_('expr "+" term')
    def expr(self, x):
        self.storeOperation("+")
        return ('add', x.expr, x.term)

    @_('expr "-" term')
    def expr(self, x):
        self.storeOperation("-")
        return ('sub', x.expr, x.term)

    @_('term')
    def expr(self, x):
        return x.term

    # TERM

    @_('term "*" factor')
    def term(self, x):
        self.storeOperation("*")
        return ('mul', x.term, x.factor)

    @_('term "/" factor')
    def term(self, x):
        self.storeOperation("/")
        return ('div', x.term, x.factor)

    @_('factor')
    def term(self, x):
        return x.factor

    # FACTOR

    @_('"(" expr ")"')
    def factor(self, x):
        return x.expr

    @_('TRUE')
    def factor(self, x):
        return ('boolean', x.TRUE)

    @_('FALSE')
    def factor(self, x):
        return ('boolean', x.FALSE)

    @_('ID')
    def factor(self, x):
        return x.ID

    @_('INT')
    def factor(self, x):
        self.storeConstant("int", str(x.INT))
        return ('int', x.INT)

    @_('FLOAT')
    def factor(self, x):
        return ('float', x.FLOAT)

        

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
        self.dir_functions.addFunc("main", "void")
        pass

    @_('')
    def check_program(self, x):
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
                        self.dir_vars.appendToDirectory(var, dt, "", addr, 0, 0, "global")

                elif dt == "float":
                    addr = self.delimitation.getAddr("global_float") + self.delimitation.getCounter("global_float")
                    self.delimitation.verifyDelimitation(addr, "global_float")

                    if self.globals.addFloat(var, addr) == True:
                        self.delimitation.updateCounter("global_float")
                        self.dir_vars.appendToDirectory(var, dt, "", addr, 0, 0, "global")

                elif dt == "string":
                    addr = self.delimitation.getAddr("global_string") + self.delimitation.getCounter("global_string")
                    self.delimitation.verifyDelimitation(addr, "global_string")

                    if self.globals.addString(var, addr) == True:
                        self.delimitation.updateCounter("global_string")
                        self.dir_vars.appendToDirectory(var, dt, "", addr, 0, 0, "global")

                elif dt == "bool":
                    addr = self.delimitation.getAddr("global_bool") + self.delimitation.getCounter("global_bool")
                    self.delimitation.verifyDelimitation(addr, "global_bool")

                    if self.globals.addBoolean(var, addr) == True:
                        self.delimitation.updateCounter("global_bool")
                        self.dir_vars.appendToDirectory(var, dt, "", addr, 0, 0, "global")
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
                        self.dir_vars.appendToDirectory(var, dt, "", addr, 0, 0, scope)

                elif dt == "float":
                    addr = self.delimitation.getAddr("local_float") + self.delimitation.getCounter("local_float")
                    self.delimitation.verifyDelimitation(addr, "local_float")

                    if self.locals.addFloat(var, addr) == True:
                        self.delimitation.updateCounter("local_float")
                        self.dir_vars.appendToDirectory(var, dt, "", addr, 0, 0, scope)

                elif dt == "string":
                    addr = self.delimitation.getAddr("local_string") + self.delimitation.getCounter("local_string")
                    self.delimitation.verifyDelimitation(addr, "local_string")

                    if self.locals.addString(var, addr) == True:
                        self.delimitation.updateCounter("local_string")
                        self.dir_vars.appendToDirectory(var, dt, "", addr, 0, 0, scope)

                elif dt == "bool":
                    addr = self.delimitation.getAddr("local_bool") + self.delimitation.getCounter("local_bool")
                    self.delimitation.verifyDelimitation(addr, "local_bool")

                    if self.locals.addBoolean(var, addr) == True:
                        self.delimitation.updateCounter("local_bool")
                        self.dir_vars.appendToDirectory(var, dt, "", addr, 0, 0, scope)
        self.stack_vars.clear()
        

    def storeOperation(self, operator: str):
        print("Operator " + operator + " added")
        self.quads.addOperator(operator)

    def storeConstant(self, dt_constant: str, val_constant: str):
        if dt_constant == "int":
            addr = self.delimitation.getAddr("constant_int") + self.delimitation.getCounter("constant_int")
            self.delimitation.verifyDelimitation(addr, "constant_int")

            if self.constants.addInteger(val_constant, addr) == True:
                self.delimitation.updateCounter("constant_int")

        elif dt_constant == "float":
            addr = self.delimitation.getAddr("constant_float") + self.delimitation.getCounter("constant_float")
            self.delimitation.verifyDelimitation(addr, "constant_float")

            if self.constants.addFloat(val_constant, addr) == True:
                self.delimitation.updateCounter("constant_float")

        elif dt_constant == "string":
            addr = self.delimitation.getAddr("constant_string") + self.delimitation.getCounter("constant_string")
            self.delimitation.verifyDelimitation(addr, "constant_string")

            if self.constants.addString(val_constant, addr) == True:
                self.delimitation.updateCounter("constant_string")

        self.quads.addOperand(addr, dt_constant)
