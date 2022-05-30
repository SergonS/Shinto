from VM.Delimitations import Delimitation

class C_Table:
    delimitation = Delimitation().area

    c_integers = {}
    c_floats = {}
    c_strings = {}


    def addInteger(self, value: str, addr: int) -> bool:
        if value not in self.c_integers:
            self.c_integers[value] = addr
            return True
        else:
            return False

    def getInteger(self, value: str) -> int:
        return self.c_integers[value]

    def addFloat(self, value: str, addr: int) -> bool:
        if value not in self.c_floats:
            self.c_floats[value] = addr
            return True
        else:
            return False

    def getFloat(self, value: str) -> int:
        return self.c_floats[value]

    def addString(self, value: str, addr: int) -> bool:
        if value not in self.c_strings:
            self.c_strings[value] = addr
            return True
        else:
            return False

    def getString(self, value: str) -> int:
        return self.c_strings[value]

    def getCTable(self) -> dict:
        table = {
            "integer": self.c_integers,
            "float": self.c_floats,
            "string": self.c_strings
        }
        return table

    def printCTable(self):
        print("Integers:")
        print(self.c_integers)
        print()
        print("Floats:")
        print(self.c_floats)
        print()
        print("Strings:")
        print(self.c_strings)
        print()