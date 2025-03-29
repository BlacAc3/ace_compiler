from ..token import TokenType

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0  # Pointer to current token

    def peek(self) :
        """Get the current token without consuming it."""
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None  # End of input

    def advance(self):
        """Consume the current token and move to the next."""
        self.current += 1
        return self.tokens[self.current - 1]

    def match(self, *token_types):
        """Check if the current token matches any of the given types, then consume it."""
        if self.peek() and self.peek().type in token_types:
            return self.advance()
        return None

    def parse_expression(self):
        """Parse an expression following the grammar rules."""
        node = self.parse_term()
        # while self.match(TokenType.PLUS, TokenType.MINUS):
        #     operator = self.tokens[self.current - 1]  # Get the last consumed operator
        #     right = self.parse_term()
        #     node = ("binary_op", operator, node, right)
        return node


    def parse_term(self):
        """Handle multiplication and division."""
        node = self.parse_factor()
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.PLUS, TokenType.MINUS,TokenType.GREATER_THAN, TokenType.LESS_THAN):
            operator = self.tokens[self.current - 1]  # Get the last consumed operator
            right = self.parse_factor()
            node = ("binary_op", operator, node, right)
        return node

    def parse_factor(self):
        """Handle numbers, identifiers, and parenthesized expressions."""
        token = self.peek()

        if self.match(TokenType.NUMBER):
            return ("number", token.value)

        if self.match(TokenType.IDENTIFIER):
            return ("variable", token.value)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.parse_expression()
            if not self.match(TokenType.RIGHT_PAREN):
                raise SyntaxError("Expected ')'")
            return expr

        raise SyntaxError(f"Unexpected token: {token}")

    def parse_statement(self):
        """Parse a statement (assignment or expression)."""
        token = self.peek()

        if token.type == TokenType.IF:
            return self.parse_if_statement()
        if token.type == TokenType.WHILE:
            return self.parse_while_statement()
        if token.type == TokenType.IDENTIFIER and self.tokens[self.current + 1].type == TokenType.ASSIGN:
            return self.parse_assignment()
        else:
            return self.parse_expression()


    def parse_if_statement(self):
        """Parse an if statement"""
        self.match(TokenType.IF) #Consume the 'if' token
        self.match(TokenType.LEFT_PAREN) #consume the '(' token
        condition = self.parse_expression()
        self.match(TokenType.RIGHT_PAREN) #consume the ')' token
        self.match(TokenType.LEFT_BRACE)

        true_branch=[]
        while self.peek() and self.peek().type != TokenType.RIGHT_BRACE:
            true_branch.append(self.parse_statement())
        self.match(TokenType.RIGHT_BRACE)

        false_branch =None
        if self.match(TokenType.ELSE):
            self.match(TokenType.LEFT_BRACE)
            false_branch = []
            while self.peek() and self.peek().type != TokenType.RIGHT_BRACE:
                false_branch.append(self.parse_statement())
            self.match(TokenType.RIGHT_BRACE)
        return ("if", condition, true_branch, false_branch)


    def parse_while_statement(self):
        """Parse a while loop."""
        self.match(TokenType.WHILE)  # Consume 'while'
        self.match(TokenType.LEFT_PAREN)  # Consume '('
        condition = self.parse_expression()
        self.match(TokenType.RIGHT_PAREN)  # Consume ')'
        self.match(TokenType.LEFT_BRACE)  # Consume '{'

        body = []
        while self.peek() and self.peek().type != TokenType.RIGHT_BRACE:
            body.append(self.parse_statement())

        self.match(TokenType.RIGHT_BRACE)  # Consume '}'

        return ("while", condition, body)



    def parse_assignment(self):
        """Parse an assignment statement."""
        var_name = self.match(TokenType.IDENTIFIER)  # Consume identifier
        self.match(TokenType.ASSIGN)  # Consume '='
        expr = self.parse_expression()
        self.match(TokenType.SEMICOLON)  # Ensure there's a semicolon
        return ("assign", var_name.value, expr)

    def parse(self):
        """Parse the full program (multiple statements)."""
        statements = []
        while self.peek() and self.peek().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return statements
