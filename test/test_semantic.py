import pytest

from src.lexer import lexer
from src.parser import Parser
from src.semantic import SemanticAnalyzer, SemanticError


def parse(code):
    tokens = lexer(code)
    parser = Parser(tokens)
    return parser.parse()


def test_arithmetic_ok():
    ast = parse('{ print(1 + 2); }')
    analyzer = SemanticAnalyzer()
    # should not raise
    analyzer.analyze(ast)


def test_arithmetic_type_error():
    ast = parse('{ print(1 + "hi"); }')
    analyzer = SemanticAnalyzer()
    with pytest.raises(SemanticError):
        analyzer.analyze(ast)


def test_if_condition_type_error():
    ast = parse('{ if ("notbool") { print("ok"); } }')
    analyzer = SemanticAnalyzer()
    with pytest.raises(SemanticError):
        analyzer.analyze(ast)


def test_strict_undefined_identifier():
    ast = parse('{ print(x); }')
    analyzer = SemanticAnalyzer(strict=True)
    with pytest.raises(SemanticError):
        analyzer.analyze(ast)


def test_equality_mismatch_raises():
    ast = parse('{ print(1 == "1"); }')
    analyzer = SemanticAnalyzer()
    with pytest.raises(SemanticError):
        analyzer.analyze(ast)


def test_assignment_records_type_and_allows_use():
    ast = parse('{ x = 10; print(x); }')
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    assert analyzer.symbols.get('x') == 'number'


def test_assignment_type_error_on_use():
    ast = parse('{ x = "hi"; print(x + 1); }')
    analyzer = SemanticAnalyzer()
    with pytest.raises(SemanticError):
        analyzer.analyze(ast)
