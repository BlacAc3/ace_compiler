from .lexer.lexer import Lexer
from .parser.parser import Parser

source = """if (x > 10) {
    y = 5;
} else {
    y = 0;
}

while (y < 10) {
    y = y + 1;
}"""
lexer = Lexer(source)
tokens = lexer.tokenize()
print(tokens)
parser = Parser(tokens)
ast = parser.parse()
print(ast)
