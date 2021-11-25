from Pillars.Data_Types import Data_Type

class Semantic_Cube():

    cube = {
        "int": {
            "int": {
                "+": Data_Type.INT,
                "-": Data_Type.INT,
                "*": Data_Type.INT,
                "/": Data_Type.INT,
                "%": Data_Type.INT,
                "&&": Data_Type.INVALID,
                "||": Data_Type.INVALID,
                "=": Data_Type.INT,
                "==": Data_Type.BOOLEAN,
                "!=": Data_Type.BOOLEAN,
                ">=": Data_Type.BOOLEAN,
                ">": Data_Type.BOOLEAN,
                "<=": Data_Type.BOOLEAN,
                "<": Data_Type.BOOLEAN
            },
            "float": {
                "+": Data_Type.FLOAT,
                "-": Data_Type.FLOAT,
                "*": Data_Type.FLOAT,
                "/": Data_Type.FLOAT,
                "%": Data_Type.FLOAT,
                "&&": Data_Type.INVALID,
                "||": Data_Type.INVALID,
                "=": Data_Type.FLOAT,
                "==": Data_Type.BOOLEAN,
                "!=": Data_Type.BOOLEAN,
                ">=": Data_Type.BOOLEAN,
                ">": Data_Type.BOOLEAN,
                "<=": Data_Type.BOOLEAN,
                "<": Data_Type.BOOLEAN
            },
            "string": {
                "+": Data_Type.INT,
                "-": Data_Type.INT,
                "*": Data_Type.INT,
                "/": Data_Type.INT,
                "%": Data_Type.INT,
                "&&": Data_Type.INVALID,
                "||": Data_Type.INVALID,
                "=": Data_Type.INT,
                "==": Data_Type.BOOLEAN,
                "!=": Data_Type.BOOLEAN,
                ">=": Data_Type.BOOLEAN,
                ">": Data_Type.BOOLEAN,
                "<=": Data_Type.BOOLEAN,
                "<": Data_Type.BOOLEAN
            },
            "boolean": {
                "+": Data_Type.INVALID,
                "-": Data_Type.INVALID,
                "*": Data_Type.INVALID,
                "/": Data_Type.INVALID,
                "%": Data_Type.INVALID,
                "&&": Data_Type.INVALID,
                "||": Data_Type.INVALID,
                "=": Data_Type.INVALID,
                "==": Data_Type.INVALID,
                "!=": Data_Type.INVALID,
                ">=": Data_Type.INVALID,
                ">": Data_Type.INVALID,
                "<=": Data_Type.INVALID,
                "<": Data_Type.INVALID
            }
        },
        "float": {
            "int": {
                "+": Data_Type.INT,
                "-": Data_Type.INT,
                "*": Data_Type.INT,
                "/": Data_Type.INT,
                "%": Data_Type.INT,
                "&&": Data_Type.INVALID,
                "||": Data_Type.INVALID,
                "=": Data_Type.INT,
                "==": Data_Type.BOOLEAN,
                "!=": Data_Type.BOOLEAN,
                ">=": Data_Type.BOOLEAN,
                ">": Data_Type.BOOLEAN,
                "<=": Data_Type.BOOLEAN,
                "<": Data_Type.BOOLEAN
            },
            "float": {
                "+": Data_Type.FLOAT,
                "-": Data_Type.FLOAT,
                "*": Data_Type.FLOAT,
                "/": Data_Type.FLOAT,
                "%": Data_Type.FLOAT,
                "&&": Data_Type.INVALID,
                "||": Data_Type.INVALID,
                "=": Data_Type.FLOAT,
                "==": Data_Type.BOOLEAN,
                "!=": Data_Type.BOOLEAN,
                ">=": Data_Type.BOOLEAN,
                ">": Data_Type.BOOLEAN,
                "<=": Data_Type.BOOLEAN,
                "<": Data_Type.BOOLEAN
            },
            "string": {
                "+": Data_Type.INVALID,
                "-": Data_Type.INVALID,
                "*": Data_Type.INVALID,
                "/": Data_Type.INT,
                "%": Data_Type.INT,
                "&&": Data_Type.INVALID,
                "||": Data_Type.INVALID,
                "=": Data_Type.INVALID,
                "==": Data_Type.INVALID,
                "!=": Data_Type.INVALID,
                ">=": Data_Type.INVALID,
                ">": Data_Type.INVALID,
                "<=": Data_Type.INVALID,
                "<": Data_Type.INVALID
            },
            "boolean": {
                "+": Data_Type.INVALID,
                "-": Data_Type.INVALID,
                "*": Data_Type.INVALID,
                "/": Data_Type.INVALID,
                "%": Data_Type.INVALID,
                "&&": Data_Type.INVALID,
                "||": Data_Type.INVALID,
                "=": Data_Type.INVALID,
                "==": Data_Type.INVALID,
                "!=": Data_Type.INVALID,
                ">=": Data_Type.INVALID,
                ">": Data_Type.INVALID,
                "<=": Data_Type.INVALID,
                "<": Data_Type.INVALID
            }
        },
        "string": {
            "int": {
                "+": Data_Type.INVALID,
                "-": Data_Type.INVALID,
                "*": Data_Type.INVALID,
                "/": Data_Type.INVALID,
                "%": Data_Type.INVALID,
                "&&": Data_Type.INVALID,
                "||": Data_Type.INVALID,
                "=": Data_Type.INVALID,
                "==": Data_Type.INVALID,
                "!=": Data_Type.INVALID,
                ">=": Data_Type.INVALID,
                ">": Data_Type.INVALID,
                "<=": Data_Type.INVALID,
                "<": Data_Type.INVALID
            },
            "float": {
                "+": Data_Type.INVALID,
                "-": Data_Type.INVALID,
                "*": Data_Type.INVALID,
                "/": Data_Type.INVALID,
                "%": Data_Type.INVALID,
                "&&": Data_Type.INVALID,
                "||": Data_Type.INVALID,
                "=": Data_Type.INVALID,
                "==": Data_Type.INVALID,
                "!=": Data_Type.INVALID,
                ">=": Data_Type.INVALID,
                ">": Data_Type.INVALID,
                "<=": Data_Type.INVALID,
                "<": Data_Type.INVALID
            },
            "string": {
                "+": Data_Type.INVALID,
                "-": Data_Type.INVALID,
                "*": Data_Type.INVALID,
                "/": Data_Type.INVALID,
                "%": Data_Type.INVALID,
                "&&": Data_Type.INVALID,
                "||": Data_Type.INVALID,
                "=": Data_Type.STRING,
                "==": Data_Type.INVALID,
                "!=": Data_Type.BOOLEAN,
                ">=": Data_Type.INVALID,
                ">": Data_Type.INVALID,
                "<=": Data_Type.INVALID,
                "<": Data_Type.INVALID
            },
            "boolean": {
                "+": Data_Type.INVALID,
                "-": Data_Type.INVALID,
                "*": Data_Type.INVALID,
                "/": Data_Type.INVALID,
                "%": Data_Type.INVALID,
                "&&": Data_Type.INVALID,
                "||": Data_Type.BOOLEAN,
                "=": Data_Type.BOOLEAN,
                "==": Data_Type.BOOLEAN,
                "!=": Data_Type.BOOLEAN,
                ">=": Data_Type.INVALID,
                ">": Data_Type.INVALID,
                "<=": Data_Type.INVALID,
                "<": Data_Type.INVALID
            }
        },
        "boolean": {
            "int": {
                "+": Data_Type.INVALID,
                "-": Data_Type.INVALID,
                "*": Data_Type.INVALID,
                "/": Data_Type.INVALID,
                "%": Data_Type.INVALID,
                "&&": Data_Type.INVALID,
                "||": Data_Type.INVALID,
                "=": Data_Type.INVALID,
                "==": Data_Type.INVALID,
                "!=": Data_Type.INVALID,
                ">=": Data_Type.INVALID,
                ">": Data_Type.INVALID,
                "<=": Data_Type.INVALID,
                "<": Data_Type.INVALID
            },
            "float": {
                "+": Data_Type.INVALID,
                "-": Data_Type.INVALID,
                "*": Data_Type.INVALID,
                "/": Data_Type.INVALID,
                "%": Data_Type.INVALID,
                "&&": Data_Type.INVALID,
                "||": Data_Type.INVALID,
                "=": Data_Type.INVALID,
                "==": Data_Type.INVALID,
                "!=": Data_Type.INVALID,
                ">=": Data_Type.INVALID,
                ">": Data_Type.INVALID,
                "<=": Data_Type.INVALID,
                "<": Data_Type.INVALID
            },
            "string": {
                "+": Data_Type.INVALID,
                "-": Data_Type.INVALID,
                "*": Data_Type.INVALID,
                "/": Data_Type.INVALID,
                "%": Data_Type.INVALID,
                "&&": Data_Type.INVALID,
                "||": Data_Type.INVALID,
                "=": Data_Type.INVALID,
                "==": Data_Type.INVALID,
                "!=": Data_Type.INVALID,
                ">=": Data_Type.INVALID,
                ">": Data_Type.INVALID,
                "<=": Data_Type.INVALID,
                "<": Data_Type.INVALID
            },
            "boolean": {
                "+": Data_Type.INVALID,
                "-": Data_Type.INVALID,
                "*": Data_Type.INVALID,
                "/": Data_Type.INVALID,
                "%": Data_Type.INVALID,
                "&&": Data_Type.INVALID,
                "||": Data_Type.BOOLEAN,
                "=": Data_Type.BOOLEAN,
                "==": Data_Type.BOOLEAN,
                "!=": Data_Type.BOOLEAN,
                ">=": Data_Type.INVALID,
                ">": Data_Type.INVALID,
                "<=": Data_Type.INVALID,
                "<": Data_Type.INVALID
            }
        }
    }

    def operation_return(self, operandA: str, operandB: str, operator: str) -> str:
        return self.cube[operandA][operandB][operator].value