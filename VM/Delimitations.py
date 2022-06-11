class Delimitation:
 
    # Number of spaces available for each delimitation
    area = 100

    # Dictionary that calculates the amount of space for each type within a certain scope

    territories = {
        # Integers
        "global_int": 0 * area,
        "local_int": 4 * area,
        "constant_int": 8 * area,
        
        # Floats
        "global_float": 1 * area,
        "local_float": 5 * area, 
        "constant_float": 9 * area,

        # Strings
        "global_string": 2 * area,
        "local_string": 6 * area,
        "constant_string": 10 * area,

        # Booleans
        "global_boolean": 3 * area,
        "local_boolean": 7 * area,
        "constant_boolean": 11 * area
    }

    # Dictionary that counts the number of variables that have been created for each type
    # within a certain scope

    counter = {
        # Integers
        "global_int": 0,
        "local_int": 0,
        "constant_int": 0,
        
        # Floats
        "global_float": 0,
        "local_float": 0, 
        "constant_float": 0,

        # Strings
        "global_string": 0,
        "local_string": 0,
        "constant_string": 0,

        # Booleans
        "global_boolean": 0,
        "local_boolean": 0,
        "constant_boolean": 0
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

        int = self.counter["global_int"]
        float = self.counter["global_float"]
        string = self.counter["global_string"]
        boolean = self.counter["global_boolean"]

        GVCounter = {
            "int": int,
            "float": float,
            "string": string,
            "boolean": boolean
        }
        return GVCounter

    def getLVarsCounter(self) -> dict:

        int = self.counter["local_int"]
        float = self.counter["local_float"]
        string = self.counter["local_string"]
        boolean = self.counter["local_boolean"]

        LVCounter = {
            "int": int,
            "float": float,
            "string": string,
            "boolean": boolean
        }
        return LVCounter