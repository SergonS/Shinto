from VM.Delimitations import Delimitation

class L_Table:
    delimitation = Delimitation().area

    l_integers = {}
    l_floats = {}
    l_strings = {}
    l_booleans = {}

    def addInteger(self, value: str, addr: int) -> bool:
        if value not in self.l_integers:
            self.l_integers[value] = addr
            return True
        else:
            return False

    def getInteger(self, value: str) -> int:
        return self.l_integers[value]

    def addFloat(self, value: str, addr: int) -> bool:
        if value not in self.l_floats:
            self.l_floats[value] = addr
            return True
        else:
            return False

    def getFloat(self, value: str) -> int:
        return self.l_floats[value]

    def addString(self, value: str, addr: int) -> bool:
        if value not in self.l_strings:
            self.l_strings[value] = addr
            return True
        else:
            return False

    def getString(self, value: str) -> int:
        return self.l_strings[value]

    def addBoolean(self, value: str, addr: int) -> bool:
        if value not in self.l_booleans:
            self.l_booleans[value] = addr
            return True
        else:
            return False

    def getBoolean(self, value: str) -> bool:
        return self.l_booleans[value]

    def getLTable(self) -> dict:
        table = {
            "integer": self.l_integers,
            "float": self.l_floats,
            "string": self.l_strings,
            "boolean": self.l_booleans
        }
        return table