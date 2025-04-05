from .vm import VirtualMachine
from .lexer.lexer import Lexer
from .parser import Parser
from .analyzer import SemanticAnalyzer
from .optimizer import IRGenerator, constant_folding, common_subexpression_elimination
from .generator import CodeGenerator


# Handle Syntax and semantic Errors
source = """
// Begin test program
x = 10 + 5;
y = x * 2;
z = 30;
if (x < y) {
    a = x + y;
    b = a * 2;
    // Nested if-else
    if (b == 60) {
        c = b - x;
    } else {
        c = b + x;
    }
} else {
    a = y - x;
    c = a + z;
}
while (c < 100) {
    c = c + 5;
    x = x + 1;
    // Increment x each loop iteration
    /* Multi-line comment:
       This loop continues until c reaches 100.
    */
}
result = c * 2;
final = result + x - y;
// End of test program
"""
lexer = Lexer(source)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

generator = IRGenerator()
generator.generate(ast)
ir_code = generator.ir_code

# Optimize Code
optimized_code = common_subexpression_elimination(constant_folding(ir_code))
print(optimized_code)

# Generate Bytecode for a Stack Based Virtual Machine
codegen = CodeGenerator()
codegen.generate(optimized_code)
bytecode = codegen.instructions
for i in bytecode:
    print(i)

# Execute Bytecode
vm = VirtualMachine()
vm.execute(bytecode)
vm.print_memory()
