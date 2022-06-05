from sly import Lexer

### LEXER ###

"""

    Lexer that identifies keywords and turns them into tokens with help of the SLY library


    ---

    Attributes

    tokens : 
        array of defined tokens

    ignore :
        ignore other characters that are not defined

    literals :
        identify single characters that are returned as they come

    ---

    Methods

    t_FLOAT(t)
        Returns a token of type FLOAT with a float value

    t_INT(t)
        Returns a token of type INT with a int value
    
    t_COMMENT()
        Ignores lines that start with "//"

    t_space()
        Ignores spaces

    t_newline(t)
        Updates the lineno attribute of the token
"""

class ShintoLexer(Lexer):

    tokens = {
        'PROG',
        'MAIN',
        'VAR',
        'FUNC',               # func
        'ID',
        'INT',
        'FLOAT',
        'STRING',
        'BOOL',
        'TRUE',
        'FALSE',
        'D_INT',
        'D_FLOAT',
        'D_STRING',
        'D_BOOL',
        'IF',                 # if
        'THEN',               # then
        'ELSE',               # else
        'FOR',                # for
        'TO',                 # to
        'WHILE',              # while
        'ARROW',              # arrow
        'COMMENT',            # //
        'EQEQ',               # ==
        'GOETHAN',          # >=          
        'LOETHAN',          # <=
        'DIFF',             # !=
        'AND',              # &&
        'OR'                # ||
    }

    reserved = {
        'program'       : 'PROGRAM',
        'main'          : 'MAIN',
        'var'           : 'VAR',
        'if'            : 'IF',
        'else'          : 'ELSE',
        'function'      : 'FUNC',
        'return'        : 'RETURN',
        'input'         : 'INPUT',
        'print'        : 'OUTPUT',
        'int'           : 'INT',
        'float'         : 'FLOAT',
        'string'        : 'STRING',
        'bool'          : 'BOOL',
        'while'         : 'WHILE'
    }

    ignore = '\t'

    ignore_newline = r'\n+'

    literals = { 
        '=', 
        '+', 
        '-', 
        '*', 
        '/', 
        '(', 
        ')', 
        ',', 
        ';', 
        '.', 
        ' ', 
        ':',
        '[',
        ']',
        '{',
        '}'
        }

    # Define keywords
    PROG = r'program'
    MAIN = r'main'
    VAR = r'var'
    FUNC = r'function'
    IF = r'if'
    THEN = r'then'
    ELSE = r'else'
    FOR = r'for'
    TO = r'to'
    WHILE = r'while'
    ARROW = r'->'

    EQEQ = r'=='
    GOETHAN = r'>='
    LOETHAN = r'<='
    DIFF = r'!='
    AND = r'&&'
    OR = r'\|\|'

    @_(r'int')
    def D_INT(self, t):
        t.value = str(t.value)
        return t

    @_(r'float')
    def D_FLOAT(self, t):
        t.value = str(t.value)
        return t

    @_(r'string')
    def D_STRING(self, t):
        t.value = str(t.value)
        return t

    @_(r'bool')
    def BOOL(self, t):
        t.value = str(t.value)
        return t

    @_(r'true')
    def TRUE(self, t):
        t.value = str(t.value)
        return t

    @_(r'false')
    def FALSE(self, t):
        t.value = str(t.value)
        return t

    @_(r'\".*?\"')
    def STRING(self, t):
        t.value = str(t.value)
        return t

    @_(r'\d+\.\d*')
    def FLOAT(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INT(self, t):
        t.value = int(t.value)
        return t

    @_(r'[a-zA-Z_][a-zA-Z_0-9]*')
    def ID(self, t):
        t.type = self.reserved.get(t.value, 'ID')
        return t

    @_(r'//.*')
    def COMMENT(self, t):
        pass

    @_(r' ')
    def space(self, t):
        pass

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # Compute column
    def find_column(text, token):
        last_cr = text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        column = (token.index - last_cr) + 1
        return column

    # Error handling rule
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1