from Sly.lexer import ShintoLexer
from Sly.parser import ShintoParser

if __name__ == '__main__':
        S_lexer = ShintoLexer()
        S_parser = ShintoParser()

        #res = self.parse(S_lexer.tokenize(text))
        #print(res)

        while True:
            try:
                text = input('Shinto > ')
                res = S_parser.parse(S_lexer.tokenize(text))
                print(res)
            except EOFError:
                break
