from Pillars.Data_Types import Data_Type
from VM.Delimitations import Delimitation
from Pillars.Directory_Variables import Directory_Vars
from Pillars.Semantic_Cube import Semantic_Cube
from Pillars.Hierarchy import Hierarchy
from Pillars.Hierarchy import OpID
from Pillars.Hierarchy import Operators
import sys 

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

    # Add Operand to polish vector which includes the variable to add and its type
    def addOperand(self, var: int, type: str):
        self.polish_vector.append((var, type))

    # Add Operator to polish vector
    def addOperator(self, operator: str):
        # We found an ending parenthesis
        if operator == ')':
            self.unloadStack()
        # We found a GOTO
        elif self.operators[operator] == Hierarchy.GOTO:
            self.addQuad(operator, (), (), ())
            self.jumps_stack.append(len(self.quad_stack) - 1)
        # We found a GOTOF
        elif self.operators[operator] == Hierarchy.GOTOF:
            self.unloadPolishVector()
            operand = self.popOperandS()

            if operand[1] != Data_Type.BOOLEAN.value:
                sys.exit("Result must have been a boolean")
            self.addQuad(operator, operand, (), ())
            self.jumps_stack.append(len(self.quad_stack) - 1)
        # We found a While
        elif self.operators[operator] == Hierarchy.GOTOW:
            false = self.jumps_stack.pop()
            ret = self.jumps_stack.pop()
            
            self.addQuad("goto", (), (), ())
            
            self.quad_stack[len(self.quad_stack) - 1]["t_memory"] = ret
            self.quad_stack[false]["t_memory"] = (len(self.quad_stack))
        # We found the end of a function
        elif self.operators[operator] == Hierarchy.END_FUNC: 
            self.addQuad("endfunc", (), (), ())
        # We found an era
        elif self.operators[operator] == Hierarchy.ERA:
            space = self.popOperandS()
            self.addQuad(operator, (), (), space)
        # We found params
        elif self.operators[operator] == Hierarchy.PARAMS:
            param = self.popOperandS()
            val = self.popOperandS()

            # Verify Data Type
            if param[1] != val[1]:
                sys.exit(f"Expected parameter of type {param[1]}, received {val[1]} instead")
            self.addQuad(operator, val, (), param)
        # We found gosub
        elif self.operators[operator] == Hierarchy.GOSUB:
            quad = self.popOperandS()
            self.addQuad(operator, (quad[1], ""), (), (quad[0], ""))
        # We found a return
        elif self.operators[operator] == Hierarchy.RETURN:
            memory = self.popOperandS()
            operand = self.popOperandS()

            match = self.semantic_cube.operation_return(memory[1], operand[1], "=")

            if match == Data_Type.INVALID.value:
                sys.exit(f"Unable to return {operand[1]}, expected {memory[1]}")
            self.addQuad(operator, operand, (), memory)
        # We found an Assign ret
        elif self.operators[operator] == Hierarchy.ASSIGN_T:
            operand = self.popOperandS()
            self.addQuad(operator, operand, (), (None, operand[1]))
        # We found a ver
        elif self.operators[operator] == Hierarchy.VER:
            delimit = self.popOperandS()
            operand = self.polish_vector[-1]

            if operand[1] != "int":
                sys.exit(f"Only integers are allowed in an array")
            self.addQuad(operator, operand, (0, "int"), delimit)
        # Generate quadruple for array base
        elif self.operators[operator] == Hierarchy.ARR_BASE:
            base = self.popOperandS()
            operand = self.popOperandS()
            self.addQuad(operator, operand, base, (None, base[1]))
        # Generate s1 * d2 quad
        elif self.operators[operator] == Hierarchy.ARR_SD:
            d2 = self.popOperandS()
            s1 = self.popOperandS()
            self.addQuad(operator, s1, d2, (None, "int"))
        # Generate (s1 * d2) + s2 quad
        elif self.operators[operator] == Hierarchy.ARR_SDS:
            s1d2 = self.popOperandS()
            s2 = self.popOperandS()
            self.addQuad(operator, s1d2, s2, (None, "int"))
        # We found a multiplication or division
        elif self.operators[operator] == Hierarchy.MULT_DIV and len(self.operator_stack) > 0:
            # Verify for other multiplications or divisions
            while len(self.operator_stack) > 0 and self.operators[self.operator_stack[-1]] == Hierarchy.MULT_DIV:
                op = self.popOperatorS()
                operandA = self.popOperandS()
                operandB = self.popOperandS()

                match = self.semantic_cube.operation_return(operandA[1], operandB[1], op)

                if match == Data_Type.INVALID.value:
                    sys.exit(f"Operation of {op} involving {operandA[1]} and {operandB[1]} cannot be performed")
                
                self.addQuad(op, operandA, operandB, (None, match))
        # We found a sum or substraction
        elif self.operators[operator] == Hierarchy.SUM_SUB and len(self.operator_stack) > 0:
            # Verify for other sums or substractions
            while len(self.operator_stack) > 0 and self.operators[self.operator_stack[-1]] == Hierarchy.SUM_SUB:
                op = self.popOperatorS()
                operandB = self.popOperandS()
                operandA = self.popOperandS()

                match = self.semantic_cube.operation_return(operandA[1], operandB[1], op)

                if match == Data_Type.INVALID.value:
                    sys.exit(f"Operation of {op} involving {operandA[1]} and {operandB[1]} cannot be performed")
                
                self.addQuad(op, operandA, operandB, (None, match))
        # We found a comparison
        elif self.operators[operator] == Hierarchy.COMPARE and len(self.operator_stack) > 0:
            # Verify for other comparisons or operations of higher hierarchy
            while (len(self.operator_stack) > 0 and (self.operators[self.operator_stack[-1]] == Hierarchy.COMPARE
            or self.operators[self.operator_stack[-1]] < Hierarchy.COMPARE)):
                op = self.popOperatorS()
                operandB = self.popOperandS()
                operandA = self.popOperandS()

                match = self.semantic_cube.operation_return(operandA[1], operandB[1], op)

                if match == Data_Type.INVALID.value:
                    sys.exit(f"Operation of {op} involving {operandA[1]} and {operandB[1]} cannot be performed")
                
                self.addQuad(op, operandA, operandB, (None, match))
        # We found a logical operation
        elif self.operators[operator] == Hierarchy.LOGIC and len(self.operator_stack) > 0:
            # Verify for other logical operations or operations of higher hierarchy
            while (len(self.operator_stack) > 0 and (self.operators[self.operator_stack[-1]] == Hierarchy.LOGIC
            or self.operators[self.operator_stack[-1]] < Hierarchy.LOGIC)):
                op = self.popOperatorS()
                operandB = self.popOperandS()
                operandA = self.popOperandS()

                match = self.semantic_cube.operation_return(operandA[1], operandB[1], op)

                if match == Data_Type.INVALID.value:
                    sys.exit(f"Operation of {op} involving {operandA[1]} and {operandB[1]} cannot be performed")
                
                self.addQuad(op, operandA, operandB, (None, match))
        # We found a print
        elif (self.operators[operator] == Hierarchy.PRINT and len(self.operator_stack) > 0):
            self.unloadPolishVector()

        if (operator != ')' and self.operators[operator] <= Hierarchy.INPUT):
            self.operator_stack.append(operator)

    # Pop operator from Stack and return it
    def popOperatorS(self) -> str:
        operator = self.operator_stack[-1]
        self.operator_stack.pop()
        return operator

    # Pop operand from Stack and return it
    def popOperandS(self) -> tuple:
        operand = self.polish_vector[-1]
        self.polish_vector.pop()
        return operand

    # Unload Polish Vector
    def unloadPolishVector(self):
        while len(self.operator_stack) > 0:
            if self.operator_stack[-1] == '(':
                break
            # If we find a print
            elif self.operators[self.operator_stack[-1]] == Hierarchy.PRINT:
                operator = self.popOperatorS()
                operand = self.popOperandS()

                self.addQuad(operator, (), (), operand)
            # If we find an input
            elif self.operators[self.operator_stack[-1]] == Hierarchy.INPUT:
                operator = self.popOperatorS()
                operand = self.popOperandS()

                self.addQuad(operator, (), (), operand)
            # If we find a var assignment
            elif self.operators[self.operator_stack[-1]] == Hierarchy.ASSIGN:
                operator = self.popOperatorS()
                operandA = self.popOperandS()
                operandB = self.popOperandS()

                match = self.semantic_cube.operation_return(operandA[1], operandB[1], operator)

                if match == Data_Type.INVALID.value:
                    sys.exit(f"Unable to assign {operandA[1]} to {operandB[1]}")
                
                self.addQuad(operator, operandA, (), operandB)
            else:
                operator = self.popOperatorS()
                operandB = self.popOperandS()
                operandA = self.popOperandS()

                match = self.semantic_cube.operation_return(operandA[1], operandB[1], operator)

                if match == Data_Type.INVALID.value:
                    sys.exit(f"Invalid operation")

                self.addQuad(operator, operandA, operandB, (None, match))


    # Unload stack when parenthesis found
    def unloadStack(self):
        # As long as we dont find the first parenthesis
        while self.operator_stack[-1] != '(':
            operator = self.popOperatorS()
            operandA = self.popOperandS()
            operandB = self.popOperandS()
            
            # We verify if the operation is valid with our Semantic Cube
            match = self.semantic_cube.operation_return(operandA[1], operandB[2], operator)

            # If the result is invalid then we exit because the operation cannot be done
            if match == Data_Type.INVALID.value:
                sys.exit(f"Operation of {operator} involving {operandA[1]} and {operandB[1]} cannot be performed")

            # If it can be done we continue and add it to the quadruples
            self.addQuad(operator, operandA, operandB, (None, match))

    # Print all Quads
    def printQuads(self):
        for i, quad in enumerate(self.quad_stack):
            print(i, ": ", quad["operator"], quad["operandA"], quad["operandB"], quad["t_memory"])

    # Get stack of quads
    def getQuads(self):
        return self.quad_stack

    # Add Quad to jump stack
    def addJump(self):
        self.jumps_stack.append((len(self.quad_stack)))

    # Pop from jump stack
    def popJump(self) -> int:
        jump = self.jumps_stack[-1]
        self.jumps_stack.pop()
        return jump

    # Finish the goto and/or gotof
    def finishGoto(self, data_type: str = ""):
        if self.operators[data_type] == Hierarchy.GOTOF:
            jump = self.popJump()
            self.quad_stack[jump]["t_memory"] = (len(self.quad_stack))
        else: 
            jump = self.popJump()
            self.quad_stack[jump]["t_memory"] = (len(self.quad_stack) + 1)

    # Add a Quad to the Quad stack
    def addQuad(self, op: str, operandA: tuple, operandB: tuple, t_memory: tuple):
        # If we have to create a temporal
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

        

        