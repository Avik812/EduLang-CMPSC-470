# just a start for lexer
import re

# TOKEN TYPES
TOKEN_TYPES = [
    ("NUMBER",      r"\d+"),
    ("STRING",      r'"([^"\\]|\\.)*"'),
    ("IDENT",       r"[A-Za-z_][A-Za-z0-9_]*"),
    # comments (skip): C-style single-line '//' and multi-line '/* ... */'
    ("COMMENT",     r"//[^\n]*"),
    ("COMMENT",     r"/\*[\s\S]*?\*/"),
    # now includes single-char comparisons '<' and '>' in the OP pattern
    ("OP",          r"(>=|<=|==|!=|=|>|<|\+|\-|\*|/)") ,
    ("LPAREN",      r"\("),
    ("RPAREN",      r"\)"),
    ("LBRACE",      r"\{"),
    ("RBRACE",      r"\}"),
    ("SEMICOLON",   r";"),
    ("WHITESPACE",  r"[ \t\n]+"),
]

KEYWORDS = {"if", "else", "print"}

# LEXER FUNCTION
def lexer(code):
    tokens = []
    index = 0
    
    while index < len(code):
        match_found = False

        for token_type, pattern in TOKEN_TYPES:
            regex = re.compile(pattern)
            match = regex.match(code, index)

            if match:
                text = match.group(0)
                
                # now skips both whitespace and comments
                if token_type == "WHITESPACE" or token_type == "COMMENT":
                    index += len(text)
                    match_found = True
                    break

                # convert identifiers into keywords
                if token_type == "IDENT" and text in KEYWORDS:
                    tokens.append(("KEYWORD", text))
                else:
                    tokens.append((token_type, text))

                index += len(text)
                match_found = True
                break

        if not match_found:
            raise SyntaxError(f"Illegal character at index {index}: {code[index]}")

    return tokens
