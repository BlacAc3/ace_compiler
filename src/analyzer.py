class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}  # Stores variable names and their values

    def analyze(self, ast):
        for statement in ast:
            self.visit(statement)

    def visit(self, node):
        """Recursively process the AST"""
        if node[0] == "assign":
            _, var_name, expr = node
            self.symbol_table[var_name] = self.evaluate_expression(expr)  # Store variable
        elif node[0] == "if" or node[0] == "while":
            _, condition, body, *else_branch = node
            self.evaluate_expression(condition)
            for stmt in body:
                self.visit(stmt)
            if else_branch and else_branch[0] is not None:
                for stmt in else_branch[0]:
                    self.visit(stmt)
        elif node[0] == "variable":
            var_name = node[1]
            if var_name not in self.symbol_table:
                raise NameError(f"Undeclared variable '{var_name}' used")
        elif node[0] == "binary_op":
            _, op, left, right = node
            self.evaluate_expression(left)
            self.evaluate_expression(right)

    def evaluate_expression(self, expr):
        """Evaluate an expression (for type checking & validation)"""
        if expr[0] == "number":
            return "int"
        elif expr[0] == "variable":
            var_name = expr[1]
            if var_name in self.symbol_table:
                return self.symbol_table[var_name]
            raise NameError(f"Undeclared variable '{var_name}' used")
        elif expr[0] == "binary_op":
            _, op, left, right = expr
            left_type = self.evaluate_expression(left)
            right_type = self.evaluate_expression(right)
            if left_type != right_type:
                raise TypeError(f"Type mismatch in operation: {left_type} {op} {right_type}")
            return left_type
