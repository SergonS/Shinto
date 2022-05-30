from VM.ExecM import ExMemory
from Pillars.Hierarchy import Hierarchy, OpID

import sys

class VirtualMachine:
    em = ExMemory()
    operators = OpID().IDOperators

    quads = []
    ip: int

    def __init__(self, data: dict):
        # VERIFY AGAIN
        self.em.initializeGlobalMemory(data["Globals"])
        self.em.initializeConstMemory(data["Constants"])
        self.em.initializeLocalMemory(data["Locals"])

        self.quads = data["Quadruples"]
        self.executeQuads()

    # Move the pointer to the next instruction
    def nextInstruction(self):
        self.ip = self.ip + 1

    def executeQuads(self):
        self.ip = 0
        while self.ip < len(self.quads):
            self.solveQuad(self.quads[self.ip])

    def solveQuad(self, quad: dict):
        # Verify if operator is +, -, *, /, <, <=, >=, ==, !=, && or ||
        if self.operators.getOID(quad["operator"]) >= 1 and self.operators.getOID(quad["operator"]) <= 12:
            # Get operands and the address to store
            opA = quad["operandA"]
            opA = self.em.getValue(opA[0], opA[1])

            opB = quad["operandB"]
            opB = self.em.getValue(opB[0], opB[1])

            store = quad["t_memory"]

            # Sum
            if quad["operator"] == self.operators["+"]:
                ans = opA + opB
            # Substraction
            elif quad["operator"] == self.operators["-"]:
                ans = opA - opB
            # Multiplication
            elif quad["operator"] == self.operators["*"]:
                ans = opA * opB
            # Division
            elif quad["operator"] == self.operators["/"]:
                ans = opA / opB
            # Less than
            elif quad["operator"] == self.operators["<"]:
                ans = opA < opB
            # Less or equal than
            elif quad["operator"] == self.operators["<="]:
                ans = opA <= opB
            # Greater than
            elif quad["operator"] == self.operators[">"]:
                ans = opA > opB
            # Greater or equal than
            elif quad["operator"] == self.operators[">="]:
                ans = opA >= opB
            # Equal than
            elif quad["operator"] == self.operators["=="]:
                ans = opA == opB
            # Different than
            elif quad["operator"] == self.operators["!="]:
                ans = opA != opB
            # And
            elif quad["operator"] == self.operators["&&"]:
                ans = opA and opB
            # Or
            elif quad["operator"] == self.operators["||"]:
                ans = opA or opB

            self.em.saveValue(store[0], store[1], ans)

            self.nextInstruction()
        elif quad["operator"] == self.operators["print"]:
            store = quad["t_memory"]
            print(self.em.getValue(store[0], store[1]))
            self.nextInstruction()
        elif quad["operator"] == self.operators["input"]:
            store = quad["t_memory"]
            ans = input(">> ")
            ans = self.em.convertToType(store[1], ans)
            self.nextInstruction()
        elif quad["operator"] == self.operators["="]:
            opA = quad["operandA"]
            opA = self.em.getValue(opA[0], opA[1])
            store = quad["t_memory"]
            self.em.saveValue(store[0], store[1], opA)
            self.nextInstruction()
        elif quad["operator"] == self.operators["gotof"]:
            opA = quad["operandA"]
            opA = self.em.getValue(opA[0], opA[1])

            if opA == False:
                self.ip = quad["t_memory"]
            else:
                self.nextInstruction()
        elif quad["operator"] == self.operators["goto"]:
            self.ip = quad["t_memory"]
        # DOUBLE CHECK
        elif quad["operator"] == self.operators["era"]:
            self.em.initializeLocalMemory(self.data["Locals"])
            self.nextInstruction()
        elif quad["operator"] == self.operators["params"]:
            pValue = self.em.getValue(quad["operandA"][0], quad["operandA"][1])

            self.em.passParamsToExtra(quad["t_memory"], quad["operandA"][1], pValue)
            self.nextInstruction()
        elif quad["operator"] == self.operators["gosub"]:
            self.em.saveMemory(self.ip)
            self.em.setEMtoLM()
            self.ip = quad["t_memory"]
        elif quad["operator"] == self.operators["endfunc"]:
            self.IP = self.em.restorePrevMemory()
            self.nextInstruction()
        elif quad["operator"] == self.operators["return"]:
            pValue = quad["operandA"]
            pValue = self.em.getValue(pValue[0], pValue[1])
            store = quad["t_memory"]
            self.em.saveValue(store[0], store[1], pValue)
            self.nextInstruction()
        elif quad["operator"] == self.operators["assignr"]:
            pValue = quad["operandA"]
            pValue = self.em.getValue(pValue[0], pValue[1])
            store = quad["t_memory"]
            self.em.saveValue(store[0], store[1], pValue)
            self.nextInstruction()
        elif quad["operator"] == self.operators["ver"]:
            opA = quad["operandA"]
            l_lim = quad["operandB"][0]
            u_lim = quad["t_memory"]
            val = self.em.getValue(opA[0], opA[1])

            if val < l_lim or val >= u_lim:
                sys.exit(f"Index out of range")
            self.nextInstruction()
        elif quad["operator"] == self.operators["addbase"]:
            opA = quad["operandA"]
            opA = self.em.getValue(opA[0], opA[1])
            base = quad["operandB"][0]
            store = quad["t_memory"]
            store = (quad["t_memory"][0][1:-1], quad["t_memory"][1])
            addr = opA + base
            self.em.saveValue(int(store[0]), store[1], addr)
            self.nextInstruction()
        elif quad["operator"] == self.operators["arrsd"]:
            opA = quad["operandA"]
            opA = self.em.getValue(opA[0], opA[1])
            opB = quad["operandB"]
            opB = self.em.getValue(opB[0], opB[1])
            store = quad["t_memory"]
            ans = opA + opB
            self.em.saveValue(store[0], store[1], ans)
            self.nextInstruction()