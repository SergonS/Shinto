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
        'FUNC',               # func
        'ID',
        'INT',
        'FLOAT',
        'STRING',
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

    ignore = '\t'

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
    FUNC = r'function'
    IF = r'if'
    THEN = r'then'
    ELSE = r'else'
    FOR = r'for'
    TO = r'to'
    WHILE = r'while'
    ARROW = r'->'
    ID = r'[a-zA-Z_][a-zA-Z_0-9]*'

    EQEQ = r'=='
    GOETHAN = r'>='
    LOETHAN = r'<='
    DIFF = r'!='
    AND = r'&&'
    OR = r'\|\|'

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

    @_(r'//.*')
    def COMMENT(self, t):
        pass

    @_(r' ')
    def space(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')
