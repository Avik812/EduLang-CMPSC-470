# just a start for a lexer

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[0]

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def get_next_token(self):
        # TODO: implement recognizing numbers, strings, identifiers, keywords, operators
        pass