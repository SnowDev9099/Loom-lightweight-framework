import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)})'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        self.advance()

    def get_string(self):
        result = ''
        self.advance()  # Skip the opening quote
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()  # Skip the closing quote
        return Token('STRING', result)

    def get_identifier(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return Token('IDENTIFIER', result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '+':
                if self.text[self.pos:self.pos+2] == '++':
                    self.skip_comment()
                    continue
                else:
                    self.advance()
                    continue

            if self.current_char == '=':
                self.advance()
                return Token('EQUALS', '=')

            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')

            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')

            if self.current_char == '.':
                self.advance()
                return Token('DOT', '.')

            if self.current_char == '"':
                return self.get_string()

            if self.current_char.isalnum():
                return self.get_identifier()

            raise Exception(f'Invalid character: {self.current_char}')

        return Token('EOF', None)
