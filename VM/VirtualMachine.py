from VM.ExecM import ExMemory
from Pillars.Hierarchy import Hierarchy, OpID

import sys

class VirtualMachine:
    em = ExMemory()
    operators = OpID()

    ipointer : int

    quads = []
    jumps = []
    ip: int

    def __init__(self, data: dict, temps: int):
        # VERIFY AGAIN
        self.em.initializeGlobalMemory(data["Globals"])
        self.em.initializeConstMemory(data["Constants"])
        self.em.initializeLocalMemory(data["Locals"], temps)
        self.quads = data["Quadruples"]
        self.ip = 1
        self.q_length = len(self.quads)
        self.executeQuads()

    # Move the pointer to the next instruction
    def nextInstruction(self):
        self.ip = self.ip + 1

    def executeQuads(self):
        self.ip = 0
        while self.ip < self.q_length:
            self.solveQuad(self.quads[self.ip])

    def solveQuad(self, quad: dict):
        # Verify if operator is +, -, *, /, <, <=, >=, ==, !=, && or ||
        #print("Solving quad:")
        #print("#" + str(self.ip) + " " + str(quad))
        if quad["operator"] >= 1 and quad["operator"] <= 12:
            # Get operands and the address to store
            opA = quad["operandA"]
            opA = self.em.getValue(opA[0], opA[1])

            opB = quad["operandB"]
            opB = self.em.getValue(opB[0], opB[1])

            store = quad["t_memory"]
            ans = 0
            # Sum
            if self.operators.getOpID("+") == quad["operator"]:
                ans = opA + opB
            # Substraction
            elif self.operators.getOpID("-") == quad["operator"]:
                ans = opA - opB
            # Multiplication
            elif self.operators.getOpID("*") == quad["operator"]:
                ans = opA * opB
            # Division
            elif self.operators.getOpID("/") == quad["operator"]:
                ans = opA / opB
            # Less than
            elif self.operators.getOpID("<") == quad["operator"]:
                ans = opA < opB
            # Less or equal than
            elif self.operators.getOpID("<=") == quad["operator"]:
                ans = opA <= opB
            # Greater than
            elif self.operators.getOpID(">") == quad["operator"]:
                ans = opA > opB
            # Greater or equal than
            elif self.operators.getOpID(">=") == quad["operator"]:
                ans = opA >= opB
            # Equal than
            elif self.operators.getOpID("==") == quad["operator"]:
                #print(f'Comparison between {opA} and {opB}')
                ans = opA == opB
            # Different than
            elif self.operators.getOpID("!=") == quad["operator"]:
                ans = opA != opB
            # And
            elif self.operators.getOpID("&&") == quad["operator"]:
                ans = opA and opB
            # Or
            elif self.operators.getOpID("||") == quad["operator"]:
                ans = opA or opB

            self.em.saveValue(store[0], store[1], ans)

            self.nextInstruction()
        elif quad["operator"] == self.operators.getOpID("output"):
            store = quad["t_memory"]
            output = self.em.getValue(store[0], store[1])
            print(output)
            self.nextInstruction()
        elif quad["operator"] == self.operators.getOpID("input"):
            store = quad["t_memory"]
            ans = input(">> ")
            ans = self.em.convertToType(store[1], ans)
            self.em.saveValue(store[0], store[1], ans)
            self.nextInstruction()
        elif quad["operator"] == self.operators.getOpID("="):
            opA = quad["operandA"]
            opA = self.em.getValue(opA[0], opA[1])
            store = quad["t_memory"]
            self.em.saveValue(store[0], store[1], opA)
            self.nextInstruction()
        elif quad["operator"] == self.operators.getOpID("gotof"):
            opA = quad["operandA"]
            opA = self.em.getValue(opA[0], opA[1])

            if opA == False:
                self.ip = quad["t_memory"]
            else:
                self.nextInstruction()
        elif quad["operator"] == self.operators.getOpID("goto"):
            self.ip = quad["t_memory"]
        # DOUBLE CHECK
        elif quad["operator"] == self.operators.getOpID("era"):
            self.nextInstruction()
        elif quad["operator"] == self.operators.getOpID("params"):
            pValue = self.em.getValue(quad["operandA"][0], quad["operandA"][1])
            self.em.saveValue(quad["t_memory"], quad["operandA"][1], pValue)
            self.nextInstruction()
        elif quad["operator"] == self.operators.getOpID("gosub"):
            self.jumps.append(self.ip + 1)
            self.ip = quad["t_memory"]
        elif quad["operator"] == self.operators.getOpID("endfunc"):
            self.ip = self.jumps[-1]
            self.jumps.pop()
        elif quad["operator"] == self.operators.getOpID("return"):
            pValue = quad["operandA"]
            pValue = self.em.getValue(pValue[0], pValue[1])
            store = quad["t_memory"]
            self.em.saveValue(store[0], store[1], pValue)
            self.nextInstruction()
        elif quad["operator"] == self.operators.getOpID("assignr"):
            pValue = quad["operandA"]
            pValue = self.em.getValue(pValue[0], pValue[1])
            store = quad["t_memory"]
            self.em.saveValue(store[0], store[1], pValue)
            self.nextInstruction()
        elif quad["operator"] == self.operators.getOpID("ver"):
            opA = quad["operandA"]
            l_lim = quad["operandB"][0]
            u_lim = quad["t_memory"]
            val = self.em.getValue(opA[0], opA[1])

            if val < l_lim or val >= u_lim:
                sys.exit(f"Index out of range")
            self.nextInstruction()
        elif quad["operator"] == self.operators.getOpID("arrbase"):
            opA = quad["operandA"]
            opA = self.em.getValue(opA[0], opA[1])
            base = quad["operandB"][0]
            store = quad["t_memory"]
            store = (quad["t_memory"][0][1:-1], quad["t_memory"][1])
            addr = opA + base
            self.em.saveValue(int(store[0]), store[1], addr)
            self.nextInstruction()
        elif quad["operator"] == self.operators.getOpID("arrsd"):
            opA = quad["operandA"]
            opA = self.em.getValue(opA[0], opA[1])
            opB = quad["operandB"]
            opB = self.em.getValue(opB[0], opB[1])
            store = quad["t_memory"]
            ans = opA + opB
            self.em.saveValue(store[0], store[1], ans)
            self.nextInstruction()
        elif quad["operator"] == self.operators.getOpID("end"):
            self.ip = len(self.quads)
            print(f'Program compiled and executed correctly.')