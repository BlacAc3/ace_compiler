from ..token import Token, TokenType


class LexerError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"{message} at line {line}, column {column}")


def part_of_comment(instance):
    '''Checks if the following content after the '/' is either a comment initializer or a number '''
    current_char = instance.peek_char()
    if current_char is None:
        pass

    if current_char is not None and current_char.isdigit():
        return False
    elif current_char == '/' :
        instance.next_char() # moves cursor to the '/' character
        current_char = instance.next_char() #moves cursor to the next character after comment initializer
        while current_char != '\n' and current_char is not None:
            if current_char is not None:
                instance.comments+=str(current_char)
            current_char= instance.next_char()
        return True
    elif current_char == '*':
        instance.next_char()
        current_char = instance.next_char()
        while current_char != '*' and instance.peek_char() != '/':
            instance.comments+=str(current_char)
            current_char = instance.next_char()
        instance.next_char()
        return True



class LexerArithmeticHelper:
    def __init__(self):
        pass

    @staticmethod
    def handle_dual_operators(instance, current_char, tokens):
        start_line, start_column = instance.line, instance.column
        if instance.peek_char() == '=':
            current_char += instance.next_char()  # Consume the '='

            if current_char == '==':
                tokens.append(Token(TokenType.EQUALS, current_char, start_line, start_column))
            elif current_char == '!=':
                tokens.append(Token(TokenType.NOT_EQUALS, current_char, start_line, start_column))
            elif current_char == '<=':
                tokens.append(Token(TokenType.LESS_THAN_OR_EQUAL, current_char, start_line, start_column))
            elif current_char == '>=':
                tokens.append(Token(TokenType.GREATER_THAN_OR_EQUAL, current_char, start_line, start_column))
        else:
            # Handle single-character operators
            if current_char == '=':
                tokens.append(Token(TokenType.ASSIGN, current_char, start_line, start_column))
            elif current_char == '<':
                tokens.append(Token(TokenType.LESS_THAN, current_char, start_line, start_column))
            elif current_char == '>':
                tokens.append(Token(TokenType.GREATER_THAN, current_char, start_line, start_column))
            elif current_char == '!':
                raise LexerError("Unexpected character '!'", start_line, start_column)
        return tokens

    @staticmethod
    def handle_arithmetic_operators(instance, current_char, tokens):
        ch = current_char
        start_line, start_column = instance.line, instance.column
        if ch in ['=', '!', '<', '>']:
            tokens = LexerArithmeticHelper.handle_dual_operators(instance, current_char, tokens.copy())
        elif ch == '+':
            tokens.append(Token(TokenType.PLUS, ch, start_line, start_column))
        elif ch == '-':
            tokens.append(Token(TokenType.MINUS, ch, start_line, start_column))
        elif ch == '*':
            tokens.append(Token(TokenType.MULTIPLY, ch, start_line, start_column))
        elif ch == '/':
            if not part_of_comment(instance):
                tokens.append(Token(TokenType.DIVIDE, ch, start_line, start_column))
        elif ch == '=':
            tokens.append(Token(TokenType.ASSIGN, ch, start_line, start_column))
        elif ch == ';':
            tokens.append(Token(TokenType.SEMICOLON, ch, start_line, start_column))
        else:
            # You might want to raise an error or handle unknown characters.
            raise LexerError(f"Unknown character {ch}", start_line, start_column)
        return tokens
