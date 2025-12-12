# start for parser

# AST node classes are defined in `ast_nodes.py` so other passes can import them.
from .ast_nodes import (
    PrintNode,
    IfNode,
    BlockNode,
    BinaryOpNode,
    LiteralNode,
    IdentifierNode,
    AssignmentNode,
)


# PARSER CLASS

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    # Utility
    def peek(self):
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def peek_next(self):
        nxt = self.index + 1
        return self.tokens[nxt] if nxt < len(self.tokens) else None

    def consume(self, expected_type=None):
        token = self.peek()
        if not token:
            raise SyntaxError("Unexpected end of input")

        if expected_type and token[0] != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {token}")

        self.index += 1
        return token

    # Grammar:
    # program → block
    # block → { statement* }
    # statement → print | if | expression ;
    # print → "print" "(" expr ")" ";"
    # if → "if" "(" expr ")" block ("else" block)?
    # expr → term (OP term)*
    # term → NUMBER | STRING | IDENT | "(" expr ")"

    def parse(self):
        # Parse top-level as a sequence of statements. If the file contains
        # a single top-level block, return that block (preserve previous
        # behavior). Otherwise return a BlockNode containing all top-level
        # statements.
        statements = []
        while self.peek():
            statements.append(self.parse_statement())

        if len(statements) == 1 and isinstance(statements[0], BlockNode):
            return statements[0]

        return BlockNode(statements)

    def parse_block(self):
        statements = []
        self.consume("LBRACE")

        while self.peek() and self.peek()[0] != "RBRACE":
            statements.append(self.parse_statement())

        self.consume("RBRACE")
        return BlockNode(statements)

    def parse_statement(self):
        token = self.peek()

        if token == ("KEYWORD", "print"):
            return self.parse_print()

        if token == ("KEYWORD", "if"):
            return self.parse_if()

        if token and token[0] == "LBRACE":
            return self.parse_block()

        # assignment: IDENT = expr ;
        if token and token[0] == "IDENT":
            next_tok = self.peek_next()
            if next_tok and next_tok[0] == "OP" and next_tok[1] == "=":
                # parse assignment
                name = self.consume()[1]
                # consume '=' operator
                op_tok = self.consume()
                if op_tok[1] != "=":
                    raise SyntaxError(f"Expected '=', got {op_tok}")
                expr = self.parse_expression()
                self.consume("SEMICOLON")
                return AssignmentNode(name, expr)

        # expression ;
        expr = self.parse_expression()
        self.consume("SEMICOLON")
        return expr

    def parse_print(self):
        self.consume()  # "print"
        self.consume("LPAREN")
        expr = self.parse_expression()
        self.consume("RPAREN")
        self.consume("SEMICOLON")
        return PrintNode(expr)

    def parse_if(self):
        self.consume()  # "if"
        self.consume("LPAREN")
        condition = self.parse_expression()
        self.consume("RPAREN")

        then_block = self.parse_block()

        else_block = None
        if self.peek() == ("KEYWORD", "else"):
            self.consume()
            else_block = self.parse_block()

        return IfNode(condition, then_block, else_block)

    def parse_expression(self):
        left = self.parse_term()

        while self.peek() and self.peek()[0] == "OP":
            op = self.consume()[1]
            right = self.parse_term()
            left = BinaryOpNode(left, op, right)

        return left

    def parse_term(self):
        token = self.peek()

        if token[0] == "NUMBER":
            self.consume()
            return LiteralNode(int(token[1]))

        if token[0] == "STRING":
            self.consume()
            return LiteralNode(token[1])

        if token[0] == "IDENT":
            self.consume()
            return IdentifierNode(token[1])

        if token[0] == "LPAREN":
            self.consume()
            expr = self.parse_expression()
            self.consume("RPAREN")
            return expr

        raise SyntaxError(f"Unexpected token: {token}")
