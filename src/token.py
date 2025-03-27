class TokenType:
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    ASSIGN = "ASSIGN"
    SEMICOLON = "SEMICOLON"
    EQUALS="EQUALS"
    NOT_EQUALS="NOT_EQUALS"
    LESS_THAN="LESS_THAN"
    LESS_THAN_OR_EQUAL="LESS_THAN_OR_EQUAL"
    GREATER_THAN="GREATER_THAN"
    GREATER_THAN_OR_EQUAL="GREATER_THAN_OR_EQUAL"
    EOF = "EOF"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    RETURN = "RETURN"
    INT = "INT"
    FLOAT = "FLOAT"

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}, {self.column})"

    def __str__(self):
        return f"{self.type}({self.value})"
