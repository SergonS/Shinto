from Data_Types import Data_Type
from VM.Delimitations import Delimitation
from Directory_Variables import Directory_Variables
from Semantic_Cube import Semantic_Cube
from Variables import Variable
from Hierarchy import Hierarchy
from Hierarchy import OpID
from Hierarchy import Operators

class QuadOverseer:

    quad_stack: list
    jumps_stack: list
    operator_stack: list
    polish_vector: list

    semantic_cube = Semantic_Cube()
    delimitation = Delimitation()
    op_id = OpID()
    operators = Operators().HierarchyOp

    def __init__(self):
        self.quad_stack = []
        self.jumps_stack = []
        self.operator_stack = []
        self.polish_vector = []

    def addOperand(self, var: int, type: str):
        self.polish_vector.append((var, type))

    def addQuad(self, op: str, operandA: tuple, operandB: tuple, t_memory: tuple):
        if len(t_memory) > 0 and t_memory[0] == None:
            addr = self.delimitation.getAddr("local_" + str(t_memory[1]) + self.delimitation.getCounter("local_" + str(t_memory[1])))
            self.delimitation.verifyDelimitation(addr, "local_" + str(t_memory[1]))
            self.delimitation.updateCounter("local_" + str(t_memory[1]))
            t_memory = (addr, t_memory[1])
        elif op == "era" or op == "gosub" or op == "params" or op == "ver":
            t_memory = t_memory[0]

        if op == "arrbase":
            t_memory = ("(" + str(t_memory[0]) + ")", t_memory[1])

        self.quad_stack.append({
            "operator": self.op_id.getOID(op),
            "operandA": operandA,
            "operandB": operandB,
            "t_memory": t_memory
        })

        if (self.operators[op] <= Hierarchy.LOGIC or 
                self.operators[op] == Hierarchy.ASSIGN_R or
                self.operators[op] == Hierarchy.ARR_BASE or
                self.operators[op] == Hierarchy.ARR_SD or
                self.operators[op] == Hierarchy.ARR_S):
            self.addOperand(t_memory[0], t_memory[1])

        

        