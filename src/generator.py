import re

class CodeGenerator:
    def __init__(self):
        self.instructions = []
        self.values = []

    def generate(self, ir_code):
        for line in ir_code:
            self.translate(line)

    def translate(self, line):

        parts = line.split(" = ")
        if len(parts) == 2:
            lhs, rhs = parts
            tokens = rhs.split()

            if len(tokens) == 3 and tokens[1] in "+-*/<>":
                if tokens[0] in self.values:
                    self.instructions.append(f"LOAD {tokens[0]}")
                else:
                    self.instructions.append(f"PUSH {tokens[0]}")

                if tokens[2] in self.values:
                    self.instructions.append(f"LOAD {tokens[2]}")
                else:
                    self.instructions.append(f"PUSH {tokens[2]}")

                op = {"+" : "ADD", "-" : "SUB", "*" : "MUL", "/" : "DIV", ">":"GT", "<":"LT"}[tokens[1]]
                self.instructions.append(op)
                self.instructions.append(f"STORE {lhs}")
                self.values.append(lhs)

            elif len(tokens)==3 and tokens[1] == "==":
                if tokens[0] in self.values:
                    self.instructions.append(f"LOAD {tokens[0]}")
                else:
                    self.instructions.append(f"PUSH {tokens[0]}")

                if tokens[2] in self.values:
                    self.instructions.append(f"LOAD {tokens[2]}")
                else:
                    self.instructions.append(f"PUSH {tokens[2]}")

                self.instructions.append("EQUAL")
                self.instructions.append(f"STORE {lhs}")
                self.values.append(lhs)

            else:
                if tokens[0] in self.values:
                    self.instructions.append(f"LOAD {tokens[0]}")
                else:
                    self.instructions.append(f"PUSH {tokens[0]}")
                self.instructions.append(f"STORE {lhs}")
                self.values.append(lhs)

            #TODO: Implement support for assignment expressions :
            # ['t0 = 15', 'x = t0', 't1 = x * 2', 'y = t1', 'z = 30', 't2 = x < y', 'if t2 goto L1', 't3 = x + y', 'a = t3', 't4 = a * 2', 'b = t4', 't5 = b == 60', 'if t5 goto L1', 't6 = b - x', 'c = t6', 'goto L2', 't7 = b + x', 'c = t7', 'L1:', 'goto L2', 't8 = y - x', 'a = t8', 't9 = a + z', 'c = t9', 'L1:', 't10 = c < 100', 'while t10 do', 't11 = c + 5', 'c = t11', 't12 = x + 1', 'x = t12', 'end while', 't13 = c * 2', 'result = t13', 't14 = result + x', 't15 = t14 - y', 'final = t15']
            #'if t2 goto L1'
        elif "if_false" in line:
            parts = line.split()
            if parts[1] in self.values:
                self.instructions.append(f"LOAD {parts[1]}")
            self.instructions.append(f"JUMP_IF_FALSE {parts[-1].upper()}")
        elif len(line.split()) == 1 and "L_else" in line:
            line_condition_num = line[-2]
            self.instructions.append(f"GOTO L_END{line_condition_num}:")
            self.instructions.append(line.upper())
        elif len(line.split()) == 1 and "L_end" in line:
            self.instructions.append(line.upper())
        elif len(line.split()) == 3 and "while" in line:
            parts=line.split()
            self.instructions.append(parts[0].upper()+":")
            if parts[1] in self.values:
                self.instructions.append(f"LOAD {parts[1]}")
            self.instructions.append(f"JUMP_IF_FALSE END_{parts[0].upper()}")
        elif len(line.split()) == 2 and "end" in line:
            parts= line.split()
            self.instructions.append(f"GOTO {parts[1].upper()}:")
            self.instructions.append(f"END_{parts[1].upper()}:")








    def print_bytecode(self):
        for instr in self.instructions:
            print(instr)
