from Sly.lexer import ShintoLexer
from Sly.parser import ShintoParser

if __name__ == '__main__':
        S_lexer = ShintoLexer()
        S_parser = ShintoParser()

        # To get Tokens ONLY
        #res = self.parse(S_lexer.tokenize(text))
        #print(res)
        # To read from input

        """
        while True:
            try:
                text = input('Shinto > ')
                res = S_parser.parse(S_lexer.tokenize(text))
                print(res)
            except EOFError:
                break
        """

        # To read from file
        f_name = "script.txt"
        file = open(f_name, 'r') 
        f = file.read()

        res = S_parser.parse(S_lexer.tokenize(f))

        S_parser.quads.printQuads()
        #S_parser.constants.printCTable()
        
        #print(S_parser.quads.polish_vector)

        #print(res)


        
