class Delimitation:
 
    # Number of spaces available for each delimitation
    area = 100

    # Dictionary that calculates the amount of space for each type within a certain scope

    territories = {
        # Integers
        "global_integers": 0 * area,
        "local_integers": 1 * area,
        "constant_integers": 2 * area,
        
        # Floats
        "global_floats": 3 * area,
        "local_floats": 4 * area, 
        "constant_floats": 5 * area,

        # Strings
        "global_strings": 6 * area,
        "local_strings": 7 * area,
        "constant_strings": 8 * area,

        # Booleans
        "global_booleans": 9 * area,
        "local_booleans": 10 * area
    }

    # Dictionary that counts the number of variables that have been created for each type
    # within a certain scope

    counter = {
        # Integers
        "global_integers": 0,
        "local_integers": 0,
        "constant_integers": 0,
        
        # Floats
        "global_floats": 0,
        "local_floats": 0, 
        "constant_floats": 0,

        # Strings
        "global_strings": 0,
        "local_strings": 0,
        "constant_strings": 0,

        # Booleans
        "global_booleans": 0,
        "local_booleans": 0
    }

    def getAddr(self, scope_type: str) -> int:
        return self.territories[scope_type]

    def updateCounter(self, scope_type: str, delta: int = 1):
        self.counter[scope_type] = self.counter[scope_type] + delta

    def getCounter(self, scope_type: str) -> int:
        return self.counter[scope_type]

    def verifyDelimitation(self, addr: int, scope_type: str):
        if addr >= self.territories[scope_type] and addr < self.territories[scope_type] + self.area:
            pass
        else:
            # QUIT PROGRAM DUE TO ERROR OFF MEMORY LIMITS
            pass
    
    def getGVarsCounter(self) -> dict:

        integers = self.counter["global_integers"]
        floats = self.counter["global_floats"]
        strings = self.counter["global_strings"]
        booleans = self.counter["global_booleans"]

        GVCounter = {
            "integers": integers,
            "floats": floats,
            "string": strings,
            "booleans": booleans
        }
        return GVCounter

    def getLVarsCounter(self) -> dict:

        integers = self.counter["local_integers"]
        floats = self.counter["local_floats"]
        strings = self.counter["local_strings"]
        booleans = self.counter["local_booleans"]

        LVCounter = {
            "integers": integers,
            "floats": floats,
            "string": strings,
            "booleans": booleans
        }
        return LVCounter