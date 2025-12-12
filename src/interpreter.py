"""Basic interpreter for EduLang AST.

This interpreter is intentionally small: it evaluates the AST node types that
the current parser produces.

Supported nodes:
- `BlockNode` : execute statements sequentially
- `PrintNode` : evaluate expression and print its value
- `IfNode`    : evaluate condition and execute the chosen block
- `BinaryOpNode`, `LiteralNode`, `IdentifierNode` : evaluate expressions

Runtime environment:
- The interpreter accepts an `env` dict mapping identifier names to Python
  values (numbers or strings). If an identifier is missing, a `NameError` is
  raised.

Note about strings: the current lexer keeps quotes in string token values
(e.g. '"hi"'). The interpreter strips these quotes when returning/printing
string values so host Python strings are used during evaluation.
"""

from typing import Any, Dict, Optional
from .scoped import ScopedEnv


from .ast_nodes import (
    BlockNode,
    IfNode,
    PrintNode,
    BinaryOpNode,
    LiteralNode,
    IdentifierNode,
    AssignmentNode,
)




class Interpreter:
    def __init__(self, env: Optional[Dict[str, Any]] = None, output=None):
        self.block_depth = 0
        # environment for identifiers
        self.env = ScopedEnv(env)
        # output is a callable used for printing; default to built-in print
        self.output = output or print

    def eval(self, node):
        """Evaluate an AST node and return its value (or None for statements)."""
        if isinstance(node, BlockNode):
            self.block_depth += 1

            if self.block_depth > 1:
                self.env.enter_scope()
            try:               
                result = None
                for stmt in node.statements:
                    result = self.eval(stmt)
                return result
            finally:
                if self.block_depth > 1:
                    self.env.exit_scope()
                self.block_depth -= 1
            
        if isinstance(node, PrintNode):
            val = self.eval(node.expr)
            # print strings without surrounding quotes
            if isinstance(val, str):
                self.output(val)
            else:
                self.output(val)
            return None

        if isinstance(node, AssignmentNode):
            val = self.eval(node.expr)
            self.env.declare(node.name, val)
            return val

        if isinstance(node, IfNode):
            cond = self.eval(node.condition)
            if cond:
                return self.eval(node.then_block)
            elif node.else_block:
                return self.eval(node.else_block)
            return None

        if isinstance(node, BinaryOpNode):
            left = self.eval(node.left)
            right = self.eval(node.right)
            op = node.op

            if op == "+":
                return left + right
            if op == "-":
                return left - right
            if op == "*":
                return left * right
            if op == "/":
                return left / right

            if op == ">":
                return left > right
            if op == "<":
                return left < right
            if op == ">=":
                return left >= right
            if op == "<=":
                return left <= right

            if op == "==":
                return left == right
            if op == "!=":
                return left != right

            raise RuntimeError(f"Unknown operator: {op}")

        if isinstance(node, LiteralNode):
            v = node.value
            # numbers are ints already
            if isinstance(v, int):
                return v
            # strip surrounding quotes for strings
            if isinstance(v, str):
                if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
                    return v[1:-1]
                return v
            return v

        if isinstance(node, IdentifierNode):
            return self.env.lookup(node.name)

        raise RuntimeError(f"Interpreter cannot handle node: {node!r}")


def interpret(ast, env: Optional[Dict[str, Any]] = None, output=None):
    """Convenience function: create an Interpreter and run `ast`."""
    it = Interpreter(env=env, output=output)
    return it.eval(ast)




