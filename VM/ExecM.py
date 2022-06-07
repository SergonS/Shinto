from Pillars.Directory_Functions import Directory_Func
from Pillars.Directory_Variables import Directory_Vars
from VM.Delimitations import Delimitation
import sys

class ExMemory:
    address = Delimitation().territories
    area = Delimitation().area
    # Store additional memory for functions
    extra_memory = []

    newEMemory = {
        address["local_int"]: [],
        address["local_float"]: [],
        address["local_string"]: [],
        address["local_bool"]: []
    }

    memory = {
        "global": {
            address["global_int"]: [],
            address["global_float"]: [],
            address["global_string"]: [],
            address["global_bool"]: []
        },
        "local": {
            address["local_int"]: [],
            address["local_float"]: [],
            address["local_string"]: [],
            address["local_bool"]: []
        },
        "constant": {
            address["constant_int"]: [],
            address["constant_float"]: [],
            address["constant_string"]: [],
            address["constant_bool"]: []
        }
    }

    # Convert the value in string notation to its corresponding data type
    def convertToConstType(self, data_type: str, var: str):
        data_type = data_type[:len(data_type) - 1]

        if data_type == "int":
            return int(var)
        elif data_type == "float":
            return float(var)
        elif data_type == "boolean" and not isinstance(var, int):
            if var == "false":
                return False
            elif var == "true":
                return True
            else:
                sys.exit(f"Expected a boolean")
        else:
            return var[1:-1]

    def convertToType(self, data_type: str, var: str):
        try:
            if data_type == "int":
                return int(var)
            elif data_type == "float":
                return float(var)
            elif data_type == "boolean" and not isinstance(var, int):
                if var == "false":
                    return False
                elif var == "true":
                    return True
                else:
                    sys.exit(f"Expected boolean")
            else:
                return var
        except ValueError:
            sys.exit(f"Invalid variable retrieved")

    # Initialize global memory with the memory needed
    def initializeGlobalMemory(self, globals: dict):
        self.memory["global"][self.address["global_int"]] = [None] * len(globals["int"])
        self.memory["global"][self.address["global_float"]] = [None] * len(globals["float"])
        self.memory["global"][self.address["global_string"]] = [None] * len(globals["string"])
        self.memory["global"][self.address["global_bool"]] = [None] * len(globals["boolean"])

    # Store const value in its corresponding address within the memory
    def storeConstValue(self, data_type: str, vars: dict):
        initial = self.address[data_type]

        for var in vars:
            space = vars[var] - initial
            self.memory["constant"][initial][space] = self.convertToConstType(data_type, var)

    # Initialize constant memory with the memory needed
    def initializeConstMemory(self, constants: dict):
        self.memory["constant"][self.address["constant_int"]] = [None] * len(constants["int"])
        self.memory["constant"][self.address["constant_float"]] = [None] * len(constants["float"])
        self.memory["constant"][self.address["constant_string"]] = [None] * len(constants["string"])
        self.memory["constant"][self.address["constant_bool"]] = [None] * len(constants["bool"])

    # Initialize local memory with the memory needed
    def initializeLocalMemory(self, locals: dict):
        self.newEMemory[self.address["local_int"]] = [None] * len(locals["int"])
        self.newEMemory[self.address["local_float"]] = [None] * len(locals["float"])
        self.newEMemory[self.address["local_string"]] = [None] * len(locals["string"])
        self.newEMemory[self.address["local_bool"]] = [None] * len(locals["bool"])

    # Copy the extra memory into the local memory in execution
    def setEMtoLM(self):
        self.memory["local"] = self.newEMemory.copy()

    def getLocalMemory(self):
        return self.memory["local"]

    # Save the local memory and instruction pointer to allow new local memory in its place
    def saveMemory(self, instructionPointer: int):
        info = {
            "memory": self.getLocalMemory().copy(),
            "instructionPointer": instructionPointer
        }
        self.extra_memory.append(info)

    def showMemory(self):
        print("Constant")
        print(self.memory["constant"])
        print("Global")
        print(self.memory["global"])
        print("Local")
        print(self.memory["local"])

    # Retrieve a value within a given address
    def getValue(self, addr: int, data_type: str):
        # Global address
        if type(addr) == str:
            newAddr = addr[1:-1]
            address = self.getValue(int(newAddr), data_type)
            return self.getValue(address, data_type)
        elif addr >= 0 * self.area and addr < 4 * self.area:
            pos = addr - self.address["global_" + data_type]
            pos = self.convertToType("int", pos)
            var = self.memory["global"][self.address["global_" + data_type]][pos]
        # Local address
        elif addr >= 4 * self.area and addr < 8 * self.area:
            pos = addr - self.address["local_" + data_type]
            pos = self.convertToType("int", pos)
            var = self.memory["local"][self.address["local_" + data_type]][pos]
        # Constant address
        elif addr >= 8 * self.area and addr < 11 * self.area:
            pos = addr - self.address["constant_" + data_type]
            var = self.memory["constant"][self.address["constant_" + data_type]][pos]
        
        # Variable not found
        if var == None:
            sys.exit(f"No variable found at {addr}")
        
        return var

    # Save a value within a given address
    def saveValue(self, addr: int, data_type: str, value):
        if type(addr) == str:
            newAddr = addr[1:-1]
            address = self.getValue(int(newAddr), data_type)
            addr = address
        value = self.convertToType(data_type, value)

        # Global address
        if addr >= 0 * self.area and addr < 4 * self.area:
            pos = addr - self.address["global_" + data_type]
            pos = self.convertToType("int", pos)
            self.memory["global"][self.address["global_" + data_type]][pos] = value
        # Local address
        elif addr >= 4 * self.area and addr < 8 * self.area:
            pos = addr - self.address["local_" + data_type]
            pos = self.convertToType("int", pos)
            self.memory["local"][self.address["local_" + data_type]][pos] = value

    # Pass along values into the New Extra Memory
    def passParamsToExtra(self, addr: int, data_type: str, value):
        value = self.convertToType(data_type, value)

        if addr >= 4 * self.area and addr < 8 * self.area:
            pos = addr - self.address["local_" + data_type]
            self.newEMemory[self.address["local_" + data_type]][pos] = value

    # Restore Memory within the New Extra Memory to our Current Memory
    def restorePrevMemory(self) -> int:
        prevM = self.extra_memory[-1]
        self.memory["local"] = prevM["memory"]
        self.extra_memory.pop()
        return prevM["instructionPointer"]