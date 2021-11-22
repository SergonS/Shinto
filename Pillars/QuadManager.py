from Data_Types import Data_Type
from Directory_Variables import Directory_Variables
from Semantic_Cube import Semantic_Cube
from Variables import Variable

class QuadOverseer:

    quad_stack: list
    jumps_stack: list
    operator_stack: list
    polish_vector: list

    semantic_cube = Semantic_Cube()

    def __init__(self):
        self.quad_stack = []
        self.jumps_stack = []
        self.operator_stack = []
        self.polish_vector = []

        