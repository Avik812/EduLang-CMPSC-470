"""AST node definitions for EduLang.

These classes represent the concrete syntax tree nodes produced by the parser.
They are deliberately lightweight data containers so passes (semantic, interp)
can pattern-match on node types and access their fields.
"""

class PrintNode:
    def __init__(self, expr):
        self.expr = expr

class IfNode:
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class BlockNode:
    def __init__(self, statements):
        self.statements = statements

class BinaryOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class LiteralNode:
    def __init__(self, value):
        self.value = value

class IdentifierNode:
    def __init__(self, name):
        self.name = name

class AssignmentNode:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
