from Sly.lexer import ShintoLexer
from Sly.parser import ShintoParser
from VM.VirtualMachine import VirtualMachine

if __name__ == '__main__':
        S_lexer = ShintoLexer()
        S_parser = ShintoParser()

        # To read from file
        f_name = "fibonacci.txt"
        file = open(f_name, 'r') 
        f = file.read()

        res = S_parser.parse(S_lexer.tokenize(f))
        S_parser.quads.printQuads()

        vm = VirtualMachine(S_parser.parseData(), S_parser.quads.counter_temps)
        


        
