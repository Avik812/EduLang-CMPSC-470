import pytest

from src.lexer import lexer
from src.parser import Parser
from src.ast_nodes import (
    BlockNode,
    IfNode,
    BinaryOpNode,
    IdentifierNode,
    LiteralNode,
    PrintNode,
)


def test_parse_if_print():
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

    assert isinstance(ast, BlockNode)
    assert len(ast.statements) == 1

    if_node = ast.statements[0]
    assert isinstance(if_node, IfNode)

    cond = if_node.condition
    assert isinstance(cond, BinaryOpNode)
    assert isinstance(cond.left, IdentifierNode)
    assert cond.left.name == "age"
    assert cond.op == ">="
    assert isinstance(cond.right, LiteralNode)
    assert cond.right.value == 18

    then_block = if_node.then_block
    else_block = if_node.else_block
    assert isinstance(then_block, BlockNode)
    assert isinstance(else_block, BlockNode)

    assert isinstance(then_block.statements[0], PrintNode)
    assert then_block.statements[0].expr.value == '"You are an adult"'

    assert isinstance(else_block.statements[0], PrintNode)
    assert else_block.statements[0].expr.value == '"You are not an adult"'
