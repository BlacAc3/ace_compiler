from ..token import TokenType, Token
from .lexer_helper import LexerArithmeticHelper, LexerConditionalHelper

class Lexer:

    def __init__(self, source_code):
        if isinstance(source_code, str):
            self.source_code = source_code
        else:
            raise TypeError("source_code must be a string")

        self.comments = ""
        self.position = 0
        self.line = 1
        self.column = 1

    def next_char(self, jump=0):
        '''Return the next character from the source code and update the position and column.'''
        #EOF checker
        if self.position + jump >= len(self.source_code):
            print("End of file reached and caught properly")
            return None

        current_char=self.peek_char(jump)
        if current_char is None:
            print("Found nothing, uncaught by EOF checker")
            return None

        for _ in range(jump+1):
            self.position += 1

            if self.peek_char() == '\n':
                self.line += 1
                self.column = 1
            # elif current_char == ' ':
            #     return self.next_char()
            else:
                self.column += 1
        return current_char

    def peek_char(self, jump=0):
        '''Checks the next character without advancing the cursor'''
        if self.position + jump >= len(self.source_code):
            return None
        return self.source_code[self.position + jump]

    def tokenize(self):
        tokens = []
        while True:
            current_char = self.peek_char()
            if current_char is None:
                tokens.append(Token(TokenType.EOF, None, self.line, self.column))
                break

            if current_char.isspace():
                self.next_char()
                continue


            if new_tokens:=LexerArithmeticHelper.handle_integer_types(self, tokens):
                tokens = list(new_tokens)
                continue

            if new_tokens := LexerConditionalHelper.handle_conditional_statements(self, tokens):
                tokens = list(new_tokens)
                continue

            if current_char.isdigit():
                start_line, start_column = self.line, self.column
                num_str = ''
                while self.peek_char() is not None and str(self.peek_char()).isdigit():
                    num_str += str(self.next_char())
                tokens.append(Token(TokenType.NUMBER, num_str, start_line, start_column))
                continue

            if current_char.isalpha() or current_char == '_':
                start_line, start_column = self.line, self.column
                id_str = ''
                while self.peek_char() is not None and (str(self.peek_char()).isalnum() or self.peek_char() == '_'):
                    id_str += str(self.next_char())
                tokens.append(Token(TokenType.IDENTIFIER, id_str, start_line, start_column))
                continue

            tokens = LexerArithmeticHelper.handle_arithmetic_operators(self, tokens.copy())

        return tokens

class LexerError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"{message} at line {line}, column {column}")
