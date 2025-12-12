from src.lexer import lexer


def test_lexer_tokens():
    code = 'print("hi"); if (x >= 10) { print("ok"); }'
    tokens = lexer(code)

    expected = [
        ("KEYWORD", "print"), ("LPAREN", "("), ("STRING", '"hi"'), ("RPAREN", ")"), ("SEMICOLON", ";"),
        ("KEYWORD", "if"), ("LPAREN", "("), ("IDENT", "x"), ("OP", ">="), ("NUMBER", "10"), ("RPAREN", ")"),
        ("LBRACE", "{"), ("KEYWORD", "print"), ("LPAREN", "("), ("STRING", '"ok"'), ("RPAREN", ")"), ("SEMICOLON", ";"), ("RBRACE", "}"),
    ]

    assert tokens == expected
