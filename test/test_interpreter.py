import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import lexer
from src.parser import Parser

code = """
{
    if (age >= 18) {
        print("You are an adult");
    } else {
        print("You are not an adult");
    }
}
"""

tokens = lexer(code)
parser = Parser(tokens)
ast = parser.parse()

print("Tokens:", tokens)
print("AST:", ast)