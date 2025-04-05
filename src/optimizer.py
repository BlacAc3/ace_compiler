class IRGenerator:
    def __init__(self):
        self.while_counter = 0
        self.condition_counter = 0
        self.temp_counter = 0
        self.ir_code = []

    def generate(self, ast):
        for statement in ast:
            self.visit(statement)

    def new_temp(self):
        """Generate a new temporary variable (t1, t2, etc.)."""
        temp_name = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp_name

    def visit(self, node):
        if node[0] == "assign":
            _, var_name, expr = node
            result_temp = self.generate_expression(expr)
            self.ir_code.append(f"{var_name} = {result_temp}")
        elif node[0] == "if":
            _, condition, true_branch, false_branch = node
            cond_temp = self.generate_expression(condition)
            cond_counter= self.condition_counter
            self.condition_counter+=1
            self.ir_code.append(f"if_false {cond_temp} goto L_else{cond_counter}")
            for stmt in true_branch:
                self.visit(stmt)
            if false_branch:
                self.ir_code.append(f"L_else{cond_counter}:")
                for stmt in false_branch:
                    self.visit(stmt)
            self.ir_code.append(f"L_end{cond_counter}:")
        elif node[0] == "while":
            _, condition, body = node
            while_counter = self.while_counter + 1
            self.while_counter+=1
            cond_temp = self.generate_expression(condition)
            self.ir_code.append(f"while{while_counter} {cond_temp} do")
            for stmt in body:
                self.visit(stmt)
            self.ir_code.append(f"end while{while_counter}")

    def generate_expression(self, expr):
        """Generate IR for an expression."""
        if expr[0] == "number":
            return str(expr[1])
        elif expr[0] == "variable":
            return expr[1]
        elif expr[0] == "binary_op":
            _, op, left, right = expr
            left_temp = self.generate_expression(left)
            right_temp = self.generate_expression(right)
            result_temp = self.new_temp()
            self.ir_code.append(f"{result_temp} = {left_temp} {op.value} {right_temp}")
            return result_temp



def constant_folding(ir_code):
    '''evaluates and executes arithmetic operations during compilation, for speed.'''
    optimized_code = []
    for line in ir_code:
        parts = line.split(" = ")
        if len(parts) == 2 and any(op in parts[1] for op in "+-*/"):
            try:
                result = eval(parts[1])  # Evaluate if it's a constant expression
                optimized_code.append(f"{parts[0]} = {result}")
            except:
                optimized_code.append(line)
        else:
            optimized_code.append(line)
    return optimized_code


def dead_code_elimination(ir_code):
    used_vars = set()
    for line in ir_code:
        if "=" in line:
            used_vars.update(line.split(" = ")[1].split())

    optimized_code = []
    for line in ir_code:
        lhs = line.split(" = ")[0]
        # rhs = line.split(" = ")[1]
        if lhs in used_vars or "goto" in line:
            optimized_code.append(line)
    return optimized_code


def common_subexpression_elimination(ir_code):
    expr_map = {}
    optimized_code = []
    for line in ir_code:
        parts = line.split(" = ")
        if len(parts) == 2:
            lhs, rhs = parts
            if rhs in expr_map:
                optimized_code.append(f"{lhs} = {expr_map[rhs]}")
            else:
                expr_map[rhs] = lhs
                optimized_code.append(line)
        else:
            optimized_code.append(line)
    return optimized_code
