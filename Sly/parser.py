from sly import Parser
from Sly.lexer import ShintoLexer
from Pillars.Directory_Functions import Directory_Func
from Pillars.Directory_Variables import Directory_Vars
from Pillars.QuadManager import QuadOverseer
from Pillars.Constants import C_Table
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

    call_params = []
    counter_params = 0
    counter = 0

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),           
    )

    constants = C_Table()
    quads = QuadOverseer()
    delimitation = Delimitation()

    # PROGRAM
    

    # Statements

    @_('')
    def statement(self, x):
        pass

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

    @_('expr')
    def statement(self, x):
        return (x.expr)

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

    @_('expr "+" expr')
    def expr(self, x):
        return ('add', x.expr0, x.expr1)

    @_('expr "-" expr')
    def expr(self, x):
        return ('sub', x.expr0, x.expr1)

    @_('expr "*" expr')
    def expr(self, x):
        return ('mul', x.expr0, x.expr1)

    @_('expr "/" expr')
    def expr(self, x):
        return ('div', x.expr0, x.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, x):
        return x.expr

    @_('ID')
    def expr(self, x):
        return ('var', x.ID)

    @_('INT')
    def expr(self, x):
        return ('int', x.INT)

    @_('FLOAT')
    def expr(self, x):
        return ('float', x.FLOAT)

