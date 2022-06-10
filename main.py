from Sly.lexer import ShintoLexer
from Sly.parser import ShintoParser
from VM.VirtualMachine import VirtualMachine

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

        """
        for tok in S_lexer.tokenize(f):
            print('type=%r, value=%r' % (tok.type, tok.value))
        """
        res = S_parser.parse(S_lexer.tokenize(f))
        S_parser.quads.printQuads()
        print(S_parser.locals.getLTable())
        print("Temps: ")
        print(S_parser.quads.counter_temps)

        vm = VirtualMachine(S_parser.parseData(), S_parser.quads.counter_temps)
        
        vm.em.showMemory()
        
        

        #print(res)


        
