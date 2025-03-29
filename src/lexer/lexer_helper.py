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
        instance.next_char() # Consumes the '/' character
        current_char = instance.next_char() # Starts consuming the next character after comment initializer
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
    def handle_arithmetic_operators(instance, tokens):
        ch = instance.next_char()
        start_line, start_column = instance.line, instance.column
        if ch in ['=', '!', '<', '>']:
            tokens = LexerArithmeticHelper.handle_dual_operators(instance, ch, tokens.copy())
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
            return None
        return tokens

    @staticmethod
    def handle_integer_types(instance, tokens):
        new_tokens =[]
        handle_words(instance, "int",tokens, callback=lambda: new_tokens.append(Token(TokenType.INTEGER, "int" ,instance.line,instance.column)))
        handle_words(instance, "float", tokens, callback=lambda: new_tokens.append(Token(TokenType.FLOAT, "float",instance.line,instance.column)))
        if len(new_tokens) == 0:
            return None
        tokens = [tokens.append(new_token) for new_token in new_tokens]
        return tokens


class LexerConditionalHelper:
    @staticmethod
    def handle_conditional_statements(instance, tokens):
        """
        Handle conditional statements (if, else) and their associated tokens

        Args:
            instance: The lexer instance
            current_char: The current character being processed
            tokens: List of tokens to append to

        Returns:
            list: Updated list of tokens
        """
        start_line, start_column = instance.line, instance.column
        current_char=instance.peek_char()
        new_tokens=[]

        handle_words(instance, "if", tokens,callback = lambda: new_tokens.append(Token(TokenType.IF, "if", instance.line, instance.column)))
        handle_words(instance, "else", tokens, callback = lambda: new_tokens.append(Token(TokenType.ELSE, "else", instance.line, instance.column)))
        handle_words(instance, "while", tokens, callback= lambda: new_tokens.append(Token(TokenType.WHILE, "while", instance.line, instance.column)))
        handle_words(instance, "return ", tokens, callback = lambda: new_tokens.append(Token(TokenType.RETURN, "return", instance.line, instance.column)))



        # Handle parentheses for condition
        if current_char == '(':
            new_tokens.append(Token(TokenType.LEFT_PAREN, current_char, start_line, start_column))

        elif current_char == ')':
            new_tokens.append(Token(TokenType.RIGHT_PAREN, current_char, start_line, start_column))

        # Handle curly braces for code blocks
        elif current_char == '{':
            new_tokens.append(Token(TokenType.LEFT_BRACE, current_char, start_line, start_column))

        elif current_char == '}':
            new_tokens.append(Token(TokenType.RIGHT_BRACE, current_char, start_line, start_column))

        if len(new_tokens)==0:
            return None

        instance.next_char()
        return tokens + new_tokens



def handle_words(instance, word, tokens, callback):
    result=""
    for i in range(len(word)):
        result += str(instance.peek_char(i))
    if result == word:
        callback()
        print(f"call back called for {result}")
    else:
        return tokens
    instance.next_char(len(result)-1)

    return tokens
