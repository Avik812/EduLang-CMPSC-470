import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import lexer
from src.parser import Parser

import pytest

from src.lexer import lexer
from src.parser import Parser
from src.interpreter import interpret


def parse(code):
    tokens = lexer(code)
    parser = Parser(tokens)
    return parser.parse()


def capture_output():
    out = []
    return out, lambda v: out.append(str(v))


def test_if_print_adult():
    code = """
    {
        if (age >= 18) {
            print("You are an adult");
        } else {
            print("You are not an adult");
        }
    }
    """

    ast = parse(code)
    out, writer = capture_output()
    interpret(ast, env={"age": 20}, output=writer)
    assert out == ["You are an adult"]


def test_if_print_not_adult():
    code = """
    {
        if (age >= 18) {
            print("You are an adult");
        } else {
            print("You are not an adult");
        }
    }
    """

    ast = parse(code)
    out, writer = capture_output()
    interpret(ast, env={"age": 16}, output=writer)
    assert out == ["You are not an adult"]


def test_print_arithmetic():
    code = """
    { print(1 + 2); }
    """

    ast = parse(code)
    out, writer = capture_output()
    interpret(ast, output=writer)
    assert out == ["3"] or out == [3]


def test_undefined_identifier_raises():
    code = """
    { print(x); }
    """

    ast = parse(code)
    out, writer = capture_output()
    with pytest.raises(NameError):
        interpret(ast, output=writer)
