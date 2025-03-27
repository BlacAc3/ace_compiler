from ..token import TokenType, Token
from .lexer_helper import LexerArithmeticHelper





class Lexer:
    # KEYWORDS = {
    #     "if": TokenType.IF,
    #     "else": TokenType.ELSE,
    #     "while": TokenType.WHILE,
    #     "return": TokenType.RETURN,
    #     "int": TokenType.INT,
    #     "float": TokenType.FLOAT
    # }

    def __init__(self, source_code):
        if isinstance(source_code, str):
            self.source_code = source_code
        else:
            raise TypeError("source_code must be a string")


        self.comments = ""
        self.position = 0
        self.line = 1
        self.column = 1

    def next_char(self):
        '''Return the next character from the source code and update the position and column.'''
        #EOF checker
        if self.position >= len(self.source_code):
            print("End of file reached and caught properly")
            return None

        current_char=self.peek_char()
        if current_char is None:
            print("Found nothing, uncaught by EOF checker")
            return None
        self.position += 1

        if current_char == '\n':
            self.line += 1
            self.column = 1
        # elif current_char == ' ':
        #     return self.next_char()
        else:
            self.column += 1
        return current_char

    def peek_char(self):
        '''Checks the next character without advancing the cursor'''
        if self.position >= len(self.source_code):
            return None
        return self.source_code[self.position]

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
            if current_char.isdigit():
                start_line, start_column = self.line, self.column
                num_str = ''
                while self.peek_char() is not None and self.peek_char().isdigit():
                    num_str += self.next_char()
                tokens.append(Token(TokenType.NUMBER, num_str, start_line, start_column))
                continue

            if current_char.isalpha() or current_char == '_':
                start_line, start_column = self.line, self.column
                id_str = ''
                id_str.isalnum()
                while self.peek_char() is not None and (self.peek_char().isalnum() or self.peek_char() == '_'):
                    id_str += self.next_char()
                tokens.append(Token(TokenType.IDENTIFIER, id_str, start_line, start_column))
                continue

            ch = self.next_char()
            tokens = LexerArithmeticHelper.handle_arithmetic_operators(self, ch, tokens.copy())
            #Arithmetic Operators
            #----------------------------

            #Conditionals
        return tokens

class LexerError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"{message} at line {line}, column {column}")

source = """
x = 10 //Hello people, this is a one line comment
x = 20
/*Now this is a multi-line comment
takes and uses more lines than you thought huh.
*/
z = y +3
"""
lexer = Lexer(source)
tokens = lexer.tokenize()
print(f'Comments: {lexer.comments}')
for token in tokens:
    print(token)
